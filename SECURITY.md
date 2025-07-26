# Security Guidelines for ChatDev

## Overview

This document outlines security considerations when using ChatDev.

## Security Improvements Made

### 1. Command Injection Prevention
- **Fixed**: Replaced `shell=True` with secure subprocess calls using argument lists
- **Location**: `chatdev/chat_env.py` in `fix_module_not_found_error()` and `exist_bugs()`
- **Impact**: Prevents arbitrary command execution through malicious input

### 2. Input Validation
- **Added**: Module name validation using regex patterns
- **Added**: Project name validation for file system safety
- **Added**: Company name validation for configuration loading
- **Location**: `run.py`, `chatdev/chat_env.py`

### 3. Error Handling
- **Improved**: Proper exception handling with specific exception types
- **Added**: Graceful handling of file operations and JSON parsing
- **Location**: `run.py`, `chatdev/chat_chain.py`, `chatdev/phase.py`

## Security Best Practices

### For Users

1. **API Key Security**
   - Never commit API keys to version control
   - Use environment variables for sensitive configuration
   - Regularly rotate your OpenAI API keys

2. **Input Validation**
   - Avoid using special characters in project names
   - Be cautious with user-provided prompts that might contain sensitive information

3. **File System Security**
   - Run ChatDev in a sandboxed environment when possible
   - Review generated code before execution
   - Be aware that ChatDev may install Python packages automatically

### For Developers

1. **Code Security**
   - Always validate user inputs
   - Use parameterized commands instead of shell=True
   - Implement proper error handling
   - Follow the principle of least privilege

2. **Dependencies**
   - Regularly update dependencies to patch security vulnerabilities
   - Review third-party packages before installation
   - Use virtual environments to isolate dependencies

## Reporting Security Issues

If you discover a security vulnerability, please report it by:

1. **Do not** create a public GitHub issue
2. Email the maintainers directly with details
3. Include steps to reproduce the issue
4. Allow reasonable time for the issue to be addressed before public disclosure

## Security Checklist for Contributors

- [ ] Input validation for all user-provided data
- [ ] No use of `shell=True` with user input
- [ ] Proper error handling with specific exceptions
- [ ] No hardcoded secrets or credentials
- [ ] Documentation of security considerations
- [ ] Code review for security implications

## Additional Resources

- [OWASP Top 10](https://owasp.org/www-project-top-ten/)
- [Python Security Guidelines](https://python.org/dev/security/)
- [Secure Coding Practices](https://owasp.org/www-project-secure-coding-practices-quick-reference-guide/)