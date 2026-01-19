"""Notification channel implementations."""

import json
import smtplib
import ssl
from abc import ABC, abstractmethod
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from datetime import datetime
from typing import Optional
import urllib.request
import urllib.error

from .models import Alert, DeliveryResult, DeliveryStatus


class NotificationChannel(ABC):
    """Base class for notification channels."""
    
    @abstractmethod
    def send(self, alert: Alert) -> DeliveryResult:
        """Send an alert through this channel."""
        pass
    
    @abstractmethod
    def test(self) -> DeliveryResult:
        """Send a test notification."""
        pass
    
    @abstractmethod
    def is_configured(self) -> bool:
        """Check if channel is properly configured."""
        pass


class SlackChannel(NotificationChannel):
    """Slack webhook notification channel."""
    
    def __init__(self, webhook_url: str, channel: str = "", mention_on_critical: str = ""):
        self.webhook_url = webhook_url
        self.channel = channel
        self.mention_on_critical = mention_on_critical
    
    def is_configured(self) -> bool:
        return bool(self.webhook_url and self.webhook_url.startswith("https://hooks.slack.com/"))
    
    def send(self, alert: Alert) -> DeliveryResult:
        """Send alert to Slack."""
        if not self.is_configured():
            return DeliveryResult(
                alert_id=alert.id,
                channel="slack",
                status=DeliveryStatus.FAILED,
                response_message="Slack webhook not configured"
            )
        
        payload = self._build_payload(alert)
        return self._send_webhook(alert.id, payload)
    
    def test(self) -> DeliveryResult:
        """Send test message to Slack."""
        test_alert = Alert(
            id="test_" + datetime.utcnow().strftime("%Y%m%d%H%M%S"),
            title="NOMAD Test Alert",
            summary="This is a test notification from NOMAD. Your Slack integration is working!",
            priority=Alert.AlertPriority.INFO if hasattr(Alert, 'AlertPriority') else None,
        )
        # Fix priority assignment
        from .models import AlertPriority
        test_alert.priority = AlertPriority.INFO
        return self.send(test_alert)
    
    def _build_payload(self, alert: Alert) -> dict:
        """Build Slack block kit payload."""
        emoji = alert.get_severity_emoji()
        color = alert.get_severity_color()
        
        # Build fields
        fields = []
        if alert.cvss_score:
            fields.append({"type": "mrkdwn", "text": f"*CVSS:* {alert.cvss_score}"})
        if alert.epss_score:
            fields.append({"type": "mrkdwn", "text": f"*EPSS:* {alert.epss_score:.1%}"})
        if alert.kev_listed:
            fields.append({"type": "mrkdwn", "text": "*KEV:* Yes ⚠️"})
        if alert.exploit_status:
            fields.append({"type": "mrkdwn", "text": f"*Exploit:* {alert.exploit_status}"})
        
        blocks = [
            {
                "type": "header",
                "text": {
                    "type": "plain_text",
                    "text": f"{emoji} {alert.priority.value.upper()}: {alert.title[:100]}",
                    "emoji": True
                }
            },
            {
                "type": "section",
                "text": {
                    "type": "mrkdwn",
                    "text": alert.summary[:500]
                }
            }
        ]
        
        if fields:
            blocks.append({
                "type": "section",
                "fields": fields[:8]  # Slack limit
            })
        
        if alert.cves:
            blocks.append({
                "type": "section",
                "text": {
                    "type": "mrkdwn",
                    "text": f"*CVEs:* {', '.join(alert.cves[:5])}"
                }
            })
        
        if alert.affected_crown_jewels:
            blocks.append({
                "type": "section",
                "text": {
                    "type": "mrkdwn",
                    "text": f"*Affected Systems:* {', '.join(alert.affected_crown_jewels)}"
                }
            })
        
        # Add action buttons
        actions = []
        if alert.source_url:
            actions.append({
                "type": "button",
                "text": {"type": "plain_text", "text": "View Source"},
                "url": alert.source_url
            })
        if alert.report_url:
            actions.append({
                "type": "button",
                "text": {"type": "plain_text", "text": "View Report"},
                "url": alert.report_url,
                "style": "primary"
            })
        
        if actions:
            blocks.append({"type": "actions", "elements": actions})
        
        # Add context
        blocks.append({
            "type": "context",
            "elements": [
                {
                    "type": "mrkdwn",
                    "text": f"Source: {alert.source_name} | {alert.created_at.strftime('%Y-%m-%d %H:%M UTC')}"
                }
            ]
        })
        
        payload = {"blocks": blocks}
        
        # Add mention for critical alerts
        from .models import AlertPriority
        if alert.priority == AlertPriority.CRITICAL and self.mention_on_critical:
            payload["text"] = f"{self.mention_on_critical} Critical threat detected!"
        
        return payload
    
    def _send_webhook(self, alert_id: str, payload: dict) -> DeliveryResult:
        """Send payload to Slack webhook."""
        try:
            data = json.dumps(payload).encode("utf-8")
            req = urllib.request.Request(
                self.webhook_url,
                data=data,
                headers={"Content-Type": "application/json"}
            )
            
            with urllib.request.urlopen(req, timeout=10) as response:
                return DeliveryResult(
                    alert_id=alert_id,
                    channel="slack",
                    status=DeliveryStatus.SENT,
                    response_code=response.status,
                    response_message="OK"
                )
        except urllib.error.HTTPError as e:
            return DeliveryResult(
                alert_id=alert_id,
                channel="slack",
                status=DeliveryStatus.FAILED,
                response_code=e.code,
                response_message=str(e.reason)
            )
        except Exception as e:
            return DeliveryResult(
                alert_id=alert_id,
                channel="slack",
                status=DeliveryStatus.FAILED,
                response_message=str(e)
            )


class TeamsChannel(NotificationChannel):
    """Microsoft Teams webhook notification channel."""
    
    def __init__(self, webhook_url: str, mention_on_critical: str = ""):
        self.webhook_url = webhook_url
        self.mention_on_critical = mention_on_critical
    
    def is_configured(self) -> bool:
        return bool(self.webhook_url and "webhook.office.com" in self.webhook_url)
    
    def send(self, alert: Alert) -> DeliveryResult:
        """Send alert to Teams."""
        if not self.is_configured():
            return DeliveryResult(
                alert_id=alert.id,
                channel="teams",
                status=DeliveryStatus.FAILED,
                response_message="Teams webhook not configured"
            )
        
        payload = self._build_payload(alert)
        return self._send_webhook(alert.id, payload)
    
    def test(self) -> DeliveryResult:
        from .models import AlertPriority
        test_alert = Alert(
            id="test_" + datetime.utcnow().strftime("%Y%m%d%H%M%S"),
            title="NOMAD Test Alert",
            summary="This is a test notification from NOMAD. Your Teams integration is working!",
            priority=AlertPriority.INFO,
        )
        return self.send(test_alert)
    
    def _build_payload(self, alert: Alert) -> dict:
        """Build Teams adaptive card payload."""
        emoji = alert.get_severity_emoji()
        color = alert.get_severity_color()
        
        facts = []
        if alert.cvss_score:
            facts.append({"title": "CVSS", "value": str(alert.cvss_score)})
        if alert.epss_score:
            facts.append({"title": "EPSS", "value": f"{alert.epss_score:.1%}"})
        if alert.kev_listed:
            facts.append({"title": "KEV Listed", "value": "Yes ⚠️"})
        if alert.cves:
            facts.append({"title": "CVEs", "value": ", ".join(alert.cves[:3])})
        
        return {
            "@type": "MessageCard",
            "@context": "http://schema.org/extensions",
            "themeColor": color.replace("#", ""),
            "summary": f"{alert.priority.value.upper()}: {alert.title}",
            "sections": [{
                "activityTitle": f"{emoji} {alert.priority.value.upper()}: {alert.title}",
                "activitySubtitle": f"Source: {alert.source_name}",
                "facts": facts,
                "text": alert.summary[:500],
                "markdown": True
            }],
            "potentialAction": [
                {
                    "@type": "OpenUri",
                    "name": "View Details",
                    "targets": [{"os": "default", "uri": alert.source_url or alert.report_url or ""}]
                }
            ] if (alert.source_url or alert.report_url) else []
        }
    
    def _send_webhook(self, alert_id: str, payload: dict) -> DeliveryResult:
        """Send payload to Teams webhook."""
        try:
            data = json.dumps(payload).encode("utf-8")
            req = urllib.request.Request(
                self.webhook_url,
                data=data,
                headers={"Content-Type": "application/json"}
            )
            
            with urllib.request.urlopen(req, timeout=10) as response:
                return DeliveryResult(
                    alert_id=alert_id,
                    channel="teams",
                    status=DeliveryStatus.SENT,
                    response_code=response.status,
                    response_message="OK"
                )
        except Exception as e:
            return DeliveryResult(
                alert_id=alert_id,
                channel="teams",
                status=DeliveryStatus.FAILED,
                response_message=str(e)
            )


class DiscordChannel(NotificationChannel):
    """Discord webhook notification channel."""
    
    def __init__(self, webhook_url: str, role_id_critical: str = ""):
        self.webhook_url = webhook_url
        self.role_id_critical = role_id_critical
    
    def is_configured(self) -> bool:
        return bool(self.webhook_url and "discord.com/api/webhooks" in self.webhook_url)
    
    def send(self, alert: Alert) -> DeliveryResult:
        """Send alert to Discord."""
        if not self.is_configured():
            return DeliveryResult(
                alert_id=alert.id,
                channel="discord",
                status=DeliveryStatus.FAILED,
                response_message="Discord webhook not configured"
            )
        
        payload = self._build_payload(alert)
        return self._send_webhook(alert.id, payload)
    
    def test(self) -> DeliveryResult:
        from .models import AlertPriority
        test_alert = Alert(
            id="test_" + datetime.utcnow().strftime("%Y%m%d%H%M%S"),
            title="NOMAD Test Alert",
            summary="This is a test notification from NOMAD. Your Discord integration is working!",
            priority=AlertPriority.INFO,
        )
        return self.send(test_alert)
    
    def _build_payload(self, alert: Alert) -> dict:
        """Build Discord embed payload."""
        color_int = int(alert.get_severity_color().replace("#", ""), 16)
        
        fields = []
        if alert.cvss_score:
            fields.append({"name": "CVSS", "value": str(alert.cvss_score), "inline": True})
        if alert.epss_score:
            fields.append({"name": "EPSS", "value": f"{alert.epss_score:.1%}", "inline": True})
        if alert.kev_listed:
            fields.append({"name": "KEV", "value": "Yes ⚠️", "inline": True})
        if alert.cves:
            fields.append({"name": "CVEs", "value": ", ".join(alert.cves[:5]), "inline": False})
        if alert.affected_crown_jewels:
            fields.append({"name": "Affected Systems", "value": ", ".join(alert.affected_crown_jewels), "inline": False})
        
        content = ""
        from .models import AlertPriority
        if alert.priority == AlertPriority.CRITICAL and self.role_id_critical:
            content = f"<@&{self.role_id_critical}> Critical threat detected!"
        
        return {
            "content": content,
            "embeds": [{
                "title": f"{alert.get_severity_emoji()} {alert.priority.value.upper()}: {alert.title[:200]}",
                "description": alert.summary[:2000],
                "color": color_int,
                "fields": fields[:10],
                "footer": {"text": f"Source: {alert.source_name}"},
                "timestamp": alert.created_at.isoformat(),
                "url": alert.source_url or alert.report_url or None
            }]
        }
    
    def _send_webhook(self, alert_id: str, payload: dict) -> DeliveryResult:
        """Send payload to Discord webhook."""
        try:
            data = json.dumps(payload).encode("utf-8")
            req = urllib.request.Request(
                self.webhook_url,
                data=data,
                headers={"Content-Type": "application/json"}
            )
            
            with urllib.request.urlopen(req, timeout=10) as response:
                return DeliveryResult(
                    alert_id=alert_id,
                    channel="discord",
                    status=DeliveryStatus.SENT,
                    response_code=response.status,
                    response_message="OK"
                )
        except Exception as e:
            return DeliveryResult(
                alert_id=alert_id,
                channel="discord",
                status=DeliveryStatus.FAILED,
                response_message=str(e)
            )


class EmailChannel(NotificationChannel):
    """Email (SMTP) notification channel."""
    
    def __init__(
        self,
        smtp_host: str,
        smtp_port: int = 587,
        smtp_user: str = "",
        smtp_password: str = "",
        from_address: str = "",
        recipients: list[str] = None,
        use_tls: bool = True
    ):
        self.smtp_host = smtp_host
        self.smtp_port = smtp_port
        self.smtp_user = smtp_user
        self.smtp_password = smtp_password
        self.from_address = from_address
        self.recipients = recipients or []
        self.use_tls = use_tls
    
    def is_configured(self) -> bool:
        return bool(self.smtp_host and self.from_address and self.recipients)
    
    def send(self, alert: Alert) -> DeliveryResult:
        """Send alert via email."""
        if not self.is_configured():
            return DeliveryResult(
                alert_id=alert.id,
                channel="email",
                status=DeliveryStatus.FAILED,
                response_message="Email not configured"
            )
        
        try:
            msg = self._build_message(alert)
            self._send_smtp(msg)
            return DeliveryResult(
                alert_id=alert.id,
                channel="email",
                status=DeliveryStatus.SENT,
                response_message=f"Sent to {len(self.recipients)} recipients"
            )
        except Exception as e:
            return DeliveryResult(
                alert_id=alert.id,
                channel="email",
                status=DeliveryStatus.FAILED,
                response_message=str(e)
            )
    
    def test(self) -> DeliveryResult:
        from .models import AlertPriority
        test_alert = Alert(
            id="test_" + datetime.utcnow().strftime("%Y%m%d%H%M%S"),
            title="NOMAD Test Alert",
            summary="This is a test notification from NOMAD. Your email integration is working!",
            priority=AlertPriority.INFO,
        )
        return self.send(test_alert)
    
    def _build_message(self, alert: Alert) -> MIMEMultipart:
        """Build email message."""
        msg = MIMEMultipart("alternative")
        msg["Subject"] = f"[{alert.priority.value.upper()}] {alert.title}"
        msg["From"] = self.from_address
        msg["To"] = ", ".join(self.recipients)
        
        # Plain text version
        text = f"""
{alert.priority.value.upper()} THREAT ALERT
{'=' * 40}

{alert.title}

{alert.summary}

Details:
- CVSS: {alert.cvss_score or 'N/A'}
- EPSS: {f'{alert.epss_score:.1%}' if alert.epss_score else 'N/A'}
- KEV Listed: {'Yes' if alert.kev_listed else 'No'}
- CVEs: {', '.join(alert.cves) if alert.cves else 'None'}

Affected Systems: {', '.join(alert.affected_crown_jewels) if alert.affected_crown_jewels else 'None identified'}

Source: {alert.source_name}
Link: {alert.source_url or alert.report_url or 'N/A'}

---
Sent by NOMAD Threat Intelligence
"""
        
        # HTML version
        html = f"""
<!DOCTYPE html>
<html>
<head><meta charset="utf-8"></head>
<body style="font-family: Arial, sans-serif; max-width: 600px; margin: 0 auto;">
    <div style="background: {alert.get_severity_color()}; color: white; padding: 16px 20px;">
        <h1 style="margin: 0; font-size: 18px;">
            {alert.get_severity_emoji()} {alert.priority.value.upper()} THREAT ALERT
        </h1>
    </div>
    <div style="padding: 20px; background: #f9fafb;">
        <h2 style="margin-top: 0; color: #1f2937;">{alert.title}</h2>
        <p style="color: #4b5563; line-height: 1.6;">{alert.summary}</p>
        
        <table style="width: 100%; border-collapse: collapse; margin: 20px 0;">
            <tr>
                <td style="padding: 8px; border-bottom: 1px solid #e5e7eb;"><strong>CVSS</strong></td>
                <td style="padding: 8px; border-bottom: 1px solid #e5e7eb;">{alert.cvss_score or 'N/A'}</td>
            </tr>
            <tr>
                <td style="padding: 8px; border-bottom: 1px solid #e5e7eb;"><strong>EPSS</strong></td>
                <td style="padding: 8px; border-bottom: 1px solid #e5e7eb;">{f'{alert.epss_score:.1%}' if alert.epss_score else 'N/A'}</td>
            </tr>
            <tr>
                <td style="padding: 8px; border-bottom: 1px solid #e5e7eb;"><strong>KEV Listed</strong></td>
                <td style="padding: 8px; border-bottom: 1px solid #e5e7eb;">{'<span style="color: #dc2626;">Yes ⚠️</span>' if alert.kev_listed else 'No'}</td>
            </tr>
            <tr>
                <td style="padding: 8px; border-bottom: 1px solid #e5e7eb;"><strong>CVEs</strong></td>
                <td style="padding: 8px; border-bottom: 1px solid #e5e7eb;">{', '.join(alert.cves) if alert.cves else 'None'}</td>
            </tr>
        </table>
        
        {'<h3>Affected Systems</h3><ul>' + ''.join(f'<li>{cj}</li>' for cj in alert.affected_crown_jewels) + '</ul>' if alert.affected_crown_jewels else ''}
        
        <div style="margin-top: 20px;">
            <a href="{alert.source_url or alert.report_url or '#'}" 
               style="background: #2563eb; color: white; padding: 12px 24px; text-decoration: none; border-radius: 4px; display: inline-block;">
                View Full Details
            </a>
        </div>
        
        <p style="margin-top: 20px; font-size: 12px; color: #6b7280;">
            Source: {alert.source_name}<br>
            Sent by NOMAD Threat Intelligence
        </p>
    </div>
</body>
</html>
"""
        
        msg.attach(MIMEText(text, "plain"))
        msg.attach(MIMEText(html, "html"))
        
        return msg
    
    def _send_smtp(self, msg: MIMEMultipart):
        """Send message via SMTP."""
        context = ssl.create_default_context()
        
        if self.use_tls:
            with smtplib.SMTP(self.smtp_host, self.smtp_port) as server:
                server.starttls(context=context)
                if self.smtp_user and self.smtp_password:
                    server.login(self.smtp_user, self.smtp_password)
                server.sendmail(self.from_address, self.recipients, msg.as_string())
        else:
            with smtplib.SMTP_SSL(self.smtp_host, self.smtp_port, context=context) as server:
                if self.smtp_user and self.smtp_password:
                    server.login(self.smtp_user, self.smtp_password)
                server.sendmail(self.from_address, self.recipients, msg.as_string())


class PagerDutyChannel(NotificationChannel):
    """PagerDuty Events API v2 notification channel."""
    
    EVENTS_API_URL = "https://events.pagerduty.com/v2/enqueue"
    
    def __init__(self, routing_key: str, severity_threshold: str = "critical"):
        self.routing_key = routing_key
        self.severity_threshold = severity_threshold
    
    def is_configured(self) -> bool:
        return bool(self.routing_key and len(self.routing_key) == 32)
    
    def send(self, alert: Alert) -> DeliveryResult:
        """Send alert to PagerDuty."""
        if not self.is_configured():
            return DeliveryResult(
                alert_id=alert.id,
                channel="pagerduty",
                status=DeliveryStatus.FAILED,
                response_message="PagerDuty routing key not configured"
            )
        
        # Map priority to PagerDuty severity
        from .models import AlertPriority
        severity_map = {
            AlertPriority.CRITICAL: "critical",
            AlertPriority.HIGH: "error",
            AlertPriority.MEDIUM: "warning",
            AlertPriority.LOW: "info",
            AlertPriority.INFO: "info",
        }
        
        payload = {
            "routing_key": self.routing_key,
            "event_action": "trigger",
            "dedup_key": alert.id,
            "payload": {
                "summary": f"[{alert.priority.value.upper()}] {alert.title}"[:1024],
                "source": "NOMAD Threat Intelligence",
                "severity": severity_map.get(alert.priority, "warning"),
                "timestamp": alert.created_at.isoformat(),
                "custom_details": {
                    "summary": alert.summary,
                    "cvss_score": alert.cvss_score,
                    "epss_score": alert.epss_score,
                    "kev_listed": alert.kev_listed,
                    "cves": alert.cves,
                    "affected_systems": alert.affected_crown_jewels,
                    "source_url": alert.source_url,
                }
            },
            "links": [{"href": alert.source_url, "text": "View Source"}] if alert.source_url else [],
        }
        
        try:
            data = json.dumps(payload).encode("utf-8")
            req = urllib.request.Request(
                self.EVENTS_API_URL,
                data=data,
                headers={"Content-Type": "application/json"}
            )
            
            with urllib.request.urlopen(req, timeout=10) as response:
                result = json.loads(response.read().decode())
                return DeliveryResult(
                    alert_id=alert.id,
                    channel="pagerduty",
                    status=DeliveryStatus.SENT,
                    response_code=response.status,
                    response_message=result.get("message", "OK")
                )
        except Exception as e:
            return DeliveryResult(
                alert_id=alert.id,
                channel="pagerduty",
                status=DeliveryStatus.FAILED,
                response_message=str(e)
            )
    
    def test(self) -> DeliveryResult:
        from .models import AlertPriority
        test_alert = Alert(
            id="test_" + datetime.utcnow().strftime("%Y%m%d%H%M%S"),
            title="NOMAD Test Alert - This is a test",
            summary="This is a test notification from NOMAD. Your PagerDuty integration is working! This incident can be resolved.",
            priority=AlertPriority.INFO,
        )
        return self.send(test_alert)
