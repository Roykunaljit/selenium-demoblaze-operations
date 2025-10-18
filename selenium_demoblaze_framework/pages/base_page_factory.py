from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium_demoblaze_framework.utilities.page_factory import PageFactory


class BasePageFactory(PageFactory):
    """Base page class using Page Factory pattern"""

    def __init__(self, driver, logger=None):
        super().__init__(driver)
        self.driver = driver
        self.logger = logger
        self.wait = WebDriverWait(driver, 10)

    def get_page_title(self):
        """Get page title"""
        return self.driver.title

    def is_displayed(self, element):
        """Check if element is displayed"""
        try:
            return element.is_displayed()
        except:
            return False

    def is_enabled(self, element):
        """Check if element is enabled"""
        try:
            return element.is_enabled()
        except:
            return False

    def click_element(self, element):
        """Click on element"""
        try:
            element.click()
            return True
        except Exception as e:
            if self.logger:
                self.logger.error(f"Error clicking element: {str(e)}")
            return False

    def enter_text(self, element, text):
        """Enter text in element"""
        try:
            element.clear()
            element.send_keys(text)
            return True
        except Exception as e:
            if self.logger:
                self.logger.error(f"Error entering text: {str(e)}")
            return False

    def get_text(self, element):
        """Get text from element"""
        try:
            return element.text
        except:
            return ""

    def wait_for_element(self, by, value, timeout=10):
        """Wait for element to be present"""
        wait = WebDriverWait(self.driver, timeout)
        return wait.until(EC.presence_of_element_located((by, value)))

    def wait_for_element_clickable(self, by, value, timeout=10):
        """Wait for element to be clickable"""
        wait = WebDriverWait(self.driver, timeout)
        return wait.until(EC.element_to_be_clickable((by, value)))