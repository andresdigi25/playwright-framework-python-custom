
## UIFramework Class

The `UIFramework` class (defined in `ui_framework.py`) provides a range of methods for both UI and API testing:

- **UI Automation:**
  - `open_url(url)`: Opens a given URL in the browser.
  - `click(selector)`: Clicks an element identified by a CSS selector.
  - `fill(selector, text)`: Fills an input field with text.
  - `take_screenshot(filename)`: Takes a screenshot of the current page.
  - `wait_for_element(selector, timeout)`: Waits until an element is visible on the page.
  - `close()`: Closes the browser and stops Playwright.

- **API Testing:**
  - `request_api(url, method, data, headers)`: Performs an API request.
  - `validate_api_response(url, expected_status, method, data, headers)`: Checks if an API call returns the expected HTTP status.
  - `validate_json_schema(response, schema)`: Validates an API response against a JSON Schema.

- **Utilities:**
  - `generate_fake_data()`: Generates fake data using Faker.
  - `parallel_execution(test_functions)`: Executes multiple test functions in parallel.
  - `run_ui_test(test_func)`: Runs a UI test and captures errors (including screenshots).
  - Logging is integrated into each method to help with debugging.

## Tests

The tests are written using `pytest` and are located in `test_ui_framework.py`. The test cases include:

1. **UI Test: Open URL and Take Screenshot**  
   - Opens the URL specified in `config.yaml`.
   - Takes a screenshot.
   - Checks that the page content includes the `<html>` tag, indicating that the page loaded correctly.

2. **API Test**  
   - Calls an API endpoint and verifies that the returned HTTP status is 200.

3. **Fake Data Generation Test**  
   - Validates that the fake data generated contains keys like `name`, `email`, `address`, and `phone`.

## CI/CD Integration with GitHub Actions

A GitHub Actions workflow is set up to run the tests automatically on every push or pull request to the `main` branch. The workflow file is located at `.github/workflows/ci.yml` and performs the following steps:

1. **Checkout the Repository**  
   Uses the `actions/checkout@v2` action to clone the repository.

2. **Set Up Python Environment**  
   Uses the `actions/setup-python@v2` action to install Python (version 3.8 in this example).

3. **Install Dependencies**  
   Installs required dependencies from `requirements.txt` and downloads Playwright browser binaries using `playwright install`.

4. **Run Tests**  
   Executes the tests with `pytest`.
    pytest --maxfail=1 --disable-warnings -q -v 
    

### Example GitHub Actions Workflow (`.github/workflows/ci.yml`)

```yaml
name: CI Pipeline

on:
  push:
    branches: [main]
  pull_request:
    branches: [main]

jobs:
  test:
    runs-on: ubuntu-latest

    steps:
      - name: Checkout repository
        uses: actions/checkout@v2

      - name: Set up Python
        uses: actions/setup-python@v2
        with:
          python-version: '3.8'

      - name: Install dependencies
        run: |
          python -m pip install --upgrade pip
          pip install -r requirements.txt
          playwright install

      - name: Run tests
        run: |
          pytest --maxfail=1 --disable-warnings -q
