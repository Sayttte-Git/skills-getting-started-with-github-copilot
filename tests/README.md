# Test Suite for Mergington High School API

This directory contains comprehensive tests for the FastAPI application.

## Test Structure

- `conftest.py` - Pytest configuration and fixtures
- `test_api.py` - API endpoint tests

## Test Coverage

### TestGetActivities
- ✅ Get all activities
- ✅ Verify activity structure
- ✅ Check initial participants

### TestSignupForActivity
- ✅ Successful signup
- ✅ Activity not found (404)
- ✅ Duplicate signup prevention (400)
- ✅ Multiple activity signups
- ✅ URL-encoded activity names

### TestUnregisterFromActivity
- ✅ Successful unregistration
- ✅ Activity not found (404)
- ✅ Student not registered (400)
- ✅ Unregister and re-signup workflow
- ✅ URL-encoded activity names

### TestRootEndpoint
- ✅ Root redirect to static HTML

### TestIntegrationScenarios
- ✅ Complete signup/unregister workflow
- ✅ Activity capacity tracking

## Running Tests

```bash
# Run all tests
pytest tests/ -v

# Run with coverage
pytest tests/ --cov=src --cov-report=html

# Run specific test class
pytest tests/test_api.py::TestSignupForActivity -v

# Run specific test
pytest tests/test_api.py::TestSignupForActivity::test_signup_success -v
```

## Test Results

All 16 tests passing ✅
