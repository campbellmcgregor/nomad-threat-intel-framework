#!/bin/bash
# NOMAD Cache Verification Hook
# Verifies threat cache was properly saved before session end

CACHE_FILE="data/threats-cache.json"
METRICS_FILE="data/feed-quality-metrics.json"

# OS-aware file modification time (detect once, use efficiently)
get_mtime() {
    if [[ "$OSTYPE" == "darwin"* ]]; then
        stat -f %m "$1" 2>/dev/null
    else
        stat -c %Y "$1" 2>/dev/null
    fi
}

ISSUES=""

# Check threats cache
if [ -f "$CACHE_FILE" ]; then
    # Verify it's valid JSON
    if ! jq empty "$CACHE_FILE" 2>/dev/null; then
        ISSUES="$ISSUES\n- Threats cache is corrupted (invalid JSON)"
    else
        CACHE_SIZE=$(jq '. | length' "$CACHE_FILE" 2>/dev/null)
        CACHE_AGE=$(( ($(date +%s) - $(get_mtime "$CACHE_FILE")) / 60 ))
        echo "Threats cache: $CACHE_SIZE items, modified ${CACHE_AGE}m ago"
    fi
else
    echo "Threats cache: Not present (will be created on first /threats or /refresh)"
fi

# Check metrics file
if [ -f "$METRICS_FILE" ]; then
    if ! jq empty "$METRICS_FILE" 2>/dev/null; then
        ISSUES="$ISSUES\n- Feed metrics file is corrupted (invalid JSON)"
    else
        echo "Feed metrics: Present and valid"
    fi
else
    echo "Feed metrics: Not present (will be created on first feed collection)"
fi

# Check audit log
AUDIT_FILE="data/audit-log.json"
if [ -f "$AUDIT_FILE" ]; then
    if jq empty "$AUDIT_FILE" 2>/dev/null; then
        AUDIT_COUNT=$(jq '. | length' "$AUDIT_FILE" 2>/dev/null)
        echo "Audit log: $AUDIT_COUNT entries"
    fi
fi

# Report issues
if [ -n "$ISSUES" ]; then
    echo "CACHE_STATUS=issues"
    echo -e "Issues found:$ISSUES"
    exit 0
fi

echo "CACHE_STATUS=healthy"
echo "All data files verified."
exit 0
