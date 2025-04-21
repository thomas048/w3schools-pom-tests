import pytest
from selenium import webdriver
from pages.LoginPage import LoginPage
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from test_data.login_data import LoginData  # Import test data
from selenium.webdriver.chrome.options import Options

class TestLogin:
    @pytest.fixture(scope="function")
    def setup(self):
        # Configure Chrome options to reduce unwanted logs
        chrome_options = Options()
        chrome_options.add_experimental_option('excludeSwitches', ['enable-logging'])
        chrome_options.add_argument('--log-level=3')  # Only show fatal errors
        
        # Initialize the driver with options
        self.driver = webdriver.Chrome(options=chrome_options)
        self.driver.maximize_window()
        yield self.driver
        self.driver.quit()

    @pytest.mark.login
    def test_successful_login(self, setup):
        """Test successful login with valid credentials"""
        login_page = LoginPage(self.driver)
        
        self.driver.get("https://profile.w3schools.com/login")
        
        login_page.login(
            LoginData.VALID_CREDENTIALS["email"], 
            LoginData.VALID_CREDENTIALS["password"]
        )
        
        WebDriverWait(self.driver, 10).until(
            EC.url_to_be("https://pathfinder.w3schools.com/")
        )

    @pytest.mark.login
    @pytest.mark.parametrize("email, password, expected_error", LoginData.INVALID_EMAIL_FORMATS)
    def test_invalid_login_format(self, setup, email, password, expected_error):
        """Test login with invalid email formats"""
        login_page = LoginPage(self.driver)
        
        self.driver.get("https://profile.w3schools.com/login")
        
        login_page.login(email, password)
        
        error_message = login_page.get_error_message()
        assert expected_error in error_message, f"Expected error '{expected_error}' not found in '{error_message}'"

    @pytest.mark.login
    def test_invalid_login_empty(self, setup):
        """Test login with empty credentials"""
        login_page = LoginPage(self.driver)
        
        self.driver.get("https://profile.w3schools.com/login")
        
        login_page.login(
            LoginData.EMPTY_CREDENTIALS["email"], 
            LoginData.EMPTY_CREDENTIALS["password"]
        )
        
        error_message = login_page.get_error_message()
        assert LoginData.EMPTY_CREDENTIALS["error"] in error_message
