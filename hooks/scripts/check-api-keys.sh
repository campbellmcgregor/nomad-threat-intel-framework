#!/bin/bash
# NOMAD API Key Check Hook
# Checks if required API keys are configured for premium sources

URL="$1"
CONFIG_FILE="config/user-preferences.json"

# Extract domain from URL
DOMAIN=$(echo "$URL" | sed -E 's|^https?://([^/]+).*|\1|' | sed 's/^www\.//')

# Get required API key for domain (bash 3.2 compatible - no associative arrays)
get_required_key() {
    local domain="$1"
    case "$domain" in
        r.jina.ai|s.jina.ai)
            echo "jina_api_key" ;;
        api.first.org)
            echo "first_api_key" ;;
        services.nvd.nist.gov)
            echo "nvd_api_key" ;;
        *)
            echo "" ;;
    esac
}

# Check if this domain requires an API key
REQUIRED_KEY=$(get_required_key "$DOMAIN")

# If no API key required, exit
if [ -z "$REQUIRED_KEY" ]; then
    exit 0
fi

# Check if config exists
if [ ! -f "$CONFIG_FILE" ]; then
    echo "API_KEY_STATUS=missing_config"
    echo "Configuration file not found. Run /setup to configure NOMAD."
    exit 0
fi

# Check if the required key is set
KEY_VALUE=$(jq -r ".verification.$REQUIRED_KEY // .api_keys.$REQUIRED_KEY // \"\"" "$CONFIG_FILE" 2>/dev/null)

if [ -z "$KEY_VALUE" ] || [ "$KEY_VALUE" = "null" ]; then
    echo "API_KEY_STATUS=not_configured"
    echo "API key '$REQUIRED_KEY' is required for $DOMAIN but not configured."
    echo "Run /setup-verification to configure API keys."

    # Special handling for optional keys
    if [ "$REQUIRED_KEY" = "nvd_api_key" ]; then
        echo "Note: NVD API works without a key but with rate limits."
    fi
    exit 0
fi

echo "API_KEY_STATUS=configured"
echo "API key '$REQUIRED_KEY' is configured for $DOMAIN."
exit 0
