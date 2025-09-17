# Contributing to NOMAD Threat Intelligence Framework

Thank you for your interest in contributing to the NOMAD Threat Intelligence Framework! We welcome contributions from the security community to help improve and expand this defensive security tool.

## Code of Conduct

By participating in this project, you agree to abide by our Code of Conduct:

- **Be Respectful**: Treat all contributors with respect and professionalism
- **Be Constructive**: Provide helpful feedback and suggestions
- **Be Ethical**: This framework is for defensive security only
- **Be Collaborative**: Work together to improve the framework

## How to Contribute

### Reporting Issues

1. **Check existing issues** first to avoid duplicates
2. **Use issue templates** when available
3. **Provide detailed information**:
   - Clear description of the issue
   - Steps to reproduce
   - Expected vs actual behavior
   - Environment details (OS, Python version, etc.)
   - Relevant logs or error messages

### Security Vulnerabilities

**DO NOT** open public issues for security vulnerabilities. Instead:

1. Email the maintainers privately at: security@nomad-framework.example
2. Include:
   - Description of the vulnerability
   - Steps to reproduce
   - Potential impact
   - Suggested fix (if available)

### Feature Requests

1. Open an issue with the `enhancement` label
2. Describe the feature and its use case
3. Explain how it benefits defensive security operations
4. Consider how it fits with existing architecture

### Pull Requests

#### Before You Start

1. **Fork the repository** and create a new branch
2. **Discuss major changes** first by opening an issue
3. **Follow the existing code style** and conventions
4. **Ensure defensive use only** - no offensive capabilities

#### Development Process

1. **Set up your environment**:
   ```bash
   git clone https://github.com/yourusername/nomad-threat-intel-framework.git
   cd nomad-threat-intel-framework
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   pip install -r requirements.txt
   pip install -r requirements-dev.txt  # If available
   ```

2. **Create a feature branch**:
   ```bash
   git checkout -b feature/your-feature-name
   ```

3. **Make your changes**:
   - Write clean, documented code
   - Add tests for new functionality
   - Update documentation as needed
   - Follow Python PEP 8 style guide

4. **Test your changes**:
   ```bash
   # Run tests
   pytest tests/

   # Check code style
   flake8 src/

   # Type checking (if applicable)
   mypy src/
   ```

5. **Commit your changes**:
   - Use clear, descriptive commit messages
   - Follow conventional commits format:
     - `feat:` New feature
     - `fix:` Bug fix
     - `docs:` Documentation changes
     - `style:` Code style changes
     - `refactor:` Code refactoring
     - `test:` Test additions/changes
     - `chore:` Maintenance tasks

6. **Push and create PR**:
   ```bash
   git push origin feature/your-feature-name
   ```
   - Open a pull request against the `main` branch
   - Fill out the PR template completely
   - Link related issues

#### Pull Request Guidelines

- **One feature per PR** - Keep PRs focused
- **Include tests** - All new code should have tests
- **Update documentation** - Keep docs in sync with code
- **Pass CI checks** - Ensure all tests and linters pass
- **Be responsive** - Address review feedback promptly

### Contributing Agent Prompts

When contributing new agent prompts:

1. Follow the existing prompt structure
2. Include clear input/output schemas
3. Document the agent's purpose and workflow position
4. Test with various input scenarios
5. Ensure Admiralty grading consistency

### Documentation Contributions

- Fix typos or clarify existing documentation
- Add examples and use cases
- Improve installation or deployment guides
- Translate documentation (coordinate first)

## Development Guidelines

### Code Style

- **Python**: Follow PEP 8
- **Markdown**: Use consistent formatting
- **YAML/JSON**: Maintain consistent indentation

### Testing

- Write unit tests for new functions
- Include integration tests for agent workflows
- Test edge cases and error conditions
- Maintain or improve test coverage

### Security Considerations

All contributions must:
- Be designed for **defensive security only**
- Not include any offensive capabilities
- Follow secure coding practices
- Not expose sensitive information
- Validate all inputs
- Handle errors gracefully

### Agent Development

When creating or modifying agents:

1. **Maintain Single Responsibility**: Each agent should have one clear purpose
2. **Use Standard Schemas**: Follow existing data format conventions
3. **Handle Edge Cases**: Account for missing or malformed data
4. **Document Thoroughly**: Include usage examples and expected outputs
5. **Test Extensively**: Verify with real-world threat data

## Review Process

1. **Maintainer Review**: All PRs are reviewed by maintainers
2. **Community Feedback**: Larger changes may have community review period
3. **Testing**: PRs must pass all automated tests
4. **Security Review**: Security-sensitive changes get additional review
5. **Documentation**: Changes must include appropriate documentation

## Recognition

Contributors will be recognized in:
- The project's contributors list
- Release notes for significant contributions
- Annual contributor acknowledgments

## Questions?

- Open a discussion in GitHub Discussions
- Join our community chat (if available)
- Review existing documentation and issues

## License

By contributing, you agree that your contributions will be licensed under the project's GNU AGPL-3.0 license.

Thank you for helping make NOMAD a better tool for the defensive security community!