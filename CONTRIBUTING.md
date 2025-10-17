# Contributing to Stream Bill Generator

Thank you for your interest in contributing to the Stream Bill Generator! This document provides guidelines and best practices for contributing to the project.

## Code of Conduct

By participating in this project, you agree to abide by our Code of Conduct. Please treat all contributors and users with respect and professionalism.

## How to Contribute

### Reporting Bugs

Before submitting a bug report, please check if the issue has already been reported. If not, create a new issue with:

1. A clear and descriptive title
2. Steps to reproduce the issue
3. Expected behavior
4. Actual behavior
5. Screenshots or error messages if applicable
6. Your environment details (OS, Python version, etc.)

### Suggesting Enhancements

We welcome suggestions for new features or improvements. Please create an issue with:

1. A clear description of the enhancement
2. Use cases or scenarios where it would be beneficial
3. Any implementation ideas you might have

### Code Contributions

#### Development Setup

1. Fork the repository
2. Clone your fork
3. Create a new branch for your feature or bugfix
4. Install dependencies: `pip install -r requirements.txt`
5. Make your changes
6. Test your changes
7. Submit a pull request

#### Pull Request Process

1. Ensure your code follows the project's coding standards
2. Add tests for any new functionality
3. Update documentation as needed
4. Ensure all tests pass
5. Submit a pull request with a clear description of your changes

### Architecture Guidelines

Please familiarize yourself with our [Architecture Overview](ARCHITECTURE.md) before making contributions. Key principles include:

1. **DO NOT modify files in `core/`** - These contain protected computation logic
2. **Follow the modular structure** - Add new features in appropriate modules
3. **Maintain backward compatibility** - Existing functionality must continue to work
4. **Write tests** - All new code should have unit tests

### Coding Standards

#### Python Style

We follow PEP 8 guidelines with some project-specific conventions:

- Use 4 spaces for indentation
- Limit lines to 88 characters
- Use descriptive variable and function names
- Write docstrings for all public functions and classes
- Use type hints where possible

#### Example

```python
def calculate_total(items: List[Dict[str, Any]]) -> float:
    """
    Calculate the total amount from a list of items.
    
    Args:
        items: List of item dictionaries with 'amount' key
        
    Returns:
        float: Total amount
    """
    return sum(item.get('amount', 0) for item in items)
```

### Testing

#### Running Tests

```bash
# Run all tests
pytest

# Run specific test file
pytest tests/test_exports.py

# Run tests with coverage
pytest --cov=exports --cov=core
```

#### Writing Tests

- Place test files in the `tests/` directory
- Follow the naming convention `test_*.py`
- Use pytest for test framework
- Write both unit and integration tests
- Test edge cases and error conditions

### Documentation

#### Updating Documentation

- Update README.md for user-facing changes
- Update ARCHITECTURE.md for architectural changes
- Add docstrings to new functions and classes
- Update this CONTRIBUTING.md for process changes

### Commit Messages

Follow conventional commit messages:

- `feat: Add new feature`
- `fix: Resolve bug issue`
- `docs: Update documentation`
- `test: Add test cases`
- `refactor: Restructure code`
- `chore: Update dependencies`

### Branch Naming

Use descriptive branch names:

- `feature/pdf-enhancement`
- `bugfix/zero-rate-handling`
- `docs/architecture-update`
- `test/validation-improvements`

## Getting Help

If you need help with your contribution:

1. Check the documentation
2. Review existing issues and pull requests
3. Ask questions in new issues
4. Contact the maintainers

## License

By contributing to this project, you agree that your contributions will be licensed under the same license as the project (typically MIT or Apache 2.0).

## Recognition

Contributors will be recognized in:

1. Git commit history
2. GitHub contributors list
3. Project release notes
4. Hall of Contributors (if implemented)

Thank you for contributing to the Stream Bill Generator!