# Climate Action Orchestrator Tests

This directory contains tests for the Climate Action Orchestrator.

## Test Scripts

- `verify_installation.py`: Verifies that the Climate Action Orchestrator is properly installed and configured
- `test_data_collection.py`: Tests the data collection agent functionality
- `test_carbon_calculation.py`: Tests the carbon calculation agent functionality
- `test_recommendation.py`: Tests the recommendation agent functionality
- `test_simulation.py`: Tests the simulation agent functionality
- `test_reporting.py`: Tests the reporting agent functionality
- `test_orchestrator.py`: Tests the main orchestrator functionality

## Running Tests

You can run all tests with:

```bash
pytest
```

Or run a specific test:

```bash
python -m tests.verify_installation
```

## Adding New Tests

When adding new tests, please follow these guidelines:

1. Create a new file named `test_*.py`
2. Use pytest fixtures for setup and teardown
3. Document each test function with a clear docstring
4. Ensure tests are independent and can be run in any order
