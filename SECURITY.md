# Security Policy

## Purpose Statement

NOMAD Threat Intelligence Framework is designed exclusively for **defensive security purposes**. This tool is intended to help security teams protect their organizations by processing and prioritizing threat intelligence.

## Responsible Use

This framework must be used in accordance with:
- All applicable laws and regulations
- Organizational security policies
- Ethical security practices
- The project's GNU AGPL-3.0 license

**Prohibited uses include:**
- Offensive security operations
- Unauthorized system access
- Distribution of malware or exploits
- Any illegal activities

## Supported Versions

We release patches for security vulnerabilities in the following versions:

| Version | Supported          |
| ------- | ------------------ |
| 1.x.x   | :white_check_mark: |
| < 1.0   | :x:                |

## Reporting a Vulnerability

### Do NOT Create Public Issues for Security Vulnerabilities

If you discover a security vulnerability in NOMAD, please follow responsible disclosure practices:

1. **Email privately**: Send details to `security@nomad-framework.example`
2. **Encrypt if possible**: Use PGP encryption when available
3. **Include details**:
   - Description of the vulnerability
   - Steps to reproduce
   - Potential impact assessment
   - Suggested remediation (if any)
   - Your contact information

### What to Expect

- **Acknowledgment**: Within 48 hours
- **Initial Assessment**: Within 1 week
- **Status Updates**: Every 2 weeks until resolved
- **Credit**: Security researchers will be credited (unless you prefer to remain anonymous)

### Bug Bounty

We currently do not offer a bug bounty program, but we deeply appreciate responsible disclosure and will acknowledge security researchers in our releases.

## Security Best Practices

When deploying NOMAD:

### API Keys and Secrets
- Never commit API keys to the repository
- Use environment variables or secure vaults
- Rotate credentials regularly
- Use least-privilege access principles

### Network Security
- Deploy behind appropriate firewalls
- Use TLS/HTTPS for all communications
- Implement rate limiting
- Monitor for anomalous activity

### Data Protection
- Encrypt sensitive data at rest
- Sanitize all inputs
- Implement proper access controls
- Maintain audit logs

### Updates and Patches
- Keep all dependencies updated
- Monitor security advisories
- Apply patches promptly
- Test updates in non-production first

## Security Features

NOMAD includes several security features:

- **Input validation**: All agent inputs are validated against schemas
- **Rate limiting**: API calls are rate-limited to prevent abuse
- **Audit logging**: All routing decisions are logged
- **Evidence chain**: Maintains custody chain for threat artifacts
- **Admiralty grading**: Credibility assessment for all sources

## Compliance

This framework can support compliance with:
- GDPR (data protection)
- SOC 2 (security controls)
- ISO 27001 (information security)
- NIST Cybersecurity Framework

Users are responsible for ensuring their specific implementation meets their compliance requirements.

## Contact

For security concerns, contact: `security@nomad-framework.example`

For general questions, please use GitHub Issues or Discussions.

## Acknowledgments

We thank the security community for their responsible disclosure practices and contributions to making NOMAD more secure.