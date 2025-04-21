# W3Schools Automation Testing Project (POM)

This project is an automation testing framework designed with the Page Object Model (POM) pattern, specifically for testing the login and profile functionality of the W3Schools website.

## Project Structure

```
└── POM/
    ├── pages/           # Page object classes
    │   ├── BasePage.py  # Base page class
    │   ├── LoginPage.py # Login page class
    │   └── ProfilePage.py # Profile page class
    │
    ├── test_data/       # Test data
    │   ├── login_data.py  # Login test data
    │   ├── profile_data.py # Profile test data
    │   └── images/        # Test images
    │       └── profile.jpg # Profile test image
    │
    ├── tests/           # Test cases
    │   ├── test_login.py  # Login tests
    │   └── test_profile.py # Profile tests
    │
    ├── reports/         # Test reports
    │   └── screenshots/ # Test failure screenshots
    │
    ├── conftest.py      # Pytest configuration file
    ├── pytest.ini       # Pytest ini configuration
    ├── run_tests.py     # Test runner script
    ├── verify_setup.py  # Setup verification script
    └── requirements.txt # Dependencies
```

## Installation

1. Ensure you have Python 3.7+ and pip installed

2. Clone the repository
```
git clone <repository-url>
cd POM
```

3. Install all dependencies
```
pip install -r requirements.txt
```

4. Verify installation
```
python verify_setup.py
```

## Setting Up Test Data

Configure your test account in `test_data/login_data.py`:

```python
VALID_CREDENTIALS = {
    "email": "your-email@example.com",
    "password": "your-password"
}
```

## Running Tests

### Using the Run Script (Recommended)
The easiest way to run tests is using the included run script:

```bash
# Run all tests
python run_tests.py

# Run only login tests
python run_tests.py --login

# Run only profile tests
python run_tests.py --profile

# Run tests with automatic retry on failure
python run_tests.py --rerun

# Generate HTML report
python run_tests.py --report

# Generate specific report for login tests
python run_tests.py --login --report  # Creates reports/login_report.html

# Generate specific report for profile tests
python run_tests.py --profile --report  # Creates reports/profile_report.html
```

### Running with pytest directly
You can also run tests directly with pytest:

```bash
# Run all tests
python -m pytest -v

# Run specific test sets
python -m pytest -m login -v           # Only run login tests
python -m pytest -m profile -v         # Only run profile tests

# Enable automatic retry of failed tests
python -m pytest --reruns 2

# Generate HTML report
python -m pytest -v --html=reports/report.html
```

## Framework Features

1. **Page Object Model (POM)**: Separates page operations from test logic
2. **Centralized Configuration**: Manages test setup through `conftest.py` and `pytest.ini`
3. **HTML Reports**: Generates detailed reports using pytest-html
4. **Failure Retry**: Supports automatic retry of failed tests via pytest-rerunfailures
5. **Screenshot Capture**: Automatically captures screenshots for failed tests
6. **Flexible Test Runner**: Built-in test runner script (`run_tests.py`) with command-line options for test selection, reporting, and retry behavior
7. **Environment Verification**: Setup verification script (`verify_setup.py`) ensures all dependencies are properly installed

## Dependencies

The project uses the following main dependencies:

- Selenium 4.0.0+: Browser automation
- pytest 7.0.0+: Testing framework
- pytest-html: HTML report generation
- webdriver-manager: Browser driver management
- requests: HTTP request handling

See `requirements.txt` for a detailed list of dependencies.

## Advanced Features

### Automatic Retry for Flaky Tests
Some tests may be unstable due to network or timing issues. These tests can be marked as "flaky" and will be automatically retried when they fail:

```python
@pytest.mark.flaky(reruns=2, reruns_delay=2)
def test_something_unstable(self):
    # This test will be retried up to 2 times if it fails
    pass
```

You can also enable retries for all tests:
```bash
python run_tests.py --rerun
```

### Pytest Configuration
The `pytest.ini` file provides project-wide configuration for pytest:

```ini
[pytest]
# Test markers definition
markers =
    login: mark test as login test
    profile: mark test as profile test
    flaky: mark test as flaky, will be retried on failure

# Default retry configuration
reruns = 1
reruns_delay = 1

# Logging settings
log_cli = True
log_cli_level = INFO
```

This configuration file controls test discovery, marker definitions, default retry behavior, and logging settings.

### Screenshot Capture on Failure
When tests fail, screenshots are automatically captured and saved to the `reports/screenshots` directory. These screenshots are also embedded in the HTML report for easy viewing.

The screenshot file names include the test name and timestamp, following this format:
```
testname_YYYYMMDD_HHMMSS.png
```

For example:
```
test_login_invalid_credentials_20230415_143022.png
```

Screenshots can be accessed in two ways:
1. Directly from the `reports/screenshots` directory
2. Through the HTML report - click on a failed test to view the attached screenshot

This feature helps with debugging by providing visual evidence of the application state at the time of failure.

## Report Screenshot
![2025-04-21 21 57 42](https://github.com/user-attachments/assets/b3da82d3-ebb5-428a-85f3-a4d508931c73)
