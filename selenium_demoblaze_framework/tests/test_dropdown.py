# selenium_demoblaze_framework/tests/test_dropdowns.py

import pytest
import os
import sys
import allure
import time
import socket
import threading
import shutil
from http.server import HTTPServer, SimpleHTTPRequestHandler
from selenium.webdriver.common.by import By

# Add project root to path for imports
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from selenium_demoblaze_framework.config.browser_config import BrowserConfig
from selenium_demoblaze_framework.utilities.custom_logger import CustomLogger
from selenium_demoblaze_framework.pages.base_page import BasePage


# --- Helper function to find a free port for our local server ---
def find_free_port():
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.bind(("", 0))
        return s.getsockname()[1]


@allure.feature('Form Elements')
class TestDropdowns:
    """
    Test suite for dropdown interactions using a 100% reliable local HTML file.
    This test validates the dropdown selection methods in the BasePage class.
    """

    @pytest.fixture(autouse=True)
    def setup_and_teardown(self):
        """
        Setup fixture: Creates a local web server with a dropdown page,
        initializes the WebDriver, and handles teardown.
        """
        # --- Standard Setup ---
        self.logger = CustomLogger.get_logger(self.__class__.__name__)
        self.logger.info("=" * 50)
        self.logger.info("Starting new LOCAL Dropdown Test")

        # --- Local Web Server Setup ---
        self.temp_dir = "temp_dropdown_pages"
        os.makedirs(self.temp_dir, exist_ok=True)
        html_content = """
        <!DOCTYPE html>
        <html>
        <head><title>Local Dropdown Test</title></head>
        <body>
            <h2>Local Dropdown Test Page</h2>
            <form>
                <label for="car-select">Choose a car:</label>
                <select name="cars" id="car-select">
                    <option value="" disabled selected>--Please choose an option--</option>
                    <option value="volvo">Volvo</option>
                    <option value="saab">Saab</option>
                    <option value="mercedes">Mercedes</option>
                    <option value="audi">Audi</option>
                </select>
            </form>
            <div id="status-message" style="margin-top:20px; font-weight:bold;"></div>
            <script>
                document.getElementById('car-select').onchange = (event) => {
                    const selectedOption = event.target.options[event.target.selectedIndex];
                    document.getElementById('status-message').textContent = 
                        `Selected car: ${selectedOption.text} (value: ${selectedOption.value})`;
                };
            </script>
        </body>
        </html>
        """
        with open(os.path.join(self.temp_dir, "dropdown_test.html"), "w") as f:
            f.write(html_content)

        port = find_free_port()
        handler = lambda *args, **kwargs: SimpleHTTPRequestHandler(*args, directory=self.temp_dir, **kwargs)
        self.server = HTTPServer(("localhost", port), handler)
        self.server_thread = threading.Thread(target=self.server.serve_forever)
        self.server_thread.daemon = True
        self.server_thread.start()
        self.test_url = f"http://localhost:{port}/dropdown_test.html"
        self.logger.info(f"Local test server running at: {self.test_url}")

        # --- WebDriver Setup ---
        self.browser_config = BrowserConfig()
        self.driver = self.browser_config.get_driver()
        # We instantiate BasePage to get access to the dropdown methods
        self.base_page = BasePage(self.driver, self.logger)

        yield

        # --- Teardown ---
        self.logger.info("Dropdown Test completed")
        self.logger.info("=" * 50)
        self.driver.quit()
        self.server.shutdown()
        shutil.rmtree(self.temp_dir)  # Clean up the temp directory and HTML file

    @allure.story('Test All Dropdown Selection Methods')
    @allure.description(
        "This test verifies all three dropdown selection methods (by value, by text, and by index) "
        "from the BasePage class against a locally-hosted, 100% reliable test page.")
    def test_dropdown_selection_methods(self):
        """
        Tests selecting dropdown options using by_value, by_text, and by_index.
        """
        self.logger.info(f"Navigating to local dropdown page: {self.test_url}")
        self.driver.get(self.test_url)

        # Define locators for our local page
        DROPDOWN = (By.ID, "car-select")
        STATUS_MESSAGE = (By.ID, "status-message")

        # --- Step 1: Select by Value ---
        self.logger.info("Step 1: Selecting option by value: 'saab'")
        self.base_page.select_dropdown_by_value(DROPDOWN, "saab")
        time.sleep(0.5)  # Allow JS to update status message
        status_text_1 = self.base_page.get_text(STATUS_MESSAGE)
        assert "Selected car: Saab (value: saab)" in status_text_1
        self.logger.info(f"Verification PASSED. Status: '{status_text_1}'")
        allure.attach(self.driver.get_screenshot_as_png(), name="After_Select_By_Value",
                      attachment_type=allure.attachment_type.PNG)

        # --- Step 2: Select by Visible Text ---
        self.logger.info("Step 2: Selecting option by visible text: 'Mercedes'")
        self.base_page.select_dropdown_by_text(DROPDOWN, "Mercedes")
        time.sleep(0.5)
        status_text_2 = self.base_page.get_text(STATUS_MESSAGE)
        assert "Selected car: Mercedes (value: mercedes)" in status_text_2
        self.logger.info(f"Verification PASSED. Status: '{status_text_2}'")
        allure.attach(self.driver.get_screenshot_as_png(), name="After_Select_By_Text",
                      attachment_type=allure.attachment_type.PNG)

        # --- Step 3: Select by Index ---
        # Note: Index is 0-based. "Audi" is the 5th option, so its index is 4.
        self.logger.info("Step 3: Selecting option by index: 4 (Audi)")
        self.base_page.select_dropdown_by_index(DROPDOWN, 4)
        time.sleep(0.5)
        status_text_3 = self.base_page.get_text(STATUS_MESSAGE)
        assert "Selected car: Audi (value: audi)" in status_text_3
        self.logger.info(f"Verification PASSED. Status: '{status_text_3}'")
        allure.attach(self.driver.get_screenshot_as_png(), name="After_Select_By_Index",
                      attachment_type=allure.attachment_type.PNG)

        self.logger.info("All dropdown selection methods verified successfully!")