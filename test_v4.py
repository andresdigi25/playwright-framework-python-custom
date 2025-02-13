import pytest
from v4 import UIFramework, CONFIG

@pytest.fixture
def ui():
    """
    Pytest fixture to initialize the UIFramework before each test and close it after.
    """
    ui_instance = UIFramework(headless=True)  # Use headless mode for testing
    yield ui_instance
    ui_instance.close()

def test_open_url_and_take_screenshot(ui):
    """
    Test that opens a URL from the config, takes a screenshot,
    and asserts that the page content contains an HTML tag.
    """
    # Open the URL from your configuration file
    ui.open_url(CONFIG['test_url'])
    
    # Optionally, wait for an element here if needed, e.g.:
    # ui.wait_for_element("body")
    
    # Take a screenshot (it will be saved with a timestamped filename)
    ui.take_screenshot()
    
    # Verify that the page content contains <html> (simple check to ensure page loaded)
    content = ui.page.content()
    assert "<html" in content.lower()

def test_api_test(ui):
    """
    Test the API endpoint using run_api_test.
    If the response status is not 200, an AssertionError will be raised.
    """
    ui.run_api_test("https://jsonplaceholder.typicode.com/posts/1", 200)

def test_api_meaning_of_life(ui):
    """
    Test the API endpoint using run_api_test.
    If the response status is not 200, an AssertionError will be raised.
    """
    ui.run_api_test("https://jsonplaceholder.typicode.com/posts/42", 200)

def test_generate_fake_data(ui):
    """
    Test that verifies the generated fake data contains expected keys.
    """
    fake_data = ui.generate_fake_data()
    # Check that the fake data contains the necessary keys
    assert "name" in fake_data
    assert "email" in fake_data
    assert "address" in fake_data
    assert "phone" in fake_data
