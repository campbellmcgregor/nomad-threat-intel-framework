#!/bin/bash
# NOMAD Threat Query Logging Hook
# Logs threat intelligence queries for audit trail

URL="$1"
STATUS="$2"
LOG_FILE="data/audit-log.json"
TIMESTAMP=$(date -u +"%Y-%m-%dT%H:%M:%SZ")

# Create data directory if it doesn't exist
mkdir -p "$(dirname "$LOG_FILE")"

# Extract domain from URL
DOMAIN=$(echo "$URL" | sed -E 's|^https?://([^/]+).*|\1|' | sed 's/^www\.//')

# Create log entry
LOG_ENTRY=$(cat <<EOF
{
  "timestamp": "$TIMESTAMP",
  "event": "threat_query",
  "domain": "$DOMAIN",
  "url": "$URL",
  "status": "$STATUS"
}
EOF
)

# Append to log file (create if doesn't exist)
if [ ! -f "$LOG_FILE" ]; then
    echo "[]" > "$LOG_FILE"
fi

# Use jq to append entry if available, otherwise use simple append
if command -v jq &> /dev/null; then
    TMP_FILE=$(mktemp)
    jq --argjson entry "$LOG_ENTRY" '. += [$entry]' "$LOG_FILE" > "$TMP_FILE" 2>/dev/null && mv "$TMP_FILE" "$LOG_FILE"
else
    # Fallback: simple line append (not valid JSON array but preserves data)
    echo "$LOG_ENTRY" >> "${LOG_FILE}.lines"
fi

echo "AUDIT_LOGGED=true"
echo "Query to $DOMAIN logged at $TIMESTAMP"
exit 0
