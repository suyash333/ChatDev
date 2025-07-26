# ChatDev Development Makefile

.PHONY: help install check clean test run-example security-check setup-dev

# Default target
help:
	@echo "ChatDev Development Tasks"
	@echo "========================"
	@echo "install        - Install dependencies"
	@echo "check          - Run code quality and security checks"
	@echo "clean          - Clean temporary files and caches"
	@echo "test           - Run tests (if available)"
	@echo "run-example    - Run a simple example"
	@echo "security-check - Run security-focused checks"
	@echo "setup-dev      - Set up development environment"

# Install dependencies
install:
	pip install -r requirements.txt

# Run code quality checks
check:
	@echo "Running code quality and security checks..."
	python scripts/check_code_quality.py
	@echo "Checking Python syntax..."
	find chatdev -name "*.py" -exec python -m py_compile {} \;
	@echo "Checks completed!"

# Clean temporary files
clean:
	find . -type d -name "__pycache__" -exec rm -rf {} + 2>/dev/null || true
	find . -name "*.pyc" -delete 2>/dev/null || true
	find . -name "*.pyo" -delete 2>/dev/null || true
	find . -name ".coverage" -delete 2>/dev/null || true
	find . -type d -name "*.egg-info" -exec rm -rf {} + 2>/dev/null || true

# Run tests (placeholder for future test implementation)
test:
	@echo "No tests implemented yet. Consider adding pytest tests!"
	@echo "Example test structure:"
	@echo "  tests/"
	@echo "    test_chat_env.py"
	@echo "    test_chat_chain.py"
	@echo "    test_utils.py"

# Run a simple example
run-example:
	@echo "Running ChatDev example..."
	@echo "Note: This requires OpenAI API key to be set in OPENAI_API_KEY environment variable"
	@echo "Example command:"
	@echo "  export OPENAI_API_KEY=your_key_here"
	@echo "  python run.py --task 'Create a simple calculator' --name 'Calculator'"

# Security-focused checks
security-check:
	@echo "Running security checks..."
	@echo "Checking for potential security issues..."
	grep -r "shell=True" chatdev/ && echo "WARNING: shell=True found!" || echo "✓ No shell=True usage"
	grep -r "eval\|exec" chatdev/ && echo "WARNING: eval/exec found!" || echo "✓ No eval/exec usage"
	grep -r "password\|secret\|api_key" chatdev/ --include="*.py" | grep -v "# " && echo "WARNING: Potential secrets!" || echo "✓ No hardcoded secrets"
	@echo "Security check completed!"

# Set up development environment
setup-dev: install
	@echo "Setting up development environment..."
	@echo "Creating example configuration..."
	@echo "Development environment ready!"
	@echo ""
	@echo "Next steps:"
	@echo "1. Set your OpenAI API key: export OPENAI_API_KEY=your_key"
	@echo "2. Run quality checks: make check"
	@echo "3. Try an example: make run-example"

# Lint and format code (placeholder for future linting tools)
lint:
	@echo "Linting not configured yet. Consider adding:"
	@echo "  - black (code formatting)"
	@echo "  - flake8 (linting)"
	@echo "  - mypy (type checking)"
	@echo "  - pylint (comprehensive linting)"

# Check dependencies for security vulnerabilities
audit:
	@echo "Dependency security audit not configured yet."
	@echo "Consider using: pip-audit or safety"