#!/bin/bash
# NOMAD Session Start Hook
# Loads configuration and checks cache freshness

CONFIG_FILE="config/user-preferences.json"
CACHE_FILE="data/threats-cache.json"
METRICS_FILE="data/feed-quality-metrics.json"

# Check if config exists
if [ ! -f "$CONFIG_FILE" ]; then
    echo "NOMAD_STATUS=unconfigured"
    echo "Run /setup to configure NOMAD for your organization."
    exit 0
fi

# Load organization name
ORG_NAME=$(jq -r '.organization.name // "Not configured"' "$CONFIG_FILE" 2>/dev/null)
INDUSTRY=$(jq -r '.organization.industry // "Not set"' "$CONFIG_FILE" 2>/dev/null)
CROWN_JEWELS_COUNT=$(jq -r '.crown_jewels | length // 0' "$CONFIG_FILE" 2>/dev/null)

# Check cache freshness
if [ -f "$CACHE_FILE" ]; then
    CACHE_AGE_HOURS=$(( ($(date +%s) - $(stat -f %m "$CACHE_FILE" 2>/dev/null || stat -c %Y "$CACHE_FILE" 2>/dev/null)) / 3600 ))
    THREAT_COUNT=$(jq -r '. | length // 0' "$CACHE_FILE" 2>/dev/null)

    if [ "$CACHE_AGE_HOURS" -gt 4 ]; then
        CACHE_STATUS="stale"
    else
        CACHE_STATUS="fresh"
    fi
else
    CACHE_AGE_HOURS="N/A"
    THREAT_COUNT=0
    CACHE_STATUS="empty"
fi

# Check verification method
VERIFICATION_METHOD=$(jq -r '.verification.method // "structured"' "$CONFIG_FILE" 2>/dev/null)
JINA_KEY_SET=$(jq -r 'if .verification.jina_api_key and .verification.jina_api_key != "" then "configured" else "not_configured" end' "$CONFIG_FILE" 2>/dev/null)

# Output context
echo "NOMAD_STATUS=configured"
echo "Organization: $ORG_NAME"
echo "Industry: $INDUSTRY"
echo "Crown Jewels: $CROWN_JEWELS_COUNT systems"
echo "Cache Status: $CACHE_STATUS ($THREAT_COUNT threats, ${CACHE_AGE_HOURS}h old)"
echo "Verification: $VERIFICATION_METHOD (Jina: $JINA_KEY_SET)"

exit 0
