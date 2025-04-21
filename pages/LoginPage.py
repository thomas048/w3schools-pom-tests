from pages.BasePage import BasePage  # Direct import since files are in same directory
from selenium.webdriver.common.by import By
import time

class LoginPage(BasePage):
    # Locators
    USERNAME_INPUT = (By.XPATH, "//input[@placeholder='email']")
    PASSWORD_INPUT = (By.XPATH, "//input[@placeholder='password']")
    LOGIN_BUTTON = (By.XPATH, "//button[normalize-space()='Login']")
    ERROR_MESSAGE = (By.XPATH, "//div[@class='LoginForm_error_text__4fzmN']")

    def enter_username(self, username):
        """Enter username in the username field"""
        self.input_text(self.USERNAME_INPUT, username)
        return self

    def enter_password(self, password):
        """Enter password in the password field""" # Mask password in logs
        self.input_text(self.PASSWORD_INPUT, password)
        return self

    def click_login_button(self):
        """Click on the login button"""
        self.click_element(self.LOGIN_BUTTON)
        return self

    def get_error_message(self):
        """Get error message text if present"""
        try:
            error_text = self.get_text(self.ERROR_MESSAGE)
            self.logger.warning(f"Login error detected: {error_text}")
            return error_text
        except Exception as e:
            self.logger.info("No error message found")
            return ""
    
    def login(self, username, password, max_attempts=2, wait_between_attempts=1):
        """
        Perform login action with verification and retry mechanism
        :param username: User email/username to login with
        :param password: User password
        :param max_attempts: Maximum number of attempts to verify login page is displayed
        :param wait_between_attempts: Wait time between attempts in seconds
        """
        self.logger.info(f"Attempting to login with username: {username}")
        
        # Verify login page is fully loaded before proceeding
        login_page_loaded = False
        attempt = 0
        
        while attempt < max_attempts and not login_page_loaded:
            attempt += 1
            self.logger.info(f"Verifying login page is displayed (attempt {attempt}/{max_attempts})")
            login_page_loaded = self.is_login_page_displayed()
            
            if login_page_loaded:
                self.logger.info("Login page verified, proceeding with login")
                break
            elif attempt < max_attempts:
                self.logger.warning(f"Login page not fully loaded, waiting {wait_between_attempts}s before retry")
                time.sleep(wait_between_attempts)
                # Try refreshing the page if it's not loaded correctly
                if attempt > 1:
                    self.logger.info("Refreshing page to attempt reload")
                    self.driver.refresh()
        
        if not login_page_loaded:
            self.logger.error(f"Failed to verify login page after {max_attempts} attempts")
            # Take screenshot for debugging
            try:
                timestamp = time.strftime("%Y%m%d-%H%M%S")
                screenshot_path = f"reports/screenshots/login_page_error_{timestamp}.png"
                self.driver.save_screenshot(screenshot_path)
                self.logger.info(f"Error screenshot saved to {screenshot_path}")
            except Exception as e:
                self.logger.error(f"Failed to save error screenshot: {str(e)}")
            
            return self
        
        # Proceed with login
        self.enter_username(username)
        self.enter_password(password)
        self.click_login_button()
        
        # Check if we got redirected (success) or if we have an error message
        current_url = self.driver.current_url
        self.logger.info(f"After login attempt, current URL: {current_url}")
        
        if "login" not in current_url.lower():
            self.logger.info("Login successful - redirected away from login page")
        else:
            error = self.get_error_message()
            if error:
                self.logger.warning(f"Login failed with error: {error}")
            else:
                self.logger.warning("Login failed without specific error message")
        
        return self

    def is_login_page_displayed(self):
        """Check if login page is displayed"""
        username_visible = self.is_element_visible(self.USERNAME_INPUT)
        password_visible = self.is_element_visible(self.PASSWORD_INPUT)
        
        if username_visible and password_visible:
            self.logger.info("Login page is displayed")
        else:
            self.logger.warning("Login page elements not fully visible")
            
        return username_visible and password_visible