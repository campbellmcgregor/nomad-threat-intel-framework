#!/bin/bash
# NOMAD API Key Check Hook
# Checks if required API keys are configured for premium sources

URL="$1"
CONFIG_FILE="config/user-preferences.json"

# Extract domain from URL
DOMAIN=$(echo "$URL" | sed -E 's|^https?://([^/]+).*|\1|' | sed 's/^www\.//')

# Domains that require API keys
declare -A API_KEY_DOMAINS
API_KEY_DOMAINS=(
    ["r.jina.ai"]="jina_api_key"
    ["s.jina.ai"]="jina_api_key"
    ["api.first.org"]="first_api_key"
    ["services.nvd.nist.gov"]="nvd_api_key"
)

# Check if this domain requires an API key
REQUIRED_KEY=""
for KEY_DOMAIN in "${!API_KEY_DOMAINS[@]}"; do
    if [[ "$DOMAIN" == *"$KEY_DOMAIN"* ]]; then
        REQUIRED_KEY="${API_KEY_DOMAINS[$KEY_DOMAIN]}"
        break
    fi
done

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
