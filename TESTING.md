# Testing Guide for HealthHub

## Setting Up Tests

### Install Testing Dependencies

```bash
pip install pytest pytest-django factory-boy faker
```

### Configure pytest.ini

```ini
[pytest]
DJANGO_SETTINGS_MODULE = healthhub.settings
python_files = tests.py test_*.py *_tests.py
addopts = --verbose --strict-markers
```

## Writing Tests

### Test Structure

```python
# tests.py in each app

import pytest
from django.test import TestCase, Client
from django.contrib.auth import get_user_model
from .models import YourModel
from .factories import YourModelFactory

User = get_user_model()

class YourModelTestCase(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username='testuser',
            password='testpass123'
        )
        self.client = Client()
    
    def test_model_creation(self):
        obj = YourModelFactory()
        self.assertIsNotNone(obj.id)
    
    def test_model_str(self):
        obj = YourModelFactory()
        self.assertEqual(str(obj), expected_str)
```

### Factory Pattern

```python
# factories.py

import factory
from django.contrib.auth import get_user_model
from .models import YourModel

User = get_user_model()

class UserFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = User
    
    username = factory.Faker('user_name')
    email = factory.Faker('email')
    password = factory.PostGenerationMethodCall('set_password', 'defaultpassword')

class YourModelFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = YourModel
    
    user = factory.SubFactory(UserFactory)
    name = factory.Faker('name')
```

## Test Categories

### Unit Tests

```python
def test_patient_bmi_calculation():
    """Test BMI calculation"""
    patient = PatientFactory(weight=70, height=180)
    expected_bmi = 70 / ((180/100) ** 2)
    assert patient.calculate_bmi() == expected_bmi
```

### Integration Tests

```python
def test_appointment_booking_flow():
    """Test complete appointment booking"""
    patient = PatientFactory()
    doctor = DoctorFactory()
    
    appointment = AppointmentFactory(
        patient=patient,
        doctor=doctor
    )
    
    # Test payment
    payment = create_payment(appointment)
    assert payment.status == 'completed'
    
    assert appointment.is_paid == True
```

### API Tests

```python
def test_appointment_api_list():
    """Test appointment API list endpoint"""
    patient = PatientFactory()
    AppointmentFactory(patient=patient)
    
    client = APIClient()
    client.force_authenticate(user=patient.user)
    
    response = client.get('/api/appointments/')
    assert response.status_code == 200
    assert len(response.data) == 1
```

### View Tests

```python
def test_patient_dashboard_view():
    """Test patient dashboard view"""
    user = UserFactory(role='patient')
    patient = PatientFactory(user=user)
    
    client = Client()
    client.login(username=user.username, password='defaultpassword')
    
    response = client.get('/patients/dashboard/')
    assert response.status_code == 200
    assert response.context['patient'] == patient
```

## Running Tests

```bash
# Run all tests
python manage.py test

# Run specific app tests
python manage.py test patients

# Run specific test class
python manage.py test patients.tests.PatientModelTests

# Run with coverage
pip install coverage
coverage run --source='.' manage.py test
coverage report
coverage html  # Generate HTML report

# Run with pytest
pytest

# Run specific test file
pytest patients/tests.py

# Run with verbose output
pytest -v

# Run with coverage via pytest
pytest --cov=. --cov-report=html
```

## Code Coverage

Aim for >80% code coverage:

```bash
# Generate coverage report
coverage run --source='.' manage.py test
coverage report --omit='*/venv/*'

# HTML report
coverage html
# Open htmlcov/index.html in browser
```

## Fixtures

### Creating Test Data

```python
# fixtures/initial_data.json
[
    {
        "model": "patients.customuser",
        "pk": 1,
        "fields": {
            "username": "testuser",
            "email": "test@example.com",
            "password": "pbkdf2_sha256$...",
            "role": "patient"
        }
    }
]

# Load fixture
python manage.py loaddata initial_data
```

## Performance Testing

```python
from django.test.utils import override_settings
from django.test import TransactionTestCase

class PerformanceTests(TransactionTestCase):
    @override_settings(DEBUG=False)
    def test_query_count(self):
        with self.assertNumQueries(3):
            # Code that should execute 3 queries
            pass
```

## Mocking

```python
from unittest.mock import patch, MagicMock

def test_with_mock():
    with patch('payments.views.process_payment') as mock_payment:
        mock_payment.return_value = {'status': 'success'}
        
        # Test code
        result = some_function()
        
        # Verify mock was called
        mock_payment.assert_called_once()
```

## Continuous Integration

### GitHub Actions Example

```yaml
# .github/workflows/tests.yml
name: Tests

on: [push, pull_request]

jobs:
  test:
    runs-on: ubuntu-latest
    
    services:
      postgres:
        image: postgres:13
        env:
          POSTGRES_PASSWORD: postgres
        options: >-
          --health-cmd pg_isready
          --health-interval 10s
          --health-timeout 5s
          --health-retries 5
    
    steps:
      - uses: actions/checkout@v2
      - name: Set up Python
        uses: actions/setup-python@v2
        with:
          python-version: 3.10
      
      - name: Install dependencies
        run: pip install -r requirements.txt
      
      - name: Run tests
        run: python manage.py test
      
      - name: Upload coverage
        uses: codecov/codecov-action@v2
```

## Best Practices

1. **Test Isolation**
   - Each test should be independent
   - Use setUp/tearDown properly
   - Don't rely on test execution order

2. **Descriptive Names**
   - Use `test_<method>_<condition>_<expected_result>`
   - Example: `test_user_creation_with_valid_data_returns_user`

3. **One Assertion Per Test**
   - Keep tests focused
   - Exception: AAA (Arrange, Act, Assert) pattern acceptable

4. **Use Fixtures**
   - Avoid hardcoding test data
   - Use factories for DRY tests

5. **Mock External Services**
   - Mock API calls
   - Mock email sending
   - Mock file operations

6. **Test Edge Cases**
   - Empty data
   - Invalid input
   - Boundary conditions
   - Concurrent operations

## Test Checklist

- [ ] Models: Creation, update, deletion, validation
- [ ] Views: Access controls, response codes, context data
- [ ] Forms: Validation, cleaning, errors
- [ ] API: Authentication, permissions, data integrity
- [ ] Serializers: Serialization, deserialization
- [ ] Management Commands: Proper execution, error handling
- [ ] Signals: Proper triggering, data consistency
- [ ] Email: Proper sending, content verification
- [ ] Payments: Transaction handling, webhooks
- [ ] Chat: Message creation, WebSocket connections

## Debugging Tests

```python
# Use pdb
import pdb; pdb.set_trace()

# Use pytest fixtures
@pytest.fixture
def doctor(db):
    return DoctorFactory()

# Print debug information
print(f"Debug: {variable}")

# Use pytest markers
@pytest.mark.skip(reason="Development in progress")
def test_something():
    pass

@pytest.mark.slow
def test_slow_operation():
    pass

# Run only marked tests
pytest -m slow
```

## References

- Django Testing: https://docs.djangoproject.com/en/stable/topics/testing/
- pytest-django: https://pytest-django.readthedocs.io/
- factory_boy: https://factoryboy.readthedocs.io/
- Coverage.py: https://coverage.readthedocs.io/
