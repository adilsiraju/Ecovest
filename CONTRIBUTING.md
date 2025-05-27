# Contributing to Ecovest

Thank you for your interest in contributing to Ecovest! This document provides guidelines for contributing to the project.

## 🚀 Getting Started

### Prerequisites
- Python 3.11+
- Django 5.2+
- Git knowledge
- Understanding of sustainable investing concepts (helpful but not required)

### Development Setup
1. Fork the repository
2. Clone your fork: `git clone https://github.com/YOUR-USERNAME/Ecovest.git`
3. Follow the installation instructions in [README.md](README.md)
4. Create a new branch: `git checkout -b feature/your-feature-name`

## 📋 How to Contribute

### Reporting Bugs
Before creating a bug report, please check if the issue already exists. When creating a bug report, include:

- **Clear title** and description
- **Steps to reproduce** the issue
- **Expected vs actual behavior**
- **Environment details** (OS, Python version, Django version)
- **Screenshots** if applicable

### Suggesting Features
Feature suggestions are welcome! Please:

- **Check existing issues** first
- **Provide clear use case** and rationale
- **Consider implementation complexity**
- **Think about sustainability impact**

### Code Contributions

#### Coding Standards
- Follow [PEP 8](https://pep8.org/) Python style guide
- Use meaningful variable and function names
- Add docstrings to all public functions and classes
- Keep functions focused and under 50 lines when possible
- Use type hints where applicable

#### Code Quality Tools
We use several tools to maintain code quality:

```bash
# Code formatting
black .

# Import sorting
isort .

# Linting
flake8 .

# Type checking
mypy .
```

#### Commit Message Format
Follow the [Conventional Commits](https://www.conventionalcommits.org/) specification:

```
<type>(<scope>): <description>

[optional body]

[optional footer]
```

Types:
- `feat`: New feature
- `fix`: Bug fix
- `docs`: Documentation changes
- `style`: Code style changes (formatting, etc.)
- `refactor`: Code refactoring
- `test`: Adding or updating tests
- `chore`: Maintenance tasks

Examples:
```
feat(investments): add new impact prediction model
fix(auth): resolve login redirect issue
docs(readme): update installation instructions
```

## 🧪 Testing

### Running Tests
```bash
# Run all tests
python manage.py test

# Run specific app tests
python manage.py test initiatives

# Run with coverage
pip install coverage
coverage run manage.py test
coverage report
```

### Writing Tests
- Write tests for all new functionality
- Aim for >80% code coverage
- Use Django's built-in testing framework
- Follow AAA pattern (Arrange, Act, Assert)

Example test:
```python
from django.test import TestCase
from initiatives.models import Initiative, Category

class InitiativeModelTest(TestCase):
    def setUp(self):
        self.category = Category.objects.create(
            name='Renewable Energy',
            description='Clean energy projects'
        )
    
    def test_initiative_creation(self):
        initiative = Initiative.objects.create(
            title='Solar Farm Project',
            category=self.category,
            target_amount=1000000
        )
        self.assertEqual(initiative.title, 'Solar Farm Project')
        self.assertEqual(initiative.category, self.category)
```

## 📁 Project Structure

```
Ecovest/
├── core/              # Core application logic
├── initiatives/       # Project management
├── investments/       # Investment tracking & AI
├── users/            # User management
├── onboarding/       # User onboarding
├── static/           # Static files
├── media/            # Uploaded files
├── templates/        # HTML templates
├── tests/            # Test files
└── docs/             # Documentation
```

## 🎯 Focus Areas

We especially welcome contributions in these areas:

### 🤖 AI/ML Improvements
- Enhanced prediction models
- New sustainability metrics
- Model accuracy improvements
- Real-time data integration

### 🌍 Sustainability Features
- New investment categories
- Impact measurement tools
- Carbon footprint tracking
- ESG scoring algorithms

### 💻 Technical Enhancements
- API development
- Performance optimization
- Security improvements
- Mobile responsiveness

### 📊 Data & Analytics
- Dashboard improvements
- New visualization types
- Reporting features
- Data export capabilities

## 🔍 Code Review Process

1. **Self-review** your code before submitting
2. **Ensure tests pass** and coverage is maintained
3. **Update documentation** if needed
4. **Submit pull request** with clear description
5. **Address review feedback** promptly

### Pull Request Guidelines
- **Clear title** describing the change
- **Detailed description** of what and why
- **Link related issues** using keywords (fixes #123)
- **Include screenshots** for UI changes
- **Keep changes focused** - one feature per PR

## 🏆 Recognition

Contributors will be recognized in:
- README.md contributors section
- Release notes for significant contributions
- Special mentions for outstanding contributions

## ❓ Questions?

- **General questions**: Open a [discussion](https://github.com/adilsiraju/Ecovest/discussions)
- **Bug reports**: Create an [issue](https://github.com/adilsiraju/Ecovest/issues)
- **Feature requests**: Open a [feature request](https://github.com/adilsiraju/Ecovest/issues/new?template=feature_request.md)

## 📞 Contact

- **Email**: developers@ecovest.com
- **Discord**: [Join our developer community](https://discord.gg/ecovest-dev)

---

By contributing to Ecovest, you're helping build a more sustainable financial future! 🌱
