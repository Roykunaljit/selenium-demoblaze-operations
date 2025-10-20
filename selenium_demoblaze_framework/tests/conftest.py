import pytest
import allure
from allure_commons.types import AttachmentType
import os
from datetime import datetime

@pytest.hookimpl(tryfirst=True, hookwrapper=True)
def pytest_runtest_makereport(item, call):
    """
    Hook to take screenshot on test failure for Allure reports.
    This fixture is automatically discovered and used by pytest.
    """
    # Execute all other hooks to obtain the report object
    outcome = yield
    report = outcome.get_result()

    # We only look at the final test result, which is the 'call' phase
    if report.when == 'call' and report.failed:
        try:
            # 'setup_and_teardown' is the name of the fixture that holds the driver
            # This relies on the fixture name being consistent across tests.
            driver = item.funcargs['setup_and_teardown'][0] # Access driver from yielded fixture tuple

            # Create a unique filename for the screenshot
            screenshot_dir = os.path.join(os.getcwd(), 'reports', 'screenshots')
            os.makedirs(screenshot_dir, exist_ok=True)
            timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
            filename = f"failure_{item.name}_{timestamp}.png"
            filepath = os.path.join(screenshot_dir, filename)

            # Save screenshot file
            driver.save_screenshot(filepath)

            # Attach screenshot to Allure report
            allure.attach(
                driver.get_screenshot_as_png(),
                name=f"Screenshot on Failure: {item.name}",
                attachment_type=AttachmentType.PNG
            )
            print(f"\n📸 Screenshot saved to {filepath} and attached to Allure report.")

        except Exception as e:
            print(f"\n❗️ Failed to take screenshot on failure for test {item.name}: {e}")