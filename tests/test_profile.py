import pytest
from selenium import webdriver
from pages.LoginPage import LoginPage
from pages.ProfilePage import ProfilePage
from test_data.login_data import LoginData
from test_data.profile_data import ProfileData
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
import time
import os
from selenium.webdriver.chrome.options import Options

class TestProfile:
    @pytest.fixture(scope="function")
    def setup(self):
        # Configure Chrome options to reduce unwanted logs
        chrome_options = Options()
        chrome_options.add_experimental_option('excludeSwitches', ['enable-logging'])
        chrome_options.add_argument('--log-level=3')  # Only show fatal errors
        
        # Initialize the driver with options
        self.driver = webdriver.Chrome(options=chrome_options)
        self.driver.maximize_window()
        
        # Login first
        login_page = LoginPage(self.driver)
        self.driver.get("https://profile.w3schools.com/login")
        login_page.login(
            LoginData.VALID_CREDENTIALS["email"],
            LoginData.VALID_CREDENTIALS["password"]
        )
        
        # Wait for login redirect
        WebDriverWait(self.driver, 10).until(
            EC.url_to_be("https://pathfinder.w3schools.com/")
        )
        
        # Navigate to profile page
        self.driver.get("https://profile.w3schools.com/profile")
        
        # Add static wait for page load
        time.sleep(3)  # Wait for 3 seconds
        
        # Initialize profile page and verify
        profile_page = ProfilePage(self.driver)
        assert profile_page.is_profile_page_loaded(), "Profile page failed to load"
        
        yield self.driver
        self.driver.quit()

    @pytest.mark.profile
    def test_change_username(self, setup):
        """Test changing user's first and last name with random data"""
        profile_page = ProfilePage(self.driver)
        
        # Get random username
        random_username = ProfileData.get_random_username()
        
        assert profile_page.change_username(
            random_username['first_name'],
            random_username['last_name']
        ), f"Failed to change username to: {random_username['first_name']} {random_username['last_name']}"

    @pytest.mark.profile
    @pytest.mark.flaky(reruns=1, reruns_delay=2)
    def test_upload_profile_image(self, setup):
        """Test uploading profile image"""
        profile_page = ProfilePage(self.driver)
        
        # Get absolute path of test image
        image_path = os.path.join(os.path.dirname(__file__), "..", ProfileData.IMAGE_PATH)
        
        assert profile_page.upload_profile_image(image_path), "Failed to upload profile image"

    @pytest.mark.profile
    def test_change_profile_url(self, setup):
        """Test changing profile URL"""
        profile_page = ProfilePage(self.driver)
        
        assert profile_page.change_profile_url(
            ProfileData.NEW_URL
        ), "Failed to change profile URL"
