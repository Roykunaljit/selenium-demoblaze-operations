# keywords/keywords.py
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select
from selenium.webdriver.common.action_chains import ActionChains
import time


class Keywords:
    def __init__(self, driver, logger):
        self.driver = driver
        self.logger = logger

    def navigate_to_url(self, url):
        """Navigate to specified URL"""
        self.driver.get(url)
        self.logger.info(f"Navigated to: {url}")
        return True

    def click_element(self, locator_type, locator_value):
        """Click on element"""
        try:
            element = self.driver.find_element(getattr(By, locator_type.upper()), locator_value)
            element.click()
            self.logger.info(f"Clicked element: {locator_type}={locator_value}")
            return True
        except Exception as e:
            self.logger.error(f"Failed to click element: {str(e)}")
            return False

    def enter_text(self, locator_type, locator_value, text):
        """Enter text in input field"""
        try:
            element = self.driver.find_element(getattr(By, locator_type.upper()), locator_value)
            element.clear()
            element.send_keys(text)
            self.logger.info(f"Entered text in {locator_type}={locator_value}: {text}")
            return True
        except Exception as e:
            self.logger.error(f"Failed to enter text: {str(e)}")
            return False

    def select_dropdown(self, locator_type, locator_value, option_type, option_value):
        """Select dropdown option"""
        try:
            element = self.driver.find_element(getattr(By, locator_type.upper()), locator_value)
            select = Select(element)

            if option_type.lower() == "text":
                select.select_by_visible_text(option_value)
            elif option_type.lower() == "value":
                select.select_by_value(option_value)
            elif option_type.lower() == "index":
                select.select_by_index(int(option_value))

            self.logger.info(f"Selected dropdown option: {option_type}={option_value}")
            return True
        except Exception as e:
            self.logger.error(f"Failed to select dropdown: {str(e)}")
            return False

    def verify_element_present(self, locator_type, locator_value):
        """Verify element is present"""
        try:
            self.driver.find_element(getattr(By, locator_type.upper()), locator_value)
            self.logger.info(f"Element present: {locator_type}={locator_value}")
            return True
        except:
            self.logger.info(f"Element not present: {locator_type}={locator_value}")
            return False

    def verify_text(self, locator_type, locator_value, expected_text):
        """Verify text of element"""
        try:
            element = self.driver.find_element(getattr(By, locator_type.upper()), locator_value)
            actual_text = element.text
            result = expected_text in actual_text
            self.logger.info(f"Text verification - Expected: {expected_text}, Actual: {actual_text}, Result: {result}")
            return result
        except Exception as e:
            self.logger.error(f"Failed to verify text: {str(e)}")
            return False

    def wait_for_element(self, locator_type, locator_value, timeout=10):
        """Wait for element to be present"""
        from selenium.webdriver.support.ui import WebDriverWait
        from selenium.webdriver.support import expected_conditions as EC

        try:
            WebDriverWait(self.driver, timeout).until(
                EC.presence_of_element_located((getattr(By, locator_type.upper()), locator_value))
            )
            self.logger.info(f"Element found after wait: {locator_type}={locator_value}")
            return True
        except:
            self.logger.error(f"Element not found after wait: {locator_type}={locator_value}")
            return False

    def scroll_to_element(self, locator_type, locator_value):
        """Scroll to element"""
        try:
            element = self.driver.find_element(getattr(By, locator_type.upper()), locator_value)
            self.driver.execute_script("arguments[0].scrollIntoView(true);", element)
            self.logger.info(f"Scrolled to element: {locator_type}={locator_value}")
            return True
        except Exception as e:
            self.logger.error(f"Failed to scroll to element: {str(e)}")
            return False

    def take_screenshot(self, filename):
        """Take screenshot"""
        try:
            self.driver.save_screenshot(f"screenshots/{filename}.png")
            self.logger.info(f"Screenshot saved: {filename}.png")
            return True
        except Exception as e:
            self.logger.error(f"Failed to take screenshot: {str(e)}")
            return False

    def switch_to_frame(self, frame_identifier):
        """Switch to frame"""
        try:
            self.driver.switch_to.frame(frame_identifier)
            self.logger.info(f"Switched to frame: {frame_identifier}")
            return True
        except Exception as e:
            self.logger.error(f"Failed to switch to frame: {str(e)}")
            return False

    def switch_to_default_content(self):
        """Switch to default content"""
        self.driver.switch_to.default_content()
        self.logger.info("Switched to default content")
        return True

    def handle_alert(self, action):
        """Handle alert (accept/dismiss)"""
        try:
            alert = self.driver.switch_to.alert
            if action.lower() == "accept":
                alert.accept()
                self.logger.info("Alert accepted")
            elif action.lower() == "dismiss":
                alert.dismiss()
                self.logger.info("Alert dismissed")
            return True
        except Exception as e:
            self.logger.error(f"Failed to handle alert: {str(e)}")
            return False

    def get_page_title(self):
        """Get page title"""
        title = self.driver.title
        self.logger.info(f"Page title: {title}")
        return title

    def refresh_page(self):
        """Refresh page"""
        self.driver.refresh()
        self.logger.info("Page refreshed")
        return True

    def mouse_hover(self, locator_type, locator_value):
        """Mouse hover on element"""
        try:
            element = self.driver.find_element(getattr(By, locator_type.upper()), locator_value)
            actions = ActionChains(self.driver)
            actions.move_to_element(element).perform()
            self.logger.info(f"Mouse hovered on: {locator_type}={locator_value}")
            return True
        except Exception as e:
            self.logger.error(f"Failed to mouse hover: {str(e)}")
            return False

    def double_click(self, locator_type, locator_value):
        """Double click on element"""
        try:
            element = self.driver.find_element(getattr(By, locator_type.upper()), locator_value)
            actions = ActionChains(self.driver)
            actions.double_click(element).perform()
            self.logger.info(f"Double clicked: {locator_type}={locator_value}")
            return True
        except Exception as e:
            self.logger.error(f"Failed to double click: {str(e)}")
            return False

    def right_click(self, locator_type, locator_value):
        """Right click on element"""
        try:
            element = self.driver.find_element(getattr(By, locator_type.upper()), locator_value)
            actions = ActionChains(self.driver)
            actions.context_click(element).perform()
            self.logger.info(f"Right clicked: {locator_type}={locator_value}")
            return True
        except Exception as e:
            self.logger.error(f"Failed to right click: {str(e)}")
            return False