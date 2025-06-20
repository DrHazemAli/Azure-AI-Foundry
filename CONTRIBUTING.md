# Contributing to Azure AI Foundry Zero-to-Hero Course

Thank you for your interest in contributing to the Azure AI Foundry Zero-to-Hero Course! This document provides guidelines and information for contributors who want to help improve this educational resource.

## 🤝 How to Contribute

We welcome contributions from the community! Whether you're fixing a typo, adding new content, improving code samples, or suggesting new features, your contributions help make this course better for everyone.

### Types of Contributions We Welcome

- **Content Improvements**: Fixing typos, clarifying explanations, updating outdated information
- **Code Samples**: Adding new examples, improving existing code, fixing bugs
- **New Lessons**: Creating additional educational content
- **Documentation**: Improving README files, adding setup instructions
- **Translations**: Translating content to other languages
- **Bug Reports**: Reporting issues with content or code
- **Feature Requests**: Suggesting new topics or improvements

## 📋 Before You Start

### Prerequisites

- Basic understanding of Azure AI Foundry concepts
- Familiarity with Markdown for documentation
- Knowledge of at least one programming language (C#, Python, JavaScript)
- Git and GitHub experience

### Development Environment Setup

1. **Fork the repository** on GitHub
2. **Clone your fork** locally:
   ```bash
   git clone https://github.com/DrHazemAli/Azure-AI-Foundry.git
   cd Azure-AI-Foundry
   ```
3. **Create a branch** for your changes:
   ```bash
   git checkout -b feature/your-feature-name
   ```

## 📝 Contribution Guidelines

### Content Standards

#### Documentation (Markdown Files)

- **Use clear, concise language** that's accessible to beginners
- **Follow the existing structure** and formatting patterns
- **Include practical examples** where appropriate
- **Use proper Markdown syntax** for headers, lists, code blocks, etc.
- **Keep line length** under 100 characters where possible
- **Use descriptive commit messages** (see below)

#### Code Samples

- **Follow language-specific best practices** and conventions
- **Include proper error handling** and logging
- **Add comments** explaining complex logic
- **Ensure code is production-ready** with proper security practices
- **Test your code** before submitting
- **Include setup instructions** in README files

#### File Naming Conventions

- **Markdown files**: Use kebab-case (e.g., `01-introduction-to-ai-foundry.md`)
- **Code files**: Follow language conventions (e.g., `Program.cs`, `main.py`, `index.js`)
- **Directories**: Use kebab-case for module directories

### Content Structure

#### Lesson Files
Each lesson should follow this structure:

```markdown
# Lesson Title

## Overview
Brief description of what this lesson covers.

## Prerequisites
What learners need to know before starting.

## Learning Objectives
What learners will be able to do after completing this lesson.

## Main Content
The main educational content, organized with clear headings.

## Hands-On Exercise
Practical exercises for learners to complete.

## Summary
Key takeaways from the lesson.

## Next Steps
What to learn next or additional resources.
```

#### Code Sample Structure
Each code sample should include:

- **README.md**: Setup instructions and usage guide
- **Source code**: Well-commented, production-ready code
- **Configuration files**: Dependencies, settings, etc.
- **Documentation**: Inline comments and external documentation

## 🔄 Contribution Process

### 1. Issue Reporting

Before making changes, check if there's already an issue for your contribution:

1. **Search existing issues** to avoid duplicates
2. **Create a new issue** if none exists:
   - Use descriptive titles
   - Provide clear descriptions
   - Include reproduction steps for bugs
   - Tag appropriately (bug, enhancement, documentation, etc.)

### 2. Making Changes

1. **Create a feature branch** from the main branch
2. **Make your changes** following the guidelines above
3. **Test your changes** thoroughly
4. **Update documentation** if needed
5. **Commit your changes** with clear messages

### 3. Commit Message Guidelines

Use conventional commit format:

```
type(scope): description

[optional body]

[optional footer]
```

**Types:**
- `feat`: New feature
- `fix`: Bug fix
- `docs`: Documentation changes
- `style`: Code style changes (formatting, etc.)
- `refactor`: Code refactoring
- `test`: Adding or updating tests
- `chore`: Maintenance tasks

**Examples:**
```
feat(module02): add new authentication example
fix(samples): correct error handling in Python code
docs(readme): update installation instructions
style(module01): fix markdown formatting
```

### 4. Pull Request Process

1. **Push your changes** to your fork
2. **Create a pull request** with:
   - Clear title describing the change
   - Detailed description of what was changed and why
   - Reference to related issues
   - Screenshots for UI changes (if applicable)

3. **Wait for review** from maintainers
4. **Address feedback** and make requested changes
5. **Maintainers will merge** when ready

## 🧪 Testing Guidelines

### Code Testing

- **Test all code samples** before submitting
- **Verify setup instructions** work as described
- **Check for syntax errors** and typos
- **Ensure compatibility** with specified versions

### Content Testing

- **Review for accuracy** and completeness
- **Check all links** work correctly
- **Verify formatting** renders properly
- **Test on different devices** if UI changes

## 📚 Content Guidelines

### Educational Standards

- **Start with basics** and build complexity gradually
- **Use real-world examples** and scenarios
- **Include hands-on exercises** for practical learning
- **Provide clear learning objectives** for each lesson
- **Use consistent terminology** throughout the course

### Technical Accuracy

- **Verify all technical information** against official documentation
- **Keep content up-to-date** with latest Azure AI Foundry features
- **Test all code examples** with current SDK versions
- **Include version information** for dependencies

### Accessibility

- **Use clear, simple language** avoiding jargon when possible
- **Provide alternative text** for images and diagrams
- **Use proper heading hierarchy** for screen readers
- **Ensure sufficient color contrast** in any visual elements

## 🏗️ Development Guidelines

### Code Quality

- **Follow language-specific style guides**
- **Use meaningful variable and function names**
- **Include proper error handling**
- **Add appropriate logging and debugging**
- **Write self-documenting code**

### Security Best Practices

- **Never include sensitive information** (API keys, passwords, etc.)
- **Use environment variables** for configuration
- **Follow Azure security best practices**
- **Include security considerations** in documentation

### Performance Considerations

- **Optimize code for efficiency** where appropriate
- **Include performance tips** in documentation
- **Consider resource usage** in examples
- **Provide scaling guidance** for production use

## 🐛 Bug Reports

When reporting bugs, please include:

1. **Clear description** of the problem
2. **Steps to reproduce** the issue
3. **Expected vs actual behavior**
4. **Environment details** (OS, language versions, etc.)
5. **Screenshots or logs** if applicable
6. **Possible solutions** if you have ideas

## 💡 Feature Requests

When suggesting new features:

1. **Describe the feature** clearly
2. **Explain the benefit** to learners
3. **Provide use cases** or examples
4. **Consider implementation** complexity
5. **Check if similar features** already exist

## 📖 Documentation Standards

### Markdown Guidelines

- **Use proper heading hierarchy** (H1 → H2 → H3)
- **Include table of contents** for long documents
- **Use code blocks** with language specification
- **Include links** to related content
- **Add images** where helpful (with alt text)

### Code Documentation

- **Include README files** for all code samples
- **Add inline comments** for complex logic
- **Document function parameters** and return values
- **Provide usage examples**
- **Include troubleshooting sections**

## 🤝 Code of Conduct

### Our Standards

We are committed to providing a welcoming and inclusive environment for all contributors. By participating in this project, you agree to:

- **Be respectful** and inclusive of others
- **Use welcoming and inclusive language**
- **Be collaborative** and constructive
- **Focus on what is best for the community**
- **Show empathy** towards other community members

### Unacceptable Behavior

The following behaviors are considered unacceptable:

- **Harassment** or discrimination
- **Trolling, insulting, or derogatory comments**
- **Personal or political attacks**
- **Publishing others' private information**
- **Other conduct** that could reasonably be considered inappropriate

## 📞 Getting Help

### Questions and Support

- **GitHub Issues**: For bug reports and feature requests
- **GitHub Discussions**: For questions and general discussion
- **Documentation**: Check existing documentation first
- **Community**: Engage with other contributors

### Maintainer Contact

For urgent issues or questions about contribution guidelines, you can reach the maintainers through:

- **GitHub Issues**: Tag with `@maintainers`
- **Email**: [Maintainer email if available]
- **Discussions**: Create a new discussion thread

## 🏆 Recognition

### Contributor Recognition

We appreciate all contributions! Contributors will be recognized through:

- **GitHub Contributors** page
- **Release notes** for significant contributions
- **Special thanks** in documentation
- **Contributor badges** for regular contributors

### Becoming a Maintainer

Regular contributors who demonstrate:

- **Consistent quality** contributions
- **Good communication** skills
- **Community engagement**
- **Technical expertise**

May be invited to become maintainers with additional repository permissions.

## 📄 License

By contributing to this project, you agree that your contributions will be licensed under the same license as the project (MIT License).

## 🙏 Acknowledgments

Thank you to all contributors who help make this course better for the Azure AI Foundry community!

---

**Last Updated**: June 2025

For questions about contributing, please open an issue or discussion on GitHub. 