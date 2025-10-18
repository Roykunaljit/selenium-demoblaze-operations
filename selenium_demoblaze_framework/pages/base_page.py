# pages/base_page.py

from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import Select
from selenium.common.exceptions import *
from selenium.webdriver.support.wait import WebDriverWait
import time
import os


class BasePage:
    def __init__(self, driver, logger):
        """Initialize BasePage with WebDriver and logger."""
        self.driver = driver
        self.logger = logger
        self.wait = WebDriverWait(
            driver,
            20,
            poll_frequency=0.5,
            ignored_exceptions=[
                NoSuchElementException,
                ElementNotVisibleException,
                ElementNotSelectableException
            ]
        )

    def find_element(self, locator, timeout=20):
        """Find a single element with explicit wait."""
        try:
            element = WebDriverWait(self.driver, timeout).until(
                EC.presence_of_element_located(locator)
            )
            self.logger.info(f"Found element: {locator}")
            return element
        except TimeoutException:
            self.logger.error(f"Element not found: {locator}")
            raise

    def find_elements(self, locator, timeout=20):
        """Find multiple elements with explicit wait."""
        try:
            elements = WebDriverWait(self.driver, timeout).until(
                EC.presence_of_all_elements_located(locator)
            )
            self.logger.info(f"Found {len(elements)} elements: {locator}")
            return elements
        except TimeoutException:
            self.logger.error(f"Elements not found: {locator}")
            return []

    def click(self, locator):
        """Click an element, with fallback to JavaScript click if needed."""
        try:
            element = WebDriverWait(self.driver, 20).until(
                EC.element_to_be_clickable(locator)
            )
            element.click()
            self.logger.info(f"Clicked element: {locator}")
        except Exception as e:
            self.logger.error(f"Failed to click element: {locator}. Error: {str(e)}")
            # Fallback: JavaScript click
            element = self.find_element(locator)
            self.driver.execute_script("arguments[0].click();", element)
            self.logger.info(f"Clicked element using JavaScript: {locator}")

    def double_click(self, locator):
        """Perform a double-click on an element."""
        element = self.find_element(locator)
        actions = ActionChains(self.driver)
        actions.double_click(element).perform()
        self.logger.info(f"Double clicked element: {locator}")

    def right_click(self, locator):
        """Perform a right-click (context click) on an element."""
        element = self.find_element(locator)
        actions = ActionChains(self.driver)
        actions.context_click(element).perform()
        self.logger.info(f"Right clicked element: {locator}")

    def hover(self, locator):
        """Hover over an element."""
        element = self.find_element(locator)
        actions = ActionChains(self.driver)
        actions.move_to_element(element).perform()
        self.logger.info(f"Hovered over element: {locator}")

    def drag_and_drop(self, source_locator, target_locator):
        """Drag an element and drop it onto another."""
        source = self.find_element(source_locator)
        target = self.find_element(target_locator)
        actions = ActionChains(self.driver)
        actions.drag_and_drop(source, target).perform()
        self.logger.info(f"Dragged from {source_locator} to {target_locator}")

    def drag_and_drop_by_offset(self, locator, x_offset, y_offset):
        """Drag an element by a specified offset."""
        element = self.find_element(locator)
        actions = ActionChains(self.driver)
        actions.drag_and_drop_by_offset(element, x_offset, y_offset).perform()
        self.logger.info(f"Dragged element {locator} by offset ({x_offset}, {y_offset})")

    def send_keys(self, locator, text, clear_first=True):
        """Send text to an input field."""
        element = self.wait.until(EC.visibility_of_element_located(locator))
        if clear_first:
            element.clear()
        element.send_keys(text)
        self.logger.info(f"Sent keys to element {locator}: {text}")

    def send_keys_slowly(self, locator, text, delay=0.1):
        """Send keys one character at a time with a delay (useful for flaky inputs)."""
        element = self.find_element(locator)
        element.clear()
        for char in text:
            element.send_keys(char)
            time.sleep(delay)
        self.logger.info(f"Sent keys slowly to element {locator}: {text}")

    def press_key(self, locator, key):
        """Press a special key (e.g., ENTER, TAB) on an element."""
        element = self.find_element(locator)
        element.send_keys(key)
        self.logger.info(f"Pressed key {key} on element: {locator}")

    def key_combination(self, locator, *keys):
        """Perform a key combination (e.g., Ctrl+C)."""
        element = self.find_element(locator)
        actions = ActionChains(self.driver)
        actions.move_to_element(element)
        for key in keys[:-1]:
            actions.key_down(key)
        actions.send_keys(keys[-1])
        for key in keys[:-1]:
            actions.key_up(key)
        actions.perform()
        self.logger.info(f"Pressed key combination on element {locator}: {keys}")

    def get_text(self, locator):
        """Get visible text from an element."""
        element = self.find_element(locator)
        text = element.text
        self.logger.info(f"Got text from element {locator}: {text}")
        return text

    def get_attribute(self, locator, attribute):
        """Get the value of a specified attribute from an element."""
        element = self.find_element(locator)
        value = element.get_attribute(attribute)
        self.logger.info(f"Got attribute '{attribute}' from element {locator}: {value}")
        return value

    def get_css_property(self, locator, property_name):
        """Get the value of a CSS property from an element."""
        element = self.find_element(locator)
        value = element.value_of_css_property(property_name)
        self.logger.info(f"Got CSS property '{property_name}' from element {locator}: {value}")
        return value

    def is_displayed(self, locator):
        """Check if an element is displayed (visible)."""
        try:
            element = self.find_element(locator, timeout=5)
            return element.is_displayed()
        except (TimeoutException, NoSuchElementException):
            return False

    def is_enabled(self, locator):
        """Check if an element is enabled."""
        element = self.find_element(locator)
        return element.is_enabled()

    def is_selected(self, locator):
        """Check if an element (e.g., checkbox) is selected."""
        element = self.find_element(locator)
        return element.is_selected()

    def wait_for_element_visible(self, locator, timeout=20):
        """Wait until an element is visible."""
        WebDriverWait(self.driver, timeout).until(
            EC.visibility_of_element_located(locator)
        )
        self.logger.info(f"Element is visible: {locator}")

    def wait_for_element_invisible(self, locator, timeout=20):
        """Wait until an element is no longer visible."""
        WebDriverWait(self.driver, timeout).until(
            EC.invisibility_of_element_located(locator)
        )
        self.logger.info(f"Element is invisible: {locator}")

    def wait_for_text_present(self, locator, text, timeout=20):
        """Wait until specific text appears inside an element."""
        WebDriverWait(self.driver, timeout).until(
            EC.text_to_be_present_in_element(locator, text)
        )
        self.logger.info(f"Text '{text}' is present in element: {locator}")

    def select_dropdown_by_value(self, locator, value):
        """Select a dropdown option by its 'value' attribute."""
        element = self.find_element(locator)
        select = Select(element)
        select.select_by_value(value)
        self.logger.info(f"Selected dropdown option by value '{value}': {locator}")

    def select_dropdown_by_text(self, locator, text):
        """Select a dropdown option by its visible text."""
        element = self.find_element(locator)
        select = Select(element)
        select.select_by_visible_text(text)
        self.logger.info(f"Selected dropdown option by text '{text}': {locator}")

    def select_dropdown_by_index(self, locator, index):
        """Select a dropdown option by its index (0-based)."""
        element = self.find_element(locator)
        select = Select(element)
        select.select_by_index(index)
        self.logger.info(f"Selected dropdown option by index {index}: {locator}")

    def get_dropdown_options(self, locator):
        """Get all visible text options from a dropdown."""
        element = self.find_element(locator)
        select = Select(element)
        options = [option.text for option in select.options]
        self.logger.info(f"Got dropdown options from {locator}: {options}")
        return options

    def switch_to_frame(self, frame):
        """Switch WebDriver context into an iframe (by name, id, WebElement, or index)."""
        self.driver.switch_to.frame(frame)
        self.logger.info(f"Switched to frame: {frame}")

    def switch_to_default_content(self):
        """Switch back to the main document (out of iframes)."""
        self.driver.switch_to.default_content()
        self.logger.info("Switched to default content")

    def switch_to_window(self, window_handle):
        """Switch to a specific browser window/tab by handle."""
        self.driver.switch_to.window(window_handle)
        self.logger.info(f"Switched to window: {window_handle}")

    def get_current_window_handle(self):
        """Get the handle of the current window/tab."""
        return self.driver.current_window_handle

    def get_all_window_handles(self):
        """Get handles of all open windows/tabs."""
        return self.driver.window_handles

    def accept_alert(self, timeout=10):
        """Accept a JavaScript alert and return its text."""
        try:
            WebDriverWait(self.driver, timeout).until(EC.alert_is_present())
            alert = self.driver.switch_to.alert
            alert_text = alert.text
            alert.accept()
            self.logger.info(f"Accepted alert with text: {alert_text}")
            return alert_text
        except TimeoutException:
            self.logger.warning("No alert present")
            return None

    def dismiss_alert(self, timeout=10):
        """Dismiss (cancel) a JavaScript alert and return its text."""
        try:
            WebDriverWait(self.driver, timeout).until(EC.alert_is_present())
            alert = self.driver.switch_to.alert
            alert_text = alert.text
            alert.dismiss()
            self.logger.info(f"Dismissed alert with text: {alert_text}")
            return alert_text
        except TimeoutException:
            self.logger.warning("No alert present")
            return None

    def send_keys_to_alert(self, text, timeout=10):
        """Send text to a prompt alert and accept it."""
        try:
            WebDriverWait(self.driver, timeout).until(EC.alert_is_present())
            alert = self.driver.switch_to.alert
            alert.send_keys(text)
            alert.accept()
            self.logger.info(f"Sent keys to alert: {text}")
        except TimeoutException:
            self.logger.warning("No alert present")

    def get_cookies(self):
        """Get all cookies from the current session."""
        cookies = self.driver.get_cookies()
        self.logger.info(f"Got {len(cookies)} cookies")
        return cookies

    def add_cookie(self, cookie_dict):
        """Add a cookie (must be on the same domain)."""
        self.driver.add_cookie(cookie_dict)
        self.logger.info(f"Added cookie: {cookie_dict}")

    def delete_cookie(self, name):
        """Delete a cookie by name."""
        self.driver.delete_cookie(name)
        self.logger.info(f"Deleted cookie: {name}")

    def delete_all_cookies(self):
        """Delete all cookies."""
        self.driver.delete_all_cookies()
        self.logger.info("Deleted all cookies")

    def refresh_page(self):
        """Refresh the current page."""
        self.driver.refresh()
        self.logger.info("Page refreshed")

    def go_back(self):
        """Navigate to the previous page in history."""
        self.driver.back()
        self.logger.info("Navigated back")

    def go_forward(self):
        """Navigate to the next page in history."""
        self.driver.forward()
        self.logger.info("Navigated forward")

    def get_page_source(self):
        """Get the full HTML source of the current page."""
        return self.driver.page_source

    def get_current_url(self):
        """Get the current URL."""
        url = self.driver.current_url
        self.logger.info(f"Current URL: {url}")
        return url

    def get_title(self):
        """Get the current page title."""
        title = self.driver.title
        self.logger.info(f"Page title: {title}")
        return title