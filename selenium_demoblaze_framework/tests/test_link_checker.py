# tests/test_link_checker.py
import pytest
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from selenium_demoblaze_framework.utilities.link_checker_utils import LinkCheckerUtils
from selenium_demoblaze_framework.utilities.custom_logger import CustomLogger
from selenium_demoblaze_framework.config.browser_config import BrowserConfig


class TestLinkChecker:
    @pytest.fixture
    def setup(self):
        self.logger = CustomLogger.get_logger(self.__class__.__name__)
        self.browser_config = BrowserConfig()
        self.driver = self.browser_config.get_driver()
        self.link_checker = LinkCheckerUtils(self.driver, self.logger)

        yield

        self.driver.quit()

    def test_check_all_links(self, setup):
        """Test checking all links on a page"""
        self.driver.get("https://the-internet.herokuapp.com/")

        results = self.link_checker.check_all_links()

        assert len(results) > 0, "No links found on page"

        # Generate report
        report_file = self.link_checker.generate_link_report(results)
        assert os.path.exists(report_file), "Report file not generated"

        # Print summary
        broken_links = [r for r in results if r['is_broken']]
        self.logger.info(f"Found {len(broken_links)} broken links out of {len(results)} total")

    def test_check_internal_links(self, setup):
        """Test checking only internal links"""
        self.driver.get("https://the-internet.herokuapp.com/")

        results = self.link_checker.check_internal_links_only("https://the-internet.herokuapp.com/")

        assert len(results) > 0, "No internal links found"

        for result in results:
            assert "the-internet.herokuapp.com" in result['url'] or not result['url'].startswith("http")

    def test_check_external_links(self, setup):
        """Test checking only external links"""
        self.driver.get("https://the-internet.herokuapp.com/")

        results = self.link_checker.check_external_links_only("https://the-internet.herokuapp.com/")

        # Verify all links are external
        for result in results:
            if result['url'].startswith("http"):
                assert "the-internet.herokuapp.com" not in result['url']