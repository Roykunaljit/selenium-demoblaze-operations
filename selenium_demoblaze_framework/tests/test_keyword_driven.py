# selenium_demoblaze_framework/tests/test_keyword_driven.py

import pytest
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from selenium_demoblaze_framework.utilities.keyword_engine import KeywordEngine
from selenium_demoblaze_framework.utilities.custom_logger import CustomLogger
from selenium_demoblaze_framework.config.browser_config import BrowserConfig


class TestKeywordDriven:
    @pytest.fixture
    def setup(self):
        self.logger = CustomLogger.get_logger(self.__class__.__name__)
        self.browser_config = BrowserConfig()
        self.driver = self.browser_config.get_driver()
        self.keyword_engine = KeywordEngine(self.driver)

        yield

        self.driver.quit()

    def test_keyword_driven_execution(self, setup):
        """Test keyword-driven framework execution"""

        # Get the absolute path to the Excel file
        test_dir = os.path.dirname(os.path.abspath(__file__))
        project_root = os.path.dirname(test_dir)
        excel_file_path = os.path.join(project_root, "data", "keyword_test_cases.xlsx")

        # Check if file exists
        if not os.path.exists(excel_file_path):
            pytest.skip(f"Test data file not found: {excel_file_path}")

        # Execute test case from Excel
        test_results = self.keyword_engine.execute_test_case(
            excel_file_path,
            "Sheet1"
        )

        assert len(test_results) > 0, "No test results found"

        # Generate report
        report_file = self.keyword_engine.generate_test_report(test_results)
        assert os.path.exists(report_file), "Report file not generated"

        # Log results
        failed_steps = [r for r in test_results if not r['result']]
        passed_steps = [r for r in test_results if r['result']]

        self.logger.info(f"Test completed: {len(passed_steps)} passed, {len(failed_steps)} failed")
        self.logger.info(f"Report generated at: {report_file}")

        # Only fail if there are failed steps
        if len(failed_steps) > 0:
            self.logger.error(f"Failed steps: {failed_steps}")
            pytest.fail(f"{len(failed_steps)} step(s) failed. Check report: {report_file}")

        self.logger.info("Keyword-driven test completed successfully")