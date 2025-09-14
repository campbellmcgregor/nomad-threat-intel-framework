"""
Environment configuration manager for NOMAD Framework
Handles loading and validation of environment variables
"""

import os
import logging
from pathlib import Path
from typing import Dict, Any, Optional, List
from dotenv import load_dotenv

class EnvironmentConfig:
    """Centralized environment configuration management"""

    def __init__(self, env_file: Optional[str] = None):
        """Initialize environment configuration

        Args:
            env_file: Path to .env file (defaults to .env in project root)
        """
        # Load environment variables
        if env_file:
            load_dotenv(env_file)
        else:
            # Try to load from project root
            project_root = Path(__file__).parent.parent
            env_path = project_root / ".env"
            if env_path.exists():
                load_dotenv(env_path)

        self.logger = logging.getLogger("nomad.config")
        self._validate_required_vars()

    def _validate_required_vars(self) -> None:
        """Validate that required environment variables are set"""
        required_vars = [
            "ANTHROPIC_API_KEY",  # Primary requirement for LLM processing
        ]

        missing_vars = []
        for var in required_vars:
            if not os.getenv(var):
                missing_vars.append(var)

        if missing_vars:
            self.logger.warning(
                f"Missing required environment variables: {', '.join(missing_vars)}. "
                "Some features may not work correctly."
            )

    # ========================================================================
    # LLM Configuration
    # ========================================================================

    @property
    def anthropic_api_key(self) -> Optional[str]:
        """Get Anthropic API key"""
        return os.getenv("ANTHROPIC_API_KEY")

    @property
    def openai_api_key(self) -> Optional[str]:
        """Get OpenAI API key"""
        return os.getenv("OPENAI_API_KEY")

    @property
    def default_model(self) -> str:
        """Get default LLM model to use"""
        return os.getenv("DEFAULT_MODEL", "claude-3-sonnet-20240229")

    @property
    def api_timeout(self) -> int:
        """Get API timeout in seconds"""
        return int(os.getenv("API_TIMEOUT", "300"))

    @property
    def max_retries(self) -> int:
        """Get maximum API retries"""
        return int(os.getenv("MAX_RETRIES", "3"))

    @property
    def rate_limit_rpm(self) -> int:
        """Get rate limit in requests per minute"""
        return int(os.getenv("RATE_LIMIT_RPM", "60"))

    # ========================================================================
    # Threat Intelligence APIs
    # ========================================================================

    @property
    def nvd_api_key(self) -> Optional[str]:
        """Get NVD API key"""
        return os.getenv("NVD_API_KEY")

    @property
    def virustotal_api_key(self) -> Optional[str]:
        """Get VirusTotal API key"""
        return os.getenv("VIRUSTOTAL_API_KEY")

    @property
    def shodan_api_key(self) -> Optional[str]:
        """Get Shodan API key"""
        return os.getenv("SHODAN_API_KEY")

    @property
    def epss_api_url(self) -> str:
        """Get EPSS API URL"""
        return os.getenv("EPSS_API_URL", "https://api.first.org/data/v1/epss")

    @property
    def cisa_kev_url(self) -> str:
        """Get CISA KEV feed URL"""
        return os.getenv(
            "CISA_KEV_URL",
            "https://www.cisa.gov/sites/default/files/feeds/known_exploited_vulnerabilities.json"
        )

    @property
    def threatfox_api_url(self) -> str:
        """Get ThreatFox API URL"""
        return os.getenv("THREATFOX_API_URL", "https://threatfox-api.abuse.ch/api/v1/")

    # ========================================================================
    # File System Configuration
    # ========================================================================

    @property
    def output_dir(self) -> Path:
        """Get output directory path"""
        return Path(os.getenv("OUTPUT_DIR", "data/output"))

    @property
    def input_dir(self) -> Path:
        """Get input directory path"""
        return Path(os.getenv("INPUT_DIR", "data/input"))

    @property
    def cache_dir(self) -> Path:
        """Get cache directory path"""
        return Path(os.getenv("CACHE_DIR", "data/cache"))

    @property
    def enable_cache(self) -> bool:
        """Check if caching is enabled"""
        return os.getenv("ENABLE_CACHE", "true").lower() == "true"

    @property
    def cache_ttl(self) -> int:
        """Get cache TTL in seconds"""
        return int(os.getenv("CACHE_TTL", "3600"))

    # ========================================================================
    # Logging Configuration
    # ========================================================================

    @property
    def log_level(self) -> str:
        """Get log level"""
        return os.getenv("LOG_LEVEL", "INFO").upper()

    @property
    def verbose_logging(self) -> bool:
        """Check if verbose logging is enabled"""
        return os.getenv("VERBOSE_LOGGING", "false").lower() == "true"

    @property
    def syslog_server(self) -> Optional[str]:
        """Get syslog server address"""
        return os.getenv("SYSLOG_SERVER")

    @property
    def syslog_port(self) -> int:
        """Get syslog port"""
        return int(os.getenv("SYSLOG_PORT", "514"))

    # ========================================================================
    # Security Configuration
    # ========================================================================

    @property
    def encrypt_cache(self) -> bool:
        """Check if cache encryption is enabled"""
        return os.getenv("ENCRYPT_CACHE", "false").lower() == "true"

    @property
    def cache_encryption_key(self) -> Optional[str]:
        """Get cache encryption key"""
        return os.getenv("CACHE_ENCRYPTION_KEY")

    @property
    def webhook_url(self) -> Optional[str]:
        """Get alert webhook URL"""
        return os.getenv("ALERT_WEBHOOK_URL")

    @property
    def webhook_secret(self) -> Optional[str]:
        """Get webhook secret for validation"""
        return os.getenv("WEBHOOK_SECRET")

    # ========================================================================
    # Organization Context
    # ========================================================================

    @property
    def org_name(self) -> str:
        """Get organization name"""
        return os.getenv("ORG_NAME", "Organization")

    @property
    def crown_jewels(self) -> List[str]:
        """Get list of crown jewel systems"""
        crown_jewels_str = os.getenv("CROWN_JEWELS", "")
        if crown_jewels_str:
            return [item.strip() for item in crown_jewels_str.split(",")]
        return ["Exchange", "Active Directory", "Financial Systems"]

    @property
    def asset_exposure(self) -> List[str]:
        """Get list of asset exposure types"""
        exposure_str = os.getenv("ASSET_EXPOSURE", "")
        if exposure_str:
            return [item.strip() for item in exposure_str.split(",")]
        return ["Internet-facing", "Internal Network", "Cloud Infrastructure"]

    @property
    def business_sectors(self) -> List[str]:
        """Get list of business sectors"""
        sectors_str = os.getenv("BUSINESS_SECTORS", "")
        if sectors_str:
            return [item.strip() for item in sectors_str.split(",")]
        return []

    # ========================================================================
    # Development Configuration
    # ========================================================================

    @property
    def dev_mode(self) -> bool:
        """Check if development mode is enabled"""
        return os.getenv("DEV_MODE", "false").lower() == "true"

    @property
    def use_test_data(self) -> bool:
        """Check if test data should be used"""
        return os.getenv("USE_TEST_DATA", "false").lower() == "true"

    @property
    def mock_apis(self) -> bool:
        """Check if API responses should be mocked"""
        return os.getenv("MOCK_APIS", "false").lower() == "true"

    # ========================================================================
    # Utility Methods
    # ========================================================================

    def ensure_directories(self) -> None:
        """Ensure all required directories exist"""
        directories = [
            self.output_dir,
            self.input_dir,
            self.cache_dir,
        ]

        for directory in directories:
            directory.mkdir(parents=True, exist_ok=True)
            self.logger.debug(f"Ensured directory exists: {directory}")

    def get_context_for_agents(self) -> Dict[str, Any]:
        """Get organization context for agent processing"""
        return {
            "org_name": self.org_name,
            "crown_jewels": self.crown_jewels,
            "asset_exposure": self.asset_exposure,
            "business_sectors": self.business_sectors,
        }

    def validate_api_access(self) -> Dict[str, bool]:
        """Validate which APIs are accessible"""
        api_status = {
            "anthropic": bool(self.anthropic_api_key),
            "openai": bool(self.openai_api_key),
            "nvd": bool(self.nvd_api_key),
            "virustotal": bool(self.virustotal_api_key),
            "shodan": bool(self.shodan_api_key),
        }

        self.logger.info("API access status:")
        for api, available in api_status.items():
            status = "✓" if available else "✗"
            self.logger.info(f"  {api}: {status}")

        return api_status

# Global configuration instance
config = EnvironmentConfig()