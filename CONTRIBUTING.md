# Contributing to HealthHub

Thank you for your interest in contributing to HealthHub! This guide will help you understand our development process.

## Development Workflow

### 1. Fork & Clone

```bash
git clone https://github.com/R-dev-07/healthhub.git
cd healthhub
git remote add upstream https://github.com/original-owner/healthhub.git
```

### 2. Create Feature Branch

```bash
git checkout -b feature/your-feature-name
```

Branch naming conventions:
- `feature/` - New features
- `bugfix/` - Bug fixes
- `docs/` - Documentation updates
- `refactor/` - Code refactoring
- `test/` - Test additions

### 3. Make Changes

```bash
# Create virtual environment
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
pip install -r requirements-dev.txt

# Make your changes
# Run tests frequently
python manage.py test

# Check code style
flake8 .
black --check .
isort --check .
```

### 4. Commit Changes

```bash
# Write clear commit messages
git commit -m "feature: add patient appointment notifications

- Added EmailNotification model
- Created notification signals
- Implemented background email task
- Added tests for notification system"
```

### 5. Push & Create PR

```bash
git push origin feature/your-feature-name
```

Create a Pull Request on GitHub with:
- Clear title describing the change
- Description of what changed and why
- Link to related issues (if any)
- Screenshots (if UI changes)

## Code Standards

### Python Style

Follow [PEP 8](https://www.python.org/dev/peps/pep-0008/):

```bash
# Format code
black .

# Sort imports
isort .

# Check style
flake8 .

# Check type hints
mypy .
```

### Django Conventions

```python
# Models should be singular (Django converts to plural)
class Patient(models.Model):
    pass

# Use model properties for computed values
@property
def is_active(self):
    return self.enrollment_status == 'active'

# Use descriptive method names
def get_prescriptions_for_month(self, month):
    pass

# Use django-extensions for better model methods
def __str__(self):
    return f"{self.first_name} {self.last_name}"
```

### Model Best Practices

```python
class BaseModel(models.Model):
    """Abstract base model with common fields"""
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        abstract = True

class Patient(BaseModel):
    """Inherit common fields"""
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE)
    
    class Meta:
        verbose_name = "Patient"
        verbose_name_plural = "Patients"
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['user', '-created_at']),
        ]
```

### View Best Practices

```python
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404

@login_required(login_url='login')
def patient_detail(request, pk):
    """View with proper access control"""
    patient = get_object_or_404(Patient, pk=pk)
    
    # Check permissions
    if request.user != patient.user:
        raise PermissionDenied
    
    context = {'patient': patient}
    return render(request, 'patient_detail.html', context)
```

### API Views

```python
from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated

class PatientViewSet(viewsets.ModelViewSet):
    serializer_class = PatientSerializer
    permission_classes = [IsAuthenticated]
    
    def get_queryset(self):
        """Filter by current user"""
        return Patient.objects.filter(user=self.request.user)
    
    @action(detail=False, methods=['GET'])
    def my_profile(self, request):
        """Custom action"""
        patient = self.get_queryset().first()
        serializer = self.get_serializer(patient)
        return Response(serializer.data)
```

## Documentation

### Docstring Format

```python
def process_payment(appointment, amount):
    """
    Process payment for an appointment via SSLCommerz.
    
    Args:
        appointment (Appointment): The appointment instance
        amount (Decimal): Payment amount in USD
    
    Returns:
        dict: Payment response with transaction_id and status
    
    Raises:
        PaymentException: If payment processing fails
    
    Example:
        >>> response = process_payment(appointment, 50.00)
        >>> if response['status'] == 'success':
        ...     appointment.is_paid = True
        ...     appointment.save()
    """
    pass
```

### Type Hints

```python
from typing import Optional, List, Dict

def get_doctor_appointments(
    doctor: Doctor,
    status: Optional[str] = None
) -> List[Appointment]:
    """Get appointments for a doctor with optional status filter."""
    pass

def get_payment_summary(
    user_id: int
) -> Dict[str, any]:
    """Return payment summary for user."""
    pass
```

## Testing Requirements

### Minimum Coverage

- Models: 100%
- Views: 85%
- Serializers: 80%
- Forms: 80%
- Utilities: 85%
- Overall: 80%+

### Test Example

```python
from django.test import TestCase
from .models import Doctor
from .factories import DoctorFactory

class DoctorModelTests(TestCase):
    """Test Doctor model"""
    
    def setUp(self):
        self.doctor = DoctorFactory()
    
    def test_doctor_creation(self):
        """Test doctor can be created"""
        self.assertIsNotNone(self.doctor.id)
        self.assertTrue(len(self.doctor.user.username) > 0)
    
    def test_doctor_str_representation(self):
        """Test doctor string representation"""
        expected = f"Dr. {self.doctor.user.first_name} {self.doctor.user.last_name}"
        self.assertEqual(str(self.doctor), expected)
    
    def test_doctor_average_rating(self):
        """Test doctor average rating calculation"""
        rating = self.doctor.get_average_rating()
        self.assertGreaterEqual(rating, 0)
        self.assertLessEqual(rating, 5)
```

## Bug Reports

When reporting bugs, include:

1. **System Information**
   - OS and Python version
   - Django version
   - Browser (if frontend issue)

2. **Steps to Reproduce**
   ```
   1. Go to 'appointments'
   2. Click 'Create appointment'
   3. Select a doctor
   4. Error occurs
   ```

3. **Expected Behavior**
   - What should happen

4. **Actual Behavior**
   - What actually happened

5. **Logs & Screenshots**
   - Error messages
   - Screenshots of bug

6. **Minimal Code Example**
   ```python
   appointment = Appointment.objects.create(
       doctor=doctor,
       patient=patient,
       appointment_date=timezone.now()
   )
   ```

## Feature Requests

Describe:
- What you want to build
- Why you need it
- Suggested implementation
- Examples from other apps

## Review Process

### Automated Checks

```bash
# Run before pushing
python manage.py test
black .
isort .
flake8 .
mypy .
```

### Code Review Checklist

- [ ] Code follows style guidelines
- [ ] Tests are included and passing
- [ ] Documentation is updated
- [ ] No unnecessary dependencies added
- [ ] Performance impact considered
- [ ] Security implications reviewed
- [ ] Database migrations checked
- [ ] Breaking changes documented

## Merge Criteria

- [ ] All CI checks pass
- [ ] At least 1 approval from maintainers
- [ ] No merge conflicts
- [ ] Documentation updated
- [ ] Version number incremented (if release)

## Release Process

### Version Numbering

Follow [Semantic Versioning](https://semver.org/):
- MAJOR.MINOR.PATCH (e.g., 1.2.3)

### Release Steps

```bash
# Update version
echo "1.2.3" > VERSION

# Update CHANGELOG
# Add git tag
git tag -a v1.2.3 -m "Release version 1.2.3"

# Push to main and tag
git push origin main --tags

# Build and publish
python setup.py sdist bdist_wheel
twine upload dist/*
```

## Development Setup

### Requirements File for Development

```bash
pip install -r requirements.txt
pip install -r requirements-dev.txt
```

### Pre-commit Hooks

```bash
pip install pre-commit
pre-commit install

# .pre-commit-config.yaml
repos:
  - repo: https://github.com/psf/black
    rev: 23.1.0
    hooks:
      - id: black
  - repo: https://github.com/PyCQA/isort
    rev: 5.12.0
    hooks:
      - id: isort
  - repo: https://github.com/PyCQA/flake8
    rev: 6.0.0
    hooks:
      - id: flake8
```

## Getting Help

- **Documentation**: Check [README.md](README.md)
- **Issues**: Search [GitHub Issues](https://github.com/R-dev-07/healthhub/issues)
- **Discussions**: Join our [Discussions](https://github.com/R-dev-07/healthhub/discussions)
- **Chat**: Join our [Discord Community](https://discord.gg/your-invite)

## Recognition

Contributors will be recognized in:
- CONTRIBUTORS.md file
- Release notes
- GitHub contributors page

Thank you for contributing! 🎉
