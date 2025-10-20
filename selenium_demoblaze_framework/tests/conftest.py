# conftest.py
import pytest
import allure
from allure_commons.types import AttachmentType
import os
from datetime import datetime


@pytest.hookimpl(tryfirst=True, hookwrapper=True)
def pytest_runtest_makereport(item, call):
    """
    Hook to take screenshot on test failure for Allure reports.
    Handles multiple fixture names and patterns.
    """
    outcome = yield
    report = outcome.get_result()

    if report.when == 'call' and report.failed:
        driver = None

        try:
            # List of possible fixture names
            fixture_names = ['setup_and_teardown', 'setup', 'driver', 'browser']

            for fixture_name in fixture_names:
                if fixture_name in item.funcargs:
                    fixture_value = item.funcargs[fixture_name]

                    # Handle different return types
                    if hasattr(fixture_value, '__self__'):
                        # It's a bound method, try to get driver from self
                        if hasattr(fixture_value.__self__, 'driver'):
                            driver = fixture_value.__self__.driver
                    elif isinstance(fixture_value, tuple):
                        # Fixture returns tuple
                        for item_in_tuple in fixture_value:
                            if hasattr(item_in_tuple, 'get_screenshot_as_png'):
                                driver = item_in_tuple
                                break
                    elif hasattr(fixture_value, 'get_screenshot_as_png'):
                        # Direct driver object
                        driver = fixture_value

                    if driver:
                        break

            # Try to get driver from test instance
            if not driver and hasattr(item, 'instance'):
                if hasattr(item.instance, 'driver'):
                    driver = item.instance.driver

            if not driver:
                print(f"\n⚠️ No driver found for screenshot in test: {item.name}")
                return

            # Create screenshot directory
            screenshot_dir = os.path.join(os.getcwd(), 'reports', 'screenshots')
            os.makedirs(screenshot_dir, exist_ok=True)

            # Generate unique filename
            timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
            filename = f"failure_{item.name}_{timestamp}.png"
            filepath = os.path.join(screenshot_dir, filename)

            # Save screenshot
            driver.save_screenshot(filepath)

            # Attach to Allure
            allure.attach(
                driver.get_screenshot_as_png(),
                name=f"Screenshot on Failure: {item.name}",
                attachment_type=AttachmentType.PNG
            )

            print(f"\n📸 Screenshot saved: {filepath}")

        except Exception as e:
            print(f"\n❗ Screenshot failed for {item.name}: {str(e)}")