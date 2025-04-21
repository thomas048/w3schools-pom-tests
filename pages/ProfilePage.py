from .BasePage import BasePage
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
import os
import requests
import io
import time

class ProfilePage(BasePage):
    # Locators
    FIRST_NAME_INPUT = (By.XPATH, "//input[@placeholder='Add your first name']")
    LAST_NAME_INPUT = (By.XPATH, "//input[@placeholder='Add your last name']")
    SAVE_ACCOUNT_BTN = (By.XPATH, "//div[@class='Profile_action_wrapper__ohsJV']//button[@type='button'][normalize-space()='Save']")
    
    UPLOAD_IMG_INPUT = (By.ID, "profileImageInput")
    CONFIRM_EDIT_BTN = (By.XPATH, "//button[@type='button' and @class='chakra-button css-179v3qw' and normalize-space()='Confirm Edit']")
    UPLOADED_IMG = (By.XPATH, "//img[@class='chakra-avatar__img css-3a5bz2']")
    SUCCESS_TOAST = (By.XPATH, "//div[contains(@class, 'chakra-alert') and @data-status='success']")
    SUCCESS_TOAST_MESSAGE = (By.XPATH, "//div[contains(@class, 'chakra-alert__desc') and contains(text(), 'successfully')]")
    
    # Error toast notification
    ERROR_TOAST = (By.XPATH, "//div[contains(@class, 'chakra-alert') and @data-status='error']")
    ERROR_TOAST_MESSAGE = (By.XPATH, "//div[contains(@id, 'toast') and contains(@id, 'description')]")
    
    URL_INPUT = (By.XPATH, "//input[@id='contact']")
    SAVE_PROFILE_BTN = (By.XPATH, "//button[@type='button' and @class='chakra-button css-1rpa6kk' and contains(., 'Save')]")
    CONFIRM_YES_BTN = (By.XPATH, "//button[@type='button' and contains(@class, 'css-134g1j9') and normalize-space()='Continue']")
    
    def change_username(self, first_name, last_name):
        """Change user's first and last name"""
        try:
            # Input new names
            self.input_text(self.FIRST_NAME_INPUT, first_name)
            self.input_text(self.LAST_NAME_INPUT, last_name)
            
            # Click only if button is enabled
            self.click_element(self. SAVE_ACCOUNT_BTN)
            
            # Use refresh_and_wait_element
            self.refresh_and_wait_element(self.FIRST_NAME_INPUT)
            
            # Get current values after refresh
            current_first_name = self.find_element(self.FIRST_NAME_INPUT).get_attribute("value")
            current_last_name = self.find_element(self.LAST_NAME_INPUT).get_attribute("value")
            
            # Verify values match what was input
            if current_first_name == first_name and current_last_name == last_name:
                self.logger.info(f"Successfully changed username to: {first_name} {last_name}")
                return True
            else:
                self.logger.error(f"Username change failed. Expected: {first_name} {last_name}, Got: {current_first_name} {current_last_name}")
                return False
                
        except Exception as e:
            self.logger.error(f"Failed to change username: {str(e)}")
            raise

    def handle_edit_image_popup(self):
        """Handle the Edit Image popup by clicking Confirm Edit"""
        try:
            # Wait for Confirm Edit button to be visible and clickable
            self.wait.until(EC.element_to_be_clickable(self.CONFIRM_EDIT_BTN))
            # Click Confirm Edit button
            self.click_element(self.CONFIRM_EDIT_BTN)
            self.logger.info("Successfully confirmed image edit")
            return True
        except Exception as e:
            self.logger.error(f"Failed to handle Edit Image popup: {str(e)}")
            raise

    def upload_profile_image(self, image_path):
        """Upload profile image and verify it"""
        try:
            # Find the hidden file input and send the file path directly
            file_input = self.find_element(self.UPLOAD_IMG_INPUT)
            absolute_path = os.path.abspath(image_path)
            file_input.send_keys(absolute_path)
            
            # Handle Edit Image popup
            if not self.handle_edit_image_popup():
                return False
                
            # Toast detection with appropriate timeout
            try:
                # Use longer wait time for toast to appear
                wait_long = self.wait_for_condition(timeout=10)
                
                # Wait for success toast - this is the only reliable verification
                wait_long.until(EC.visibility_of_element_located(self.SUCCESS_TOAST))
                success_message = self.find_element(self.SUCCESS_TOAST_MESSAGE).text
                self.logger.info(f"Success toast displayed: {success_message}")
                return True
            except Exception:
                # Check for error toast to provide better diagnostics
                try:
                    wait_long = self.wait_for_condition(timeout=5)
                    wait_long.until(EC.visibility_of_element_located(self.ERROR_TOAST))
                    error_message = self.find_element(self.ERROR_TOAST_MESSAGE).text
                    self.logger.error(f"Error toast displayed: {error_message}")
                    
                    # Handle specific error cases with more detailed logging
                    if "limit exceeded" in error_message.lower():
                        self.logger.error("Upload failed due to limit exceeded")
                except Exception:
                    self.logger.error("No success or error toast detected - image upload likely failed")
                
                return False
                
        except Exception as e:
            self.logger.error(f"Failed to upload profile image: {str(e)}")
            raise

    def handle_confirmation_dialog(self):
        """Handle the confirmation dialog by clicking Yes"""
        try:
            # Wait for Continue button to be visible and clickable
            self.wait.until(EC.element_to_be_clickable(self.CONFIRM_YES_BTN))
            # Click Continue button
            self.click_element(self.CONFIRM_YES_BTN)
            self.logger.info("Successfully confirmed dialog")
            return True
        except Exception as e:
            self.logger.error(f"Failed to handle confirmation dialog: {str(e)}")
            raise

    def change_profile_url(self, new_url):
        """Change public profile URL"""
        try:
            self.input_text(self.URL_INPUT, new_url)
            self.click_element(self.SAVE_PROFILE_BTN)
            
            # Handle confirmation dialog
            if not self.handle_confirmation_dialog():
                return False
            
            # Refresh and wait for profile URL to load
            self.refresh_and_wait_element(self.URL_INPUT)
            
            # Verify URL value after refresh
            current_url = self.find_element(self.URL_INPUT).get_attribute("value")
            if current_url == new_url:
                self.logger.info(f"Successfully changed and verified profile URL to: {new_url}")
                return True
            else:
                self.logger.error("Profile URL change did not persist after refresh")
                return False
                
        except Exception as e:
            self.logger.error(f"Failed to change profile URL: {str(e)}")
            raise

    def is_profile_page_loaded(self):
        """Verify profile page is loaded"""
        return self.is_element_visible(self.FIRST_NAME_INPUT)
