"""Notification dispatcher - routes alerts to configured channels."""

import json
from datetime import datetime
from pathlib import Path
from typing import Optional

from .models import Alert, AlertPriority, DeliveryResult, DeliveryStatus, NotificationRule, RateLimitConfig
from .channels import SlackChannel, TeamsChannel, DiscordChannel, EmailChannel, PagerDutyChannel, NotificationChannel


class NotificationDispatcher:
    """Central dispatcher for routing alerts to notification channels."""
    
    def __init__(self, config_path: str = "config/user-preferences.json"):
        self.config_path = Path(config_path)
        self.channels: dict[str, NotificationChannel] = {}
        self.rules: list[NotificationRule] = []
        self.rate_limits: dict[AlertPriority, RateLimitConfig] = {}
        self.delivery_log: list[DeliveryResult] = []
        
        self._load_config()
    
    def _load_config(self):
        """Load notification configuration from user preferences."""
        if not self.config_path.exists():
            return
        
        try:
            with open(self.config_path) as f:
                config = json.load(f)
            
            notifications = config.get("notifications", {})
            if not notifications.get("enabled", False):
                return
            
            channels_config = notifications.get("channels", {})
            
            # Initialize Slack
            slack_config = channels_config.get("slack", {})
            if slack_config.get("enabled") and slack_config.get("webhook_url"):
                self.channels["slack"] = SlackChannel(
                    webhook_url=slack_config["webhook_url"],
                    channel=slack_config.get("channel", ""),
                    mention_on_critical=slack_config.get("mention_on_critical", "")
                )
            
            # Initialize Teams
            teams_config = channels_config.get("teams", {})
            if teams_config.get("enabled") and teams_config.get("webhook_url"):
                self.channels["teams"] = TeamsChannel(
                    webhook_url=teams_config["webhook_url"],
                    mention_on_critical=teams_config.get("mention_on_critical", "")
                )
            
            # Initialize Discord
            discord_config = channels_config.get("discord", {})
            if discord_config.get("enabled") and discord_config.get("webhook_url"):
                self.channels["discord"] = DiscordChannel(
                    webhook_url=discord_config["webhook_url"],
                    role_id_critical=discord_config.get("role_id_critical", "")
                )
            
            # Initialize Email
            email_config = channels_config.get("email", {})
            if email_config.get("enabled") and email_config.get("smtp_host"):
                self.channels["email"] = EmailChannel(
                    smtp_host=email_config["smtp_host"],
                    smtp_port=email_config.get("smtp_port", 587),
                    smtp_user=email_config.get("smtp_user", ""),
                    smtp_password=email_config.get("smtp_password", ""),
                    from_address=email_config.get("from_address", ""),
                    recipients=email_config.get("recipients", []),
                    use_tls=email_config.get("use_tls", True)
                )
            
            # Initialize PagerDuty
            pd_config = channels_config.get("pagerduty", {})
            if pd_config.get("enabled") and pd_config.get("routing_key"):
                self.channels["pagerduty"] = PagerDutyChannel(
                    routing_key=pd_config["routing_key"],
                    severity_threshold=pd_config.get("severity_threshold", "critical")
                )
            
            # Load rules
            for rule_config in notifications.get("rules", []):
                self.rules.append(NotificationRule(
                    name=rule_config["name"],
                    condition=rule_config["condition"],
                    channels=rule_config["channels"],
                    priority=AlertPriority(rule_config.get("priority", "medium")),
                    enabled=rule_config.get("enabled", True)
                ))
            
            # Load rate limits
            rate_limits_config = notifications.get("rate_limits", {})
            for priority in AlertPriority:
                limit_config = rate_limits_config.get(priority.value, {})
                self.rate_limits[priority] = RateLimitConfig(
                    priority=priority,
                    max_per_hour=limit_config.get("max_per_hour", -1),
                    max_per_day=limit_config.get("max_per_day", -1)
                )
            
        except Exception as e:
            print(f"Warning: Failed to load notification config: {e}")
    
    def dispatch(self, alert: Alert) -> list[DeliveryResult]:
        """Dispatch an alert to all matching channels."""
        results = []
        
        # Check rate limits
        rate_limit = self.rate_limits.get(alert.priority)
        if rate_limit and not rate_limit.is_allowed():
            results.append(DeliveryResult(
                alert_id=alert.id,
                channel="dispatcher",
                status=DeliveryStatus.RATE_LIMITED,
                response_message=f"Rate limit exceeded for {alert.priority.value} priority"
            ))
            return results
        
        # Determine target channels from rules
        target_channels = set()
        for rule in self.rules:
            if rule.enabled and rule.matches(alert):
                target_channels.update(rule.channels)
        
        # If no rules match, use default channels based on priority
        if not target_channels:
            target_channels = self._get_default_channels(alert.priority)
        
        # Dispatch to each channel
        for channel_name in target_channels:
            channel = self.channels.get(channel_name)
            if channel and channel.is_configured():
                result = channel.send(alert)
                results.append(result)
                self.delivery_log.append(result)
            else:
                results.append(DeliveryResult(
                    alert_id=alert.id,
                    channel=channel_name,
                    status=DeliveryStatus.FAILED,
                    response_message=f"Channel {channel_name} not configured"
                ))
        
        # Record rate limit usage
        if rate_limit and any(r.status == DeliveryStatus.SENT for r in results):
            rate_limit.record_send()
        
        return results
    
    def _get_default_channels(self, priority: AlertPriority) -> set[str]:
        """Get default channels for a priority level."""
        defaults = {
            AlertPriority.CRITICAL: {"slack", "pagerduty", "email"},
            AlertPriority.HIGH: {"slack", "email"},
            AlertPriority.MEDIUM: {"slack"},
            AlertPriority.LOW: {"email"},
            AlertPriority.INFO: set(),
        }
        return defaults.get(priority, set())
    
    def test_channel(self, channel_name: str) -> DeliveryResult:
        """Send a test notification to a specific channel."""
        channel = self.channels.get(channel_name)
        if not channel:
            return DeliveryResult(
                alert_id="test",
                channel=channel_name,
                status=DeliveryStatus.FAILED,
                response_message=f"Channel {channel_name} not found"
            )
        
        if not channel.is_configured():
            return DeliveryResult(
                alert_id="test",
                channel=channel_name,
                status=DeliveryStatus.FAILED,
                response_message=f"Channel {channel_name} not properly configured"
            )
        
        return channel.test()
    
    def get_status(self) -> dict:
        """Get current notification system status."""
        status = {
            "enabled": len(self.channels) > 0,
            "channels": {},
            "rules_count": len(self.rules),
            "recent_deliveries": {
                "sent": 0,
                "failed": 0,
                "rate_limited": 0
            }
        }
        
        for name, channel in self.channels.items():
            status["channels"][name] = {
                "configured": channel.is_configured(),
                "type": type(channel).__name__
            }
        
        # Count recent deliveries (last 24 hours)
        cutoff = datetime.utcnow().replace(hour=0, minute=0, second=0, microsecond=0)
        for result in self.delivery_log:
            if result.timestamp >= cutoff:
                if result.status == DeliveryStatus.SENT:
                    status["recent_deliveries"]["sent"] += 1
                elif result.status == DeliveryStatus.FAILED:
                    status["recent_deliveries"]["failed"] += 1
                elif result.status == DeliveryStatus.RATE_LIMITED:
                    status["recent_deliveries"]["rate_limited"] += 1
        
        return status
    
    def add_rule(self, rule: NotificationRule):
        """Add a new notification rule."""
        self.rules.append(rule)
        self._save_rules()
    
    def remove_rule(self, rule_name: str) -> bool:
        """Remove a notification rule by name."""
        for i, rule in enumerate(self.rules):
            if rule.name == rule_name:
                self.rules.pop(i)
                self._save_rules()
                return True
        return False
    
    def _save_rules(self):
        """Save rules back to configuration file."""
        if not self.config_path.exists():
            return
        
        try:
            with open(self.config_path) as f:
                config = json.load(f)
            
            if "notifications" not in config:
                config["notifications"] = {}
            
            config["notifications"]["rules"] = [
                {
                    "name": r.name,
                    "condition": r.condition,
                    "channels": r.channels,
                    "priority": r.priority.value,
                    "enabled": r.enabled
                }
                for r in self.rules
            ]
            
            with open(self.config_path, "w") as f:
                json.dump(config, f, indent=2)
        except Exception as e:
            print(f"Warning: Failed to save notification rules: {e}")


def create_alert_from_threat(threat_data: dict) -> Alert:
    """Create an Alert from threat data dictionary."""
    # Determine priority
    priority = AlertPriority.MEDIUM
    
    if threat_data.get("kev_listed"):
        priority = AlertPriority.CRITICAL
    elif (threat_data.get("cvss_v3") or 0) >= 9.0:
        priority = AlertPriority.CRITICAL
    elif (threat_data.get("epss_score") or 0) >= 0.7:
        priority = AlertPriority.CRITICAL
    elif (threat_data.get("cvss_v3") or 0) >= 7.0:
        priority = AlertPriority.HIGH
    elif threat_data.get("affected_crown_jewels"):
        priority = AlertPriority.HIGH
    
    return Alert(
        id=threat_data.get("id", f"alert_{datetime.utcnow().strftime('%Y%m%d%H%M%S')}"),
        title=threat_data.get("title", "Unknown Threat"),
        summary=threat_data.get("summary", ""),
        priority=priority,
        cves=threat_data.get("cves", []),
        cvss_score=threat_data.get("cvss_v3"),
        epss_score=threat_data.get("epss_score"),
        kev_listed=threat_data.get("kev_listed", False),
        exploit_status=threat_data.get("exploit_status"),
        affected_crown_jewels=threat_data.get("affected_crown_jewels", []),
        source_name=threat_data.get("source_name", ""),
        source_url=threat_data.get("source_url", ""),
        threat_id=threat_data.get("id"),
    )
