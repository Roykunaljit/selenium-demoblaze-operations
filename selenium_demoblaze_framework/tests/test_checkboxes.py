# selenium_demoblaze_framework/tests/test_checkboxes.py

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
class TestCheckboxes:
    """
    Test suite for checkbox interactions using a 100% reliable local HTML file.
    """

    @pytest.fixture(autouse=True)
    def setup_and_teardown(self):
        """
        Setup fixture: Creates a local web server with a checkbox page,
        initializes the WebDriver, and handles teardown.
        """
        # --- Standard Setup ---
        self.logger = CustomLogger.get_logger(self.__class__.__name__)
        self.logger.info("=" * 50)
        self.logger.info("Starting new LOCAL Checkbox Test")

        # --- Local Web Server Setup ---
        self.temp_dir = "temp_test_pages"
        os.makedirs(self.temp_dir, exist_ok=True)
        html_content = """
        <!DOCTYPE html>
        <html>
        <head><title>Local Checkbox Test</title></head>
        <body>
            <h2>Local Checkbox Test Page</h2>
            <form id="checkbox-form">
                <input type="checkbox" id="checkbox1">
                <label for="checkbox1">Option 1 (Initially Unchecked)</label>
                <br>
                <input type="checkbox" id="checkbox2" checked>
                <label for="checkbox2">Option 2 (Initially Checked)</label>
            </form>
            <div id="status-message" style="margin-top:20px; font-weight:bold;"></div>
            <script>
                document.querySelectorAll('input[type=checkbox]').forEach(cb => {
                    cb.onchange = () => {
                        const c1_checked = document.getElementById('checkbox1').checked;
                        const c2_checked = document.getElementById('checkbox2').checked;
                        document.getElementById('status-message').textContent = 
                            `Checkbox 1 is ${c1_checked ? 'Checked' : 'Unchecked'}, Checkbox 2 is ${c2_checked ? 'Checked' : 'Unchecked'}.`;
                    }
                });
            </script>
        </body>
        </html>
        """
        with open(os.path.join(self.temp_dir, "checkbox_test.html"), "w") as f:
            f.write(html_content)

        port = find_free_port()
        handler = lambda *args, **kwargs: SimpleHTTPRequestHandler(*args, directory=self.temp_dir, **kwargs)
        self.server = HTTPServer(("localhost", port), handler)
        self.server_thread = threading.Thread(target=self.server.serve_forever)
        self.server_thread.daemon = True
        self.server_thread.start()
        self.test_url = f"http://localhost:{port}/checkbox_test.html"
        self.logger.info(f"Local test server running at: {self.test_url}")

        # --- WebDriver Setup ---
        self.browser_config = BrowserConfig()
        self.driver = self.browser_config.get_driver()
        self.base_page = BasePage(self.driver, self.logger)

        yield

        # --- Teardown ---
        self.logger.info("Checkbox Test completed")
        self.logger.info("=" * 50)
        self.driver.quit()
        self.server.shutdown()
        shutil.rmtree(self.temp_dir)  # Clean up the temp directory and HTML file

    @allure.story('Test Checkbox States on a Local HTML Page')
    @allure.description(
        "This test verifies checkbox functionality by checking, unchecking, and asserting states on a locally-hosted, 100% reliable test page.")
    def test_local_checkbox_interaction(self):
        """
        Tests checkbox selection and deselection on a self-hosted HTML page.
        """
        self.logger.info(f"Navigating to local checkbox page: {self.test_url}")
        self.driver.get(self.test_url)

        # Define locators for our local page
        CHECKBOX_1 = (By.ID, "checkbox1")
        CHECKBOX_2 = (By.ID, "checkbox2")
        STATUS_MESSAGE = (By.ID, "status-message")

        # --- Step 1: Verify Initial State ---
        self.logger.info("Verifying initial checkbox states")
        assert not self.base_page.is_selected(CHECKBOX_1), "Checkbox 1 should be unchecked initially"
        assert self.base_page.is_selected(CHECKBOX_2), "Checkbox 2 should be checked initially"
        self.logger.info("Initial states verified successfully.")

        # --- Step 2: Check the first checkbox ---
        self.logger.info("Clicking the first checkbox to select it")
        self.base_page.click(CHECKBOX_1)

        # --- Step 3: Uncheck the second checkbox ---
        self.logger.info("Clicking the second checkbox to deselect it")
        self.base_page.click(CHECKBOX_2)

        # Give a moment for the JS on the page to update the status message
        time.sleep(0.5)

        # --- Step 4: Verify Final State ---
        self.logger.info("Verifying final checkbox states")
        assert self.base_page.is_selected(CHECKBOX_1), "Checkbox 1 should now be checked"
        assert not self.base_page.is_selected(CHECKBOX_2), "Checkbox 2 should now be unchecked"

        # Also verify the status message that our JavaScript updates
        final_status = self.base_page.get_text(STATUS_MESSAGE)
        assert "Checkbox 1 is Checked" in final_status, "Status message did not update correctly for Checkbox 1"
        assert "Checkbox 2 is Unchecked" in final_status, "Status message did not update correctly for Checkbox 2"
        self.logger.info(f"Final states verified successfully. Status: '{final_status}'")

        allure.attach(self.driver.get_screenshot_as_png(), name="FinalLocalCheckboxState",
                      attachment_type=allure.attachment_type.PNG)