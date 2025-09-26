# Contributing to NOMAD v2.0

Thank you for your interest in contributing to NOMAD (Notable Object Monitoring And Analysis Director) v2.0! This project is designed to make threat intelligence accessible through natural conversation with Claude Code.

## 🛡️ Security First

NOMAD is a **defensive security tool only**. All contributions must align with this principle:

✅ **Acceptable contributions:**
- Threat intelligence feed improvements
- Agent behavior enhancements
- Documentation improvements
- Bug fixes and performance optimizations
- New defensive analysis features

❌ **Unacceptable contributions:**
- Offensive security tools or techniques
- Credential harvesting capabilities
- Any malicious functionality
- Tools that could be used to harm systems or individuals

## 🚀 Getting Started

### Prerequisites
- Claude Code (https://claude.ai/code)
- Basic understanding of threat intelligence concepts
- Familiarity with markdown for agent template editing

### Development Environment
```bash
git clone https://github.com/your-org/nomad-threat-intel-framework
cd nomad-threat-intel-framework
claude code
```

No additional setup required - NOMAD v2.0 runs entirely within Claude Code!

## 📋 Types of Contributions

### 1. Agent Template Improvements
- Edit markdown files in `agents/` directory
- Improve natural language understanding
- Enhance response quality and accuracy
- Add new analysis capabilities

### 2. Threat Feed Enhancements
- Add new legitimate threat intelligence sources
- Improve feed parsing logic
- Enhance data quality validation
- Update industry-specific templates

### 3. Configuration Templates
- Update `config/threat-sources-templates.json`
- Add new industry-specific feed packages
- Improve default user preferences

### 4. Documentation
- README improvements
- Agent behavior documentation
- Usage examples and tutorials
- Troubleshooting guides

## 🔧 Development Workflow

### Making Changes
1. **Fork** the repository
2. **Create a branch** for your feature: `git checkout -b feature/your-feature-name`
3. **Test locally** using Claude Code natural language queries
4. **Commit changes** with clear, descriptive messages
5. **Submit a Pull Request** with detailed description

### Testing Your Changes
Since NOMAD v2.0 uses conversational interfaces:
1. Launch Claude Code in your development environment
2. Test queries like:
   - "Show me latest threats"
   - "Add healthcare feeds"
   - "Configure my preferences"
3. Verify agent responses match expected behavior
4. Test edge cases and error handling

### Code Style
- **Agent Templates**: Use clear, professional language in markdown
- **Configuration Files**: Follow existing JSON structure and naming conventions
- **Documentation**: Use GitHub-flavored markdown with clear headings

## 📝 Pull Request Guidelines

### Before Submitting
- [ ] Test your changes thoroughly with Claude Code
- [ ] Update relevant documentation
- [ ] Ensure no sensitive data is included
- [ ] Verify all new threat sources are legitimate
- [ ] Check that agent behavior aligns with defensive security principles

### PR Description Template
```markdown
## Summary
Brief description of changes

## Type of Change
- [ ] Bug fix
- [ ] New feature
- [ ] Documentation update
- [ ] Configuration improvement
- [ ] Agent template enhancement

## Testing
Describe how you tested the changes using Claude Code queries

## Security Considerations
Confirm this change maintains defensive security focus
```

## 🎯 Priority Areas

We especially welcome contributions in these areas:

1. **Industry-Specific Templates**
   - Healthcare, Financial, Manufacturing, Government
   - Sector-specific threat feeds and crown jewels

2. **Agent Intelligence Improvements**
   - Better natural language understanding
   - Enhanced threat prioritization logic
   - Improved briefing generation

3. **Feed Quality Enhancements**
   - Better source reliability detection
   - Enhanced parsing for complex feeds
   - Improved deduplication logic

4. **User Experience**
   - More intuitive natural language patterns
   - Better error messages and guidance
   - Improved onboarding experience

## 🐛 Reporting Issues

### Security Vulnerabilities
**DO NOT** open public issues for security vulnerabilities. Instead, please email the security contact listed in [SECURITY.md](SECURITY.md).

### General Issues
Use our GitHub issue templates:
- **Bug Report**: For unexpected behavior
- **Feature Request**: For new functionality ideas
- **Agent Improvement**: For conversational intelligence enhancements
- **Feed Request**: For new threat intelligence sources

Include:
- Clear description of the issue
- Steps to reproduce (for bugs)
- Expected vs actual behavior
- Relevant Claude Code queries used

## 💡 Feature Requests

When requesting new features:
1. **Check existing issues** to avoid duplicates
2. **Describe the use case** - who benefits and how?
3. **Consider defensive security** - does this align with our principles?
4. **Suggest implementation** if you have ideas
5. **Provide examples** of expected interactions

## 📚 Documentation Style Guide

- Use clear, concise language
- Include practical examples
- Test all code snippets and queries
- Use proper markdown formatting
- Link to relevant resources

## 🤝 Community Guidelines

- **Be respectful** and professional
- **Stay focused** on defensive security applications
- **Help others** by sharing knowledge and examples
- **Follow security best practices** in all contributions
- **Report issues** constructively with helpful detail

## 📄 License

By contributing, you agree that your contributions will be licensed under the GNU Affero General Public License v3.0 with the same defensive security restrictions as the main project.

## 🆘 Getting Help

- **GitHub Discussions**: General questions and ideas
- **GitHub Issues**: Specific bugs or feature requests
- **Documentation**: Check README.md and agent templates
- **Examples**: Look at existing agent templates and configurations

## 🙏 Recognition

Contributors will be recognized in:
- Release notes for significant contributions
- CONTRIBUTORS.md file (maintained separately)
- Documentation acknowledgments for major improvements

Thank you for helping make threat intelligence more accessible and actionable for security teams everywhere! 🛡️

---

**Remember**: NOMAD v2.0 is designed to help security professionals defend their organizations. All contributions should support this mission while maintaining the highest ethical standards.