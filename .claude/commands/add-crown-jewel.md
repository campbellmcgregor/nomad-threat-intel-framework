---
name: add-crown-jewel
description: Add a new crown jewel system to your organization profile
usage: /add-crown-jewel [system-name]
---

You are executing the `/add-crown-jewel` command for NOMAD v2.0. This command adds a new crown jewel system to your organization's profile, enabling personalized threat intelligence for your most critical assets.

## Command Parameters

- `$1`: Crown jewel system name (e.g., "Customer Database", "Payment Gateway")
- If no parameter: Show guided crown jewel addition wizard

## Command Execution

1. **Parse System Name**: If provided, use as crown jewel name
2. **Load Current Config**: Read `config/user-preferences.json`
3. **Crown Jewel Assessment**: If no name provided, guide user through identification
4. **Add to Configuration**: Update crown jewel list and save
5. **Impact Analysis**: Show how this affects threat prioritization

## Response Format

### Guided Crown Jewel Wizard (No Parameter):
```
💎 CROWN JEWEL IDENTIFICATION WIZARD

Crown jewels are your organization's most critical systems - the ones that would cause significant business impact if compromised.

CURRENT CROWN JEWELS ([X] systems):
• [Existing System 1]: [Description]
• [Existing System 2]: [Description]

COMMON CROWN JEWEL CATEGORIES:

🏦 Financial Systems:
• Core Banking Platform
• Payment Processing Gateway
• Trading Systems
• Billing/Accounting Systems

💾 Data Systems:
• Customer Database
• Financial Records
• Intellectual Property Repository
• Employee Records

🌐 Infrastructure:
• Authentication Systems
• Network Management
• Cloud Control Plane
• Backup Systems

🔐 Security Systems:
• SIEM Platform
• Identity Management
• Security Operations Center
• Incident Response Tools

📱 Customer-Facing:
• Mobile Banking App
• E-commerce Platform
• Customer Portal
• API Gateway

What critical system would you like to add as a crown jewel?
Example: "Customer Database" or "Mobile Banking Platform"
```

### Crown Jewel Addition Confirmation:
```
✅ CROWN JEWEL ADDED: [System Name]

SYSTEM PROFILE:
• Name: [System Name]
• Category: [Auto-detected category]
• Threat Focus: [Relevant threat types]
• Priority Level: [Critical/High based on system type]

IMPACT ON THREAT INTELLIGENCE:
• NOMAD will now prioritize threats affecting [System Name]
• Alerts will highlight vulnerabilities in related technologies
• Industry-specific threats targeting similar systems will be elevated
• Crown jewel correlation will appear in threat briefings

CURRENT CROWN JEWEL PORTFOLIO ([X] systems):
• [System 1]: [Category]
• [System 2]: [Category]
• [New System]: [Category] ← NEW

RECOMMENDATIONS:
• Related threats will now appear in `/threats` briefings
• Use `/crown-jewel [system-name]` to see targeted threats
• Consider adding complementary systems for complete coverage

Crown jewel successfully added to your threat intelligence profile.
```

### System Already Exists:
```
⚠️ CROWN JEWEL ALREADY EXISTS

The system "[System Name]" is already in your crown jewel portfolio.

CURRENT ENTRY:
• Name: [Existing Name]
• Added: [Date]
• Threat Matches: [X] recent threats

OPTIONS:
1. Update description: /configure crown-jewels update "[name]" "[new-description]"
2. Remove system: /configure crown-jewels remove "[name]"
3. View threats: /crown-jewel "[name]"

No changes made to your configuration.
```

## Crown Jewel Intelligence Enhancement

Adding crown jewels enables:
- **Personalized Prioritization**: Threats affecting your systems rank higher
- **Technology Correlation**: Vulnerabilities in your tech stack highlighted
- **Industry Context**: Sector-specific threats targeting similar systems
- **Impact Assessment**: Business context for threat severity
- **Focused Alerting**: Critical alerts prioritize crown jewel risks

## Crown Jewel Categories

NOMAD automatically categorizes crown jewels for enhanced intelligence:
- **Financial**: Banking, payment, trading systems
- **Data**: Databases, repositories, analytics platforms
- **Infrastructure**: Networks, cloud, authentication
- **Customer**: Portals, mobile apps, e-commerce
- **Operations**: Manufacturing, logistics, supply chain
- **Security**: SIEM, SOC tools, incident response

Execute this command now to enhance threat intelligence with organization-specific crown jewel identification.