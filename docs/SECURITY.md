# Security Policy

## Supported Versions

We actively support the following versions of Ecovest with security updates:

| Version | Supported          |
| ------- | ------------------ |
| 0.1.x   | :white_check_mark: |

## Reporting a Vulnerability

We take security seriously. If you discover a security vulnerability, please report it responsibly.

### How to Report

1. **Email**: Send details to security@ecovest.com
2. **Subject Line**: "Security Vulnerability Report"
3. **Include**:
   - Description of the vulnerability
   - Steps to reproduce
   - Potential impact
   - Suggested fix (if any)

### What to Expect

- **Acknowledgment**: Within 24 hours
- **Initial Assessment**: Within 72 hours
- **Fix Timeline**: 7-30 days depending on severity
- **Public Disclosure**: After fix is deployed

### Responsible Disclosure

Please do not:
- Publicly disclose the vulnerability before we've had a chance to fix it
- Access or modify data that doesn't belong to you
- Perform any destructive actions

We appreciate responsible disclosure and will acknowledge your contribution.

## Security Measures

### Authentication & Authorization
- Django's built-in authentication system
- Session-based authentication for web interface
- API key authentication for programmatic access
- Role-based access control

### Data Protection
- All sensitive data encrypted in transit (HTTPS)
- Database encryption at rest
- Secure password hashing (Django's PBKDF2)
- Personal data minimization

### Infrastructure Security
- Regular security updates
- Firewall protection
- Intrusion detection
- Regular backups with encryption

### Code Security
- Input validation and sanitization
- SQL injection prevention (Django ORM)
- XSS protection
- CSRF protection enabled
- Security headers implemented

## Security Headers

The following security headers are implemented:

```python
# Security Headers
SECURE_BROWSER_XSS_FILTER = True
SECURE_CONTENT_TYPE_NOSNIFF = True
X_FRAME_OPTIONS = 'DENY'
SECURE_HSTS_SECONDS = 31536000
SECURE_HSTS_INCLUDE_SUBDOMAINS = True
SECURE_HSTS_PRELOAD = True
```

## Contact

For security-related questions or concerns:
- **Email**: security@ecovest.com
- **Response Time**: 24-48 hours
