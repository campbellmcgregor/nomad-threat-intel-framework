#!/bin/bash
# NOMAD Setup Status Check Hook
# Checks if NOMAD is configured before operational queries

PROMPT="$1"
CONFIG_FILE="config/user-preferences.json"

# Keywords that indicate operational queries (require setup)
OPERATIONAL_KEYWORDS="threats|critical|briefing|cve|crown-jewel|trending|executive|technical|weekly|refresh"

# Keywords that are configuration-related (don't require setup)
CONFIG_KEYWORDS="setup|configure|help|status|import|add-feeds"

# Check if this is an operational query
IS_OPERATIONAL=$(echo "$PROMPT" | grep -iE "$OPERATIONAL_KEYWORDS" | head -1)
IS_CONFIG=$(echo "$PROMPT" | grep -iE "$CONFIG_KEYWORDS" | head -1)

# If it's a config query, skip the check
if [ -n "$IS_CONFIG" ]; then
    exit 0
fi

# If it's not an operational query, skip
if [ -z "$IS_OPERATIONAL" ]; then
    exit 0
fi

# Check if config exists and has minimum required settings
if [ ! -f "$CONFIG_FILE" ]; then
    echo "SETUP_STATUS=required"
    echo "NOMAD setup is required before using threat intelligence features."
    echo "Run /setup to configure your organization profile."
    exit 0
fi

# Check for minimum configuration
ORG_NAME=$(jq -r '.organization.name // ""' "$CONFIG_FILE" 2>/dev/null)
CROWN_JEWELS_COUNT=$(jq -r '.crown_jewels | length // 0' "$CONFIG_FILE" 2>/dev/null)

if [ -z "$ORG_NAME" ] || [ "$ORG_NAME" = "null" ]; then
    echo "SETUP_STATUS=incomplete"
    echo "Organization name not configured. Run /setup to complete configuration."
    exit 0
fi

if [ "$CROWN_JEWELS_COUNT" -eq 0 ]; then
    echo "SETUP_STATUS=warning"
    echo "No crown jewels configured. Consider running /add-crown-jewel to identify critical systems."
    exit 0
fi

echo "SETUP_STATUS=complete"
exit 0
