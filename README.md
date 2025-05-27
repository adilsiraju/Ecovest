# 🌱 Ecovest - Sustainable Investing Platform

[![Django](https://img.shields.io/badge/Django-5.2-green.svg)](https://djangoproject.com/)
[![Python](https://img.shields.io/badge/Python-3.11+-blue.svg)](https://python.org/)
[![License](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)
[![Status](https://img.shields.io/badge/Status-In%20Development-orange.svg)]()

![Ecovest Platform](https://github.com/user-attachments/assets/4476700f-8d9e-4750-9f17-287efabffb51)

## 📖 About Ecovest

Ecovest is a cutting-edge sustainable investing platform that bridges the gap between environmentally conscious investors and high-impact, eco-friendly investment opportunities. Our mission is to democratize sustainable investing by making it accessible, transparent, and profitable for everyone.

### ✨ Key Features

- **🤖 AI-Powered Impact Prediction** - Advanced machine learning models predict environmental outcomes
- **📊 Real-time Portfolio Tracking** - Monitor both financial performance and environmental impact
- **🌍 Curated Green Opportunities** - Vetted sustainable initiatives and green technology startups
- **📈 Measurable Impact Metrics** - Track carbon reduction, energy savings, and water conservation
- **🔍 Transparent Investment Process** - Full visibility into how your investments create positive change

## 🚀 Quick Start

### Prerequisites

- Python 3.11 or higher
- pip (Python package manager)
- Git

### Installation

1. **Clone and navigate to the repository**
   ```bash
   git clone https://github.com/adilsiraju/Ecovest.git
   cd Ecovest
   ```

2. **Set up virtual environment**
   ```bash
   # Windows
   python -m venv venv
   .\venv\Scripts\activate
   
   # macOS/Linux
   python -m venv venv
   source venv/bin/activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Configure environment**
   ```bash
   cp .env.example .env
   # Edit .env file with your configuration
   ```

5. **Initialize database**
   ```bash
   python manage.py migrate
   python manage.py createsuperuser
   python manage.py loaddata fixtures/sample_data.json  # Optional sample data
   ```

6. **Launch the application**
   ```bash
   python manage.py runserver
   ```

7. **Access Ecovest**
   - **Main Application**: http://127.0.0.1:8000/
   - **Admin Panel**: http://127.0.0.1:8000/admin/

## 🏗️ Project Structure

```
Ecovest/
├── 📁 core/              # Core application logic and settings
├── 📁 initiatives/       # Sustainable project management
├── 📁 investments/       # Investment tracking & AI prediction models
├── 📁 users/            # User management & authentication
├── 📁 onboarding/       # User onboarding flow
├── 📁 static/           # Static assets (CSS, JS, images)
├── 📁 media/            # User-uploaded files
├── 📁 templates/        # HTML templates
└── 📄 manage.py         # Django management script
```

## 🧠 AI Impact Prediction System

Our proprietary AI system uses machine learning to predict environmental impact across three key metrics for any investment:

### Prediction Metrics
- **Carbon Reduction** (kg CO2 equivalent)
- **Energy Savings** (kWh)
- **Water Conservation** (Liters)

### Supported Investment Categories
1. Renewable Energy
2. Recycling & Waste Management
3. Emission Control
4. Water Conservation
5. Reforestation
6. Sustainable Agriculture
7. Clean Transportation
8. Green Technology
9. Ocean Conservation

### Using the AI System

#### Generate and Test Models
```bash
# Generate optimized ML models
python investments/generate_models.py

# Test models with Jupyter notebook
pip install jupyter
jupyter notebook investments/model_testing.ipynb
```

#### Predict Impact in Code
```python
from investments.impact_calculator import ImpactCalculator

calculator = ImpactCalculator()
impact = calculator.predict_impact(
    investment_amount=1000000,  # Amount in rupees
    category_names=['Renewable Energy'],
    project_duration_months=12,
    project_scale=3,  # Scale: 1-5
    location='Karnataka',
    technology_type='Solar'
)

print(f"Carbon Reduced: {impact['carbon']} kg CO2")
print(f"Energy Saved: {impact['energy']} kWh") 
print(f"Water Conserved: {impact['water']} L")
```

### Model Technical Details
- **Algorithm**: Random Forest Regressor (3 separate models for each metric)
- **Training Data**: 150+ data points based on real sustainability metrics
- **Validation**: Cross-validation with R² scores > 0.85
- **Features**: Investment amount, category, duration, scale, location, technology type

## 🛠️ Development

### Tech Stack
- **Backend**: Django 5.2, Python 3.11+
- **Database**: SQLite (development), PostgreSQL (production)
- **Frontend**: HTML5, CSS3, JavaScript, Bootstrap 5
- **AI/ML**: scikit-learn, pandas, numpy
- **Analytics**: Matplotlib, Jupyter Notebooks

### Development Commands

```bash
# Run tests
python manage.py test

# Database operations
python manage.py makemigrations
python manage.py migrate

# Code quality
black .                    # Format code
flake8 .                  # Linting
mypy .                    # Type checking

# Coverage report
coverage run manage.py test
coverage report
```

### Development Workflow

1. **Create feature branch**: `git checkout -b feature/your-feature-name`
2. **Make changes and test**: `python manage.py test`
3. **Run quality checks**: `black . && flake8 . && mypy .`
4. **Commit and push**: Follow conventional commit format

## 📚 API Reference

### Impact Prediction Endpoint

**POST** `/api/predict-impact/`

```json
{
    "investment_amount": 1000000,
    "category_names": ["Renewable Energy"],
    "project_duration_months": 12,
    "project_scale": 3,
    "location": "Karnataka",
    "technology_type": "Solar"
}
```

**Response:**
```json
{
    "carbon": 25000.5,
    "energy": 150000.0,
    "water": 50000.0,
    "status": "success"
}
```

## 🤝 Contributing

We welcome contributions from the community! Here's how you can help:

### How to Contribute
1. **Fork** the repository
2. **Create** a feature branch (`git checkout -b feature/amazing-feature`)
3. **Make** your changes and add tests
4. **Ensure** all tests pass (`python manage.py test`)
5. **Commit** your changes (`git commit -m 'feat: add amazing feature'`)
6. **Push** to your branch (`git push origin feature/amazing-feature`)
7. **Submit** a pull request

### Code Standards
- Follow PEP 8 for Python code
- Write meaningful commit messages using conventional commits
- Add tests for new functionality
- Include docstrings for all functions and classes
- Keep functions focused and well-documented

For detailed guidelines, see our [Contributing Guide](CONTRIBUTING.md).

## 📋 Documentation

### Essential Guides
- **[Development Setup](DEVELOPMENT.md)** - Complete development environment setup
- **[API Documentation](API_DOCUMENTATION.md)** - Comprehensive API reference
- **[Deployment Guide](DEPLOYMENT.md)** - Production deployment instructions

### Project Resources  
- **[Contributing Guidelines](CONTRIBUTING.md)** - How to contribute effectively
- **[Changelog](CHANGELOG.md)** - Version history and updates
- **[Security Policy](SECURITY.md)** - Security guidelines and reporting

### Templates & Workflows
- **[Issue Templates](.github/ISSUE_TEMPLATE/)** - Bug reports and feature requests
- **[Pull Request Template](.github/pull_request_template.md)** - PR submission guidelines
- **[CI/CD Pipeline](.github/workflows/ci.yml)** - Automated testing and deployment

## 📄 License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.

## 📞 Support & Contact

- **🐛 Bug Reports**: [GitHub Issues](https://github.com/adilsiraju/Ecovest/issues)
- **💡 Feature Requests**: [GitHub Discussions](https://github.com/adilsiraju/Ecovest/discussions)
- **📧 Email Support**: support@ecovest.com
- **📖 Documentation**: [Project Wiki](https://github.com/adilsiraju/Ecovest/wiki)

## 🙏 Acknowledgments

- **Django Community** for the robust web framework
- **scikit-learn Team** for powerful machine learning tools
- **Open Source Contributors** who make sustainable tech possible
- **Environmental Organizations** providing real-world sustainability data

---

**Made with 💚 for a sustainable future**

*Join us in revolutionizing how the world invests in environmental solutions.*