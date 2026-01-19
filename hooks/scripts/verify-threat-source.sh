#!/bin/bash
# NOMAD Threat Source Verification Hook
# Verifies WebFetch targets are legitimate threat intelligence sources

URL="$1"

# List of approved threat intelligence domains
APPROVED_DOMAINS=(
    # Government/CERT Sources
    "nvd.nist.gov"
    "cisa.gov"
    "us-cert.cisa.gov"
    "cert.org"
    "ncsc.gov.uk"
    "cyber.gc.ca"
    "auscert.org.au"
    "cert.europa.eu"

    # Vendor Security Advisories
    "msrc.microsoft.com"
    "security.microsoft.com"
    "support.apple.com"
    "security.googleblog.com"
    "chromereleases.googleblog.com"
    "advisories.cisco.com"
    "tools.cisco.com"
    "fortiguard.com"
    "paloaltonetworks.com"
    "access.redhat.com"
    "ubuntu.com/security"
    "security.debian.org"
    "aws.amazon.com/security"
    "cloud.google.com/security"
    "azure.microsoft.com/security"
    "github.com/advisories"
    "security.snyk.io"
    "oracle.com/security-alerts"
    "vmware.com/security"
    "sap.com/security"
    "atlassian.com/security"
    "salesforce.com/security"
    "zoom.us/security"

    # Threat Intelligence Feeds
    "feeds.feedburner.com"
    "bleepingcomputer.com"
    "thehackernews.com"
    "krebsonsecurity.com"
    "darkreading.com"
    "threatpost.com"
    "securityweek.com"
    "therecord.media"
    "cyberscoop.com"
    "arstechnica.com"
    "zdnet.com"
    "wired.com"

    # Research/CVE Sources
    "cvedetails.com"
    "exploit-db.com"
    "vulndb.cyberriskanalytics.com"
    "first.org"
    "mitre.org"
    "attack.mitre.org"

    # EPSS/Scoring
    "api.first.org"
    "epss.cyentia.com"

    # Verification Services
    "r.jina.ai"
    "s.jina.ai"
)

# Extract domain from URL
DOMAIN=$(echo "$URL" | sed -E 's|^https?://([^/]+).*|\1|' | sed 's/^www\.//')

# Check if domain is approved
APPROVED=false
for APPROVED_DOMAIN in "${APPROVED_DOMAINS[@]}"; do
    if [[ "$DOMAIN" == *"$APPROVED_DOMAIN"* ]] || [[ "$APPROVED_DOMAIN" == *"$DOMAIN"* ]]; then
        APPROVED=true
        break
    fi
done

if [ "$APPROVED" = true ]; then
    echo "SOURCE_VERIFIED=approved"
    echo "Domain: $DOMAIN"
    exit 0
else
    echo "SOURCE_VERIFIED=unknown"
    echo "Domain '$DOMAIN' is not in the approved threat intelligence sources list."
    echo "Proceeding with caution. Consider adding to approved sources if legitimate."
    exit 0
fi
