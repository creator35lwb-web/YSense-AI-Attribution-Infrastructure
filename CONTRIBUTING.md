# Contributing to YSenseAI

Thank you for your interest in contributing to YSenseAI! We welcome contributions from developers, researchers, designers, and community members.

## Table of Contents

- [Code of Conduct](#code-of-conduct)
- [Ways to Contribute](#ways-to-contribute)
- [Development Setup](#development-setup)
- [Pull Request Process](#pull-request-process)
- [Coding Standards](#coding-standards)
- [Testing Guidelines](#testing-guidelines)
- [Documentation](#documentation)
- [Community](#community)

---

## Code of Conduct

By participating in this project, you agree to abide by our [Code of Conduct](CODE_OF_CONDUCT.md). Please read it before contributing.

**TL;DR**: Be respectful, inclusive, and professional. Harassment and discrimination are not tolerated.

---

## Ways to Contribute

### 1. Code Contributions

- **Fix bugs**: Check [open issues](https://github.com/creator35lwb-web/YSense-AI-Attribution-Infrastructure/issues) labeled `bug`
- **Add features**: Check issues labeled `enhancement` or `feature request`
- **Improve performance**: Optimize algorithms, database queries, or UI rendering
- **Refactor code**: Improve code quality, readability, or maintainability

### 2. Documentation

- **Write guides**: User guides, tutorials, how-tos
- **Improve README**: Clarify installation, usage, or examples
- **Add code comments**: Explain complex logic or algorithms
- **Translate**: Translate documentation to other languages

### 3. Research

- **Study ethical AI**: Publish research on Z-Protocol, consent management, or attribution
- **Analyze data**: Study quality metrics, consent patterns, or user behavior
- **Write papers**: Academic publications citing YSenseAI

### 4. Community

- **Answer questions**: Help users on GitHub Issues or Discord
- **Report bugs**: Submit detailed bug reports with reproduction steps
- **Suggest features**: Propose new features or improvements
- **Organize events**: Hackathons, workshops, or meetups

### 5. Design

- **UI/UX improvements**: Redesign interfaces, improve user flows
- **Graphics**: Create logos, icons, or illustrations
- **Branding**: Develop visual identity or marketing materials

---

## Development Setup

### Prerequisites

- Python 3.11 or higher
- Git
- Virtual environment tool (venv, conda, or virtualenv)
- (Optional) Docker for containerized development

### Fork and Clone

```bash
# Fork the repository on GitHub (click "Fork" button)

# Clone your fork
git clone https://github.com/YOUR_USERNAME/YSense-AI-Attribution-Infrastructure.git
cd YSense-AI-Attribution-Infrastructure

# Add upstream remote
git remote add upstream https://github.com/creator35lwb-web/YSense-AI-Attribution-Infrastructure.git
```

### Install Dependencies

```bash
# Create virtual environment
python3.11 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements_production.txt

# Install dev dependencies
pip install -r requirements_dev.txt
```

### Set Up Environment

```bash
# Copy example environment file
cp .env.example .env

# Edit .env with your API keys
# Get keys from:
# - Anthropic: https://console.anthropic.com/
# - Qwen: https://www.alibabacloud.com/help/en/model-studio/get-api-key
```

### Run the Application

```bash
# Initialize database
python -c "from v45_beta.database.schema import Database; Database()"

# Start Streamlit app
streamlit run v45_beta/app_legal_protected.py
```

Navigate to `http://localhost:8501`

---

## Pull Request Process

### 1. Create a Feature Branch

```bash
# Update your fork
git fetch upstream
git checkout main
git merge upstream/main

# Create feature branch
git checkout -b feature/your-feature-name
```

**Branch naming conventions**:
- `feature/` - New features
- `bugfix/` - Bug fixes
- `docs/` - Documentation changes
- `refactor/` - Code refactoring
- `test/` - Test additions or fixes

### 2. Make Your Changes

- Write clean, readable code
- Follow [coding standards](#coding-standards)
- Add tests for new features
- Update documentation if needed

### 3. Commit Your Changes

```bash
# Stage changes
git add .

# Commit with descriptive message
git commit -m "feat: add collaborative distillation dialogue"
```

**Commit message format**:
```
<type>: <subject>

<body>

<footer>
```

**Types**:
- `feat`: New feature
- `fix`: Bug fix
- `docs`: Documentation changes
- `style`: Code style changes (formatting, no logic change)
- `refactor`: Code refactoring
- `test`: Adding or updating tests
- `chore`: Maintenance tasks

**Example**:
```
feat: add collaborative distillation dialogue

- Add chat interface for 3-word refinement
- Integrate Claude API for AI responses
- Save dialogue history in database

Closes #123
```

### 4. Push to Your Fork

```bash
git push origin feature/your-feature-name
```

### 5. Create Pull Request

1. Go to your fork on GitHub
2. Click "Compare & pull request"
3. Fill in PR template:
   - **Title**: Clear, descriptive title
   - **Description**: What changes were made and why
   - **Related Issues**: Link to related issues (e.g., "Closes #123")
   - **Testing**: How you tested the changes
   - **Screenshots**: If UI changes, include screenshots

### 6. Code Review

- Maintainers will review your PR
- Address feedback by pushing new commits
- Once approved, your PR will be merged

---

## Coding Standards

### Python Style Guide

Follow [PEP 8](https://pep8.org/) with these additions:

**Formatting**:
- Use 4 spaces for indentation (no tabs)
- Maximum line length: 100 characters
- Use double quotes for strings (`"hello"` not `'hello'`)

**Naming**:
- Functions: `snake_case` (e.g., `calculate_quality_metrics`)
- Classes: `PascalCase` (e.g., `AttributionEngine`)
- Constants: `UPPER_SNAKE_CASE` (e.g., `MAX_TOKEN_LENGTH`)
- Private methods: `_leading_underscore` (e.g., `_internal_method`)

**Docstrings**:
```python
def calculate_quality_metrics(story: str, layers: dict) -> dict:
    """
    Calculate 6 training optimization quality metrics.
    
    Args:
        story: Raw story text
        layers: Dictionary of 5 perception layers
        
    Returns:
        Dictionary with quality scores and recommendations
        
    Example:
        >>> metrics = calculate_quality_metrics(story, layers)
        >>> print(metrics['overall_score'])
        0.85
    """
    pass
```

**Type Hints**:
- Use type hints for function parameters and return values
- Use `typing` module for complex types

```python
from typing import List, Dict, Optional

def process_submissions(
    user_id: int,
    submissions: List[Dict[str, any]],
    min_quality: Optional[float] = 0.7
) -> List[Dict[str, any]]:
    pass
```

### Code Organization

**File structure**:
```
v45_beta/
├── agents/              # AI agent integrations
├── attribution/         # Attribution engine
├── consent/             # Consent management
├── database/            # Database schema
├── exports/             # Export pipeline
├── legal/               # Legal documents
├── ui/                  # UI components
└── app_legal_protected.py  # Main application
```

**Imports**:
```python
# Standard library
import os
import sys
from datetime import datetime

# Third-party
import streamlit as st
from anthropic import Anthropic

# Local
from attribution.attribution_engine import AttributionEngine
from database.schema import Database
```

---

## Testing Guidelines

### Running Tests

```bash
# Run all tests
pytest tests/

# Run specific test file
pytest tests/test_attribution.py

# Run with coverage
pytest --cov=v45_beta tests/
```

### Writing Tests

**Test file naming**: `test_<module_name>.py`

**Test function naming**: `test_<function_name>_<scenario>`

**Example**:
```python
# tests/test_attribution.py

import pytest
from v45_beta.attribution.attribution_engine import AttributionEngine

def test_create_attribution_success():
    """Test successful attribution creation"""
    engine = AttributionEngine()
    
    attribution = engine.create_attribution(
        user_id=1,
        content="Test story",
        layers={"narrative": "Test"},
        essence="Test. Words. Here.",
        tier="PUBLIC"
    )
    
    assert attribution['fingerprint'] is not None
    assert attribution['did'].startswith('did:ysense:')
    assert attribution['tier'] == 'PUBLIC'

def test_create_attribution_invalid_tier():
    """Test attribution creation with invalid tier"""
    engine = AttributionEngine()
    
    with pytest.raises(ValueError):
        engine.create_attribution(
            user_id=1,
            content="Test",
            layers={},
            essence="Test",
            tier="INVALID"
        )
```

### Test Coverage

- Aim for >80% code coverage
- Test happy paths and edge cases
- Test error handling
- Mock external APIs (Claude, Qwen)

---

## Documentation

### Code Documentation

- Add docstrings to all public functions and classes
- Use clear, descriptive variable names
- Add comments for complex logic

### User Documentation

Update user-facing documentation when:
- Adding new features
- Changing UI or workflows
- Updating installation or configuration

**Documentation files**:
- `README.md` - Project overview
- `docs/USER_GUIDE.md` - User guide
- `docs/API_REFERENCE.md` - API documentation
- `docs/ARCHITECTURE.md` - System architecture

---

## Community

### Communication Channels

- **GitHub Issues**: Bug reports, feature requests, discussions
- **GitHub Discussions**: General questions, ideas, announcements
- **Discord**: Real-time chat (coming soon)
- **Email**: alton@ysenseai.org or creator35lwb@gmail.com

### Getting Help

- Check [FAQ](docs/FAQ.md)
- Search [existing issues](https://github.com/creator35lwb-web/YSense-AI-Attribution-Infrastructure/issues)
- Ask in GitHub Discussions
- Join Discord for real-time help

### Recognition

Contributors will be:
- Listed in `CONTRIBUTORS.md`
- Mentioned in release notes
- Thanked in project README

Significant contributors may be invited to join the core team!

---

## License

By contributing to YSenseAI, you agree that your contributions will be licensed under:

- **Code**: MIT License
- **Z-Protocol**: Creative Commons Attribution-ShareAlike 4.0 International (CC BY-SA 4.0)

See [LICENSE](LICENSE) and [LICENSE-ZPROTOCOL](LICENSE-ZPROTOCOL) for details.

---

## Questions?

If you have questions about contributing, please:

1. Check this guide
2. Search existing issues
3. Ask in GitHub Discussions
4. Email alton@ysenseai.org or creator35lwb@gmail.com

**Thank you for contributing to ethical AI! 🙏**
