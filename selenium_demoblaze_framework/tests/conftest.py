# conftest.py
import pytest
import allure
from allure_commons.types import AttachmentType
import os
from datetime import datetime

@pytest.hookimpl(tryfirst=True, hookwrapper=True)
def pytest_runtest_makereport(item, call):
    outcome = yield
    report = outcome.get_result()

    if report.when == 'call' and report.failed:
        driver = None

        # Try multiple possible fixture names
        possible_fixtures = ['setup_and_teardown', 'setup', 'class_setup', 'test_setup']
        for fixture_name in possible_fixtures:
            if fixture_name in item.funcargs:
                fixture_value = item.funcargs[fixture_name]
                if isinstance(fixture_value, tuple) and hasattr(fixture_value[0], 'save_screenshot'):
                    driver = fixture_value[0]
                    break
                elif hasattr(fixture_value, 'save_screenshot'):
                    driver = fixture_value
                    break

        if driver:
            try:
                screenshot_dir = os.path.join(os.getcwd(), 'reports', 'screenshots')
                os.makedirs(screenshot_dir, exist_ok=True)
                timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
                filename = f"failure_{item.name}_{timestamp}.png"
                filepath = os.path.join(screenshot_dir, filename)
                driver.save_screenshot(filepath)
                allure.attach(
                    driver.get_screenshot_as_png(),
                    name=f"Screenshot on Failure: {item.name}",
                    attachment_type=AttachmentType.PNG
                )
                print(f"\n📸 Screenshot saved to {filepath}")
            except Exception as e:
                print(f"\n❗️ Screenshot failed: {e}")
        else:
            print(f"\n⚠️ No driver found for test {item.name} — skipping screenshot.")