import pytest
import os
import sys
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from selenium_demoblaze_framework.config.browser_config import BrowserConfig
from selenium_demoblaze_framework.utilities.custom_logger import CustomLogger


class TestBase:
    @pytest.fixture(scope="class")
    def class_setup(self):
        logger = CustomLogger.get_logger("TestBase")
        browser_config = BrowserConfig()
        driver = browser_config.get_driver()

        yield driver, logger

        driver.quit()

    @pytest.fixture(scope="function")
    def test_setup(self, class_setup):
        driver, logger = class_setup
        driver.get("https://www.demoblaze.com")
        yield driver, logger