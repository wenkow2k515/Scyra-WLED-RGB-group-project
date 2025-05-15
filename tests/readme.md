# Scyra Testing Documentation

This directory contains all the test files for the Scyra project. The tests are organized to cover different aspects of the application, from unit tests to system tests.

## Test Files Overview

### Unit Tests
- `test_auth.py`: Tests for authentication functionality
- `test_api_route.py`: Tests for API endpoints and routes
- `test_mood_utils.py`: Tests for mood analysis utilities
- `test_without_api.py`: Tests for the fallback system when API is not available

### System Tests
- `systemtest.py`: End-to-end system tests
- `tester.py`: General system testing utilities

### Test Utilities
- `controllers.py`: Test controllers and helper functions
- `__init__.py`: Test package initialization and common test configurations

## Running Tests

To run all tests:
```bash
pytest
```

To run specific test files:
```bash
pytest tests/test_auth.py
pytest tests/test_mood_utils.py
```

To run tests with coverage:
```bash
pytest --cov=app tests/
```

## Test Categories

1. **Authentication Tests**
   - User registration
   - Login functionality
   - Session management
   - Password reset

2. **API Route Tests**
   - Endpoint validation
   - Request/response handling
   - Error cases
   - Data validation

3. **Mood Analysis Tests**
   - OpenAI API integration
   - Fallback system
   - Color recommendations
   - Mood analysis accuracy

4. **System Tests**
   - End-to-end workflows
   - Integration testing
   - Performance testing
   - Error handling

## Test Environment Setup

1. Ensure you have all test dependencies installed:
```bash
pip install -r requirements.txt
```

2. Set up test environment variables:
   - Copy `.env_example` to `.env.test`
   - Configure test-specific settings

3. For API tests:
   - Set up mock API responses
   - Configure test API keys

## Writing New Tests

When adding new tests:
1. Follow the existing naming convention: `test_*.py`
2. Include both positive and negative test cases
3. Add appropriate docstrings and comments
4. Update this README if adding new test categories

## Best Practices

1. Keep tests independent and isolated
2. Use appropriate fixtures and setup/teardown
3. Mock external dependencies
4. Include meaningful assertions
5. Document complex test scenarios 