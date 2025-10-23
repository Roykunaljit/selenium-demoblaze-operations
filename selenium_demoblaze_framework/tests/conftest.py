# conftest.py
import pytest
import allure
from allure_commons.types import AttachmentType
import os
from datetime import datetime
import threading

# Thread-safe screenshot counter
screenshot_lock = threading.Lock()
screenshot_counter = {}


def pytest_addoption(parser):
    """Add command line options for browser selection."""
    parser.addoption(
        "--browser",
        action="store",
        default="chrome",
        help="Browser to run tests: chrome, edge, or all"
    )


def pytest_generate_tests(metafunc):
    """Generate test combinations for different browsers."""
    if "browser_name" in metafunc.fixturenames:
        browser_option = metafunc.config.getoption("--browser").lower()

        if browser_option == "all":
            browsers = ["chrome", "edge"]
        else:
            browsers = [browser_option]

        metafunc.parametrize("browser_name", browsers, scope="function")


@pytest.hookimpl(tryfirst=True, hookwrapper=True)
def pytest_runtest_makereport(item, call):
    """
    Hook to take screenshot on test failure for Allure reports.
    Handles multiple fixture names and patterns.
    Thread-safe implementation for parallel execution.
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

            # Create screenshot directory (thread-safe)
            screenshot_dir = os.path.join(os.getcwd(), 'reports', 'screenshots')
            os.makedirs(screenshot_dir, exist_ok=True)

            # Generate unique filename with thread-safe counter
            with screenshot_lock:
                thread_id = threading.current_thread().ident
                if thread_id not in screenshot_counter:
                    screenshot_counter[thread_id] = 0
                screenshot_counter[thread_id] += 1
                counter = screenshot_counter[thread_id]

            timestamp = datetime.now().strftime('%Y%m%d_%H%M%S_%f')
            worker_id = os.environ.get('PYTEST_XDIST_WORKER', 'master')

            # Get browser name from test parameters
            browser_name = "unknown"
            if hasattr(item, 'callspec') and 'browser_name' in item.callspec.params:
                browser_name = item.callspec.params['browser_name']

            filename = f"failure_{browser_name}_{item.name}_{worker_id}_{timestamp}_{counter}.png"
            filepath = os.path.join(screenshot_dir, filename)

            # Save screenshot
            driver.save_screenshot(filepath)

            # Attach to Allure
            allure.attach(
                driver.get_screenshot_as_png(),
                name=f"Screenshot [{browser_name}] {item.name}",
                attachment_type=AttachmentType.PNG
            )

            print(f"\n📸 Screenshot saved: {filepath}")

        except Exception as e:
            print(f"\n❗ Screenshot failed for {item.name}: {str(e)}")


@pytest.hookimpl(tryfirst=True)
def pytest_configure(config):
    """Configure pytest with custom markers."""
    config.addinivalue_line(
        "markers", "chrome: mark test to run only on Chrome"
    )
    config.addinivalue_line(
        "markers", "edge: mark test to run only on Edge"
    )
    config.addinivalue_line(
        "markers", "smoke: mark test as smoke test"
    )
    config.addinivalue_line(
        "markers", "regression: mark test as regression test"
    )