from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from selenium.common.exceptions import TimeoutException, NoSuchElementException
import time
import logging

class BasePage:
    def __init__(self, driver):
        self.driver = driver
        self.wait = WebDriverWait(driver, 10)  # 10 seconds timeout
        self.actions = ActionChains(self.driver)
        
        # Setup logging
        self.logger = logging.getLogger(__name__)
        logging.basicConfig(level=logging.INFO)

    def find_element(self, locator):
        """
        Find element with explicit wait
        :param locator: tuple of locator strategy and value (e.g., (By.ID, "example"))
        """
        try:
            element = self.wait.until(EC.presence_of_element_located(locator))
            self.logger.info(f"Found element: {locator}")
            return element
        except TimeoutException:
            self.logger.error(f"Failed to find element: {locator}")
            raise

    def find_elements(self, locator):
        """
        Find all elements matching the locator
        :param locator: tuple of locator strategy and value
        """
        try:
            elements = self.wait.until(EC.presence_of_all_elements_located(locator))
            self.logger.info(f"Found elements: {locator}")
            return elements
        except TimeoutException:
            self.logger.error(f"Failed to find elements: {locator}")
            raise

    def click_element(self, locator):
        """Find element, scroll to it, wait for it to be clickable, and click it"""
        try:
            # Find element first
            element = self.find_element(locator)
            
            # Scroll element into view
            self.scroll_to_element(element)
            
            # Wait for element to be clickable after scrolling
            clickable_element = self.wait.until(
                EC.element_to_be_clickable(locator)
            )
            
            time.sleep(1)
            clickable_element.click()
            self.logger.info(f"Clicked element: {locator}")
            
        except TimeoutException:
            self.logger.error(f"Element not clickable: {locator}")
            raise
        except Exception as e:
            self.logger.error(f"Failed to click element {locator}: {str(e)}")
            raise

    def enhanced_clear(self, element):
        """Enhanced clear method that uses multiple clearing techniques"""
        try:
            # First try the standard clear method
            element.clear()
            
            # If that doesn't work, try sending CTRL+A and DELETE
            current_value = element.get_attribute("value")
            if current_value:
                # Send CTRL+A to select all text
                element.send_keys(u'\ue009' + 'a')  # CTRL+A
                # Then send DELETE to delete the text
                element.send_keys(u'\ue017')  # DELETE key
                self.logger.info("Used enhanced clear method with keyboard shortcuts")
                
            # Check again
            if element.get_attribute("value"):
                # As a last resort, try JavaScript
                self.driver.execute_script("arguments[0].value = '';", element)
                self.logger.info("Used JavaScript to clear field")
                
            self.logger.info("Input field cleared")
        except Exception as e:
            self.logger.error(f"Failed to clear element: {str(e)}")
            raise
            
    def input_text(self, locator, text):
        """Wait for element to be clickable, scroll to it, and input text"""
        try:
            element = self.wait.until(
                EC.element_to_be_clickable(locator)
            )
            # Scroll element into view before interacting
            self.scroll_to_element(element)
            time.sleep(1)
            # Use enhanced clear instead of simple clear
            self.enhanced_clear(element)
            time.sleep(1)
            element.send_keys(text)
            self.logger.info(f"Input text '{text}' into element: {locator}")
        except TimeoutException:
            self.logger.error(f"Element not clickable for text input: {locator}")
            raise
        except Exception as e:
            self.logger.error(f"Failed to input text into element {locator}: {str(e)}")
            raise

    def get_text(self, locator):
        """
        Get text from element
        :param locator: tuple of locator strategy and value
        """
        try:
            element = self.wait.until(EC.presence_of_element_located(locator))
            text = element.text
            self.logger.info(f"Got text '{text}' from element: {locator}")
            return text
        except TimeoutException:
            self.logger.error(f"Failed to get text from element: {locator}")
            raise

    def is_element_visible(self, locator, timeout=10):
        """
        Check if element is visible
        :param locator: tuple of locator strategy and value
        :param timeout: time to wait for element
        """
        try:
            self.wait.until(EC.visibility_of_element_located(locator))
            self.logger.info(f"Element is visible: {locator}")
            return True
        except TimeoutException:
            self.logger.error(f"Element is not visible: {locator}")
            return False

    def is_element_present(self, locator, timeout=10):
        """
        Check if element is present in DOM
        :param locator: tuple of locator strategy and value
        :param timeout: time to wait for element
        """
        try:
            self.wait.until(EC.presence_of_element_located(locator))
            self.logger.info(f"Element is present: {locator}")
            return True
        except TimeoutException:
            self.logger.error(f"Element is not present: {locator}")
            return False

    def wait_for_element_to_disappear(self, locator, timeout=10):
        """
        Wait for element to disappear from DOM
        :param locator: tuple of locator strategy and value
        :param timeout: time to wait for element
        """
        try:
            self.wait.until(EC.invisibility_of_element_located(locator))
            self.logger.info(f"Element disappeared: {locator}")
            return True
        except TimeoutException:
            self.logger.error(f"Element did not disappear: {locator}")
            return False

    def get_attribute(self, locator, attribute):
        """
        Get attribute value of element
        :param locator: tuple of locator strategy and value
        :param attribute: attribute name
        """
        try:
            element = self.find_element(locator)
            value = element.get_attribute(attribute)
            self.logger.info(f"Got attribute '{attribute}' with value '{value}' from element: {locator}")
            return value
        except Exception as e:
            self.logger.error(f"Failed to get attribute '{attribute}' from element: {locator}")
            raise

    def hover_over_element(self, locator):
        """
        Hover over element
        :param locator: tuple of locator strategy and value
        """
        try:
            element = self.find_element(locator)
            self.actions.move_to_element(element).perform()
            self.logger.info(f"Hovered over element: {locator}")
        except Exception as e:
            self.logger.error(f"Failed to hover over element: {locator}")
            raise

    def scroll_to_element(self, element):
        """Scroll element into middle of the viewport"""
        try:
            # Get the height of the viewport
            viewport_height = self.driver.execute_script("return window.innerHeight")
            # Calculate the scroll position to center the element
            scroll_script = """
                let elementRect = arguments[0].getBoundingClientRect();
                let absoluteElementTop = elementRect.top + window.pageYOffset;
                let middle = absoluteElementTop - (window.innerHeight / 2);
                window.scrollTo(0, middle);
            """
            self.driver.execute_script(scroll_script, element)
            # Add small delay after scrolling
            time.sleep(1)
            self.logger.info("Scrolled element to middle of viewport")
        except Exception as e:
            self.logger.error(f"Failed to scroll to element: {str(e)}")
            raise

    def switch_to_frame(self, locator):
        """
        Switch to iframe
        :param locator: tuple of locator strategy and value
        """
        try:
            frame = self.wait.until(EC.frame_to_be_available_and_switch_to_it(locator))
            self.logger.info(f"Switched to frame: {locator}")
            return frame
        except TimeoutException:
            self.logger.error(f"Failed to switch to frame: {locator}")
            raise

    def switch_to_default_content(self):
        """Switch back to default content from iframe"""
        try:
            self.driver.switch_to.default_content()
            self.logger.info("Switched to default content")
        except Exception as e:
            self.logger.error("Failed to switch to default content")
            raise

    def accept_alert(self):
        """Accept alert"""
        try:
            alert = self.wait.until(EC.alert_is_present())
            alert.accept()
            self.logger.info("Accepted alert")
        except TimeoutException:
            self.logger.error("Failed to accept alert: No alert present")
            raise

    def dismiss_alert(self):
        """Dismiss alert"""
        try:
            alert = self.wait.until(EC.alert_is_present())
            alert.dismiss()
            self.logger.info("Dismissed alert")
        except TimeoutException:
            self.logger.error("Failed to dismiss alert: No alert present")
            raise

    def refresh_and_wait_element(self, locator, wait_time=3):
        """Refresh page and wait for element to load"""
        try:
            # Refresh the page
            self.driver.refresh()
            
            # Static wait for page load
            time.sleep(wait_time)
            
            # Wait for element to be present
            element = self.wait.until(
                EC.presence_of_element_located(locator)
            )
            
            self.logger.info(f"Page refreshed and element found: {locator}")
            return element
            
        except TimeoutException:
            self.logger.error(f"Element not found after refresh: {locator}")
            raise
        except Exception as e:
            self.logger.error(f"Error refreshing page and finding element: {str(e)}")
            raise

    def wait_for_condition(self, timeout=10, poll_frequency=0.5):
        """
        Create a new WebDriverWait instance with custom timeout
        :param timeout: time to wait in seconds
        :param poll_frequency: how often to poll in seconds
        :return: WebDriverWait instance
        """
        return WebDriverWait(self.driver, timeout, poll_frequency=poll_frequency)
