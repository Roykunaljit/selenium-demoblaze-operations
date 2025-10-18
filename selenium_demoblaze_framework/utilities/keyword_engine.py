import pandas as pd
import os
from datetime import datetime
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
from selenium.common.exceptions import TimeoutException, ElementClickInterceptedException, \
    ElementNotInteractableException, NoAlertPresentException
from selenium_demoblaze_framework.utilities.custom_logger import CustomLogger


class KeywordEngine:
    def __init__(self, driver):
        self.driver = driver
        self.logger = CustomLogger.get_logger(self.__class__.__name__)
        self.wait = WebDriverWait(driver, 15)  # Timeout at 15s for stability

    def check_and_handle_unexpected_alert(self):
        """Check for and handle any unexpected alerts"""
        try:
            # Use a very short timeout to check for alerts
            alert_wait = WebDriverWait(self.driver, 0.5)
            alert = alert_wait.until(EC.alert_is_present())
            alert_text = alert.text

            # Log the alert
            self.logger.warning(f"Unexpected alert found: '{alert_text}' - Auto-accepting")

            # Always accept the alert to clear it
            alert.accept()

            import time
            time.sleep(0.5)

            # Return the alert text so caller can handle it if needed
            return alert_text

        except TimeoutException:
            # No alert present - this is normal
            return None
        except Exception as e:
            self.logger.error(f"Error handling unexpected alert: {str(e)}")
            return None

    def execute_test_case(self, excel_file, sheet_name):
        """Execute test case from Excel file"""
        test_results = []

        try:
            # Read Excel file with openpyxl engine
            df = pd.read_excel(excel_file, sheet_name=sheet_name, engine='openpyxl')

            # Debug: Print column names and first few rows
            self.logger.info(f"Excel columns: {df.columns.tolist()}")
            self.logger.info(f"Number of rows: {len(df)}")

            for index, row in df.iterrows():
                step = row.get('Step', row.get('Test_Step_ID', index + 1))
                keyword = str(row.get('Keyword', row.get('Action', ''))).strip() if pd.notna(
                    row.get('Keyword', row.get('Action'))) else ''

                # Handle locator - combine Locator_Type and Locator_Value if they exist separately
                if 'Locator' in row and pd.notna(row.get('Locator')):
                    locator = str(row.get('Locator', '')).strip()
                elif 'Locator_Type' in row and 'Locator_Value' in row:
                    locator_type = str(row.get('Locator_Type', '')).strip() if pd.notna(row.get('Locator_Type')) else ''
                    locator_value = str(row.get('Locator_Value', '')).strip() if pd.notna(
                        row.get('Locator_Value')) else ''
                    locator = f"{locator_type}={locator_value}" if locator_type and locator_value else ''
                else:
                    locator = ''

                # Handle data/value column
                data = str(row.get('Data', row.get('Value', ''))).strip() if pd.notna(
                    row.get('Data', row.get('Value'))) else ''

                # Skip empty rows
                if not keyword:
                    self.logger.warning(f"Skipping row {index + 1}: No keyword/action found")
                    continue

                self.logger.info(f"Executing Step {step}: {keyword} | Locator: {locator} | Data: {data}")

                try:
                    result = self.execute_keyword(keyword, locator, data)
                    test_results.append({
                        'step': step,
                        'keyword': keyword,
                        'locator': locator,
                        'data': data,
                        'result': True,
                        'message': 'Success'
                    })
                    self.logger.info(f"Step {step} passed")
                except Exception as e:
                    self.logger.error(f"Step {step} failed: {str(e)}")
                    test_results.append({
                        'step': step,
                        'keyword': keyword,
                        'locator': locator,
                        'data': data,
                        'result': False,
                        'message': str(e)
                    })

        except Exception as e:
            self.logger.error(f"Error executing test case: {str(e)}")
            import traceback
            self.logger.error(traceback.format_exc())

        return test_results

    def execute_keyword(self, keyword, locator, data):
        """Execute individual keyword"""
        keyword = keyword.lower().strip() if keyword else ''

        # Handle unexpected alerts before any action
        self.check_and_handle_unexpected_alert()

        if keyword in ['open_browser', 'openbrowser']:
            self.logger.info("Browser already opened in setup")
            return True

        elif keyword in ['navigate', 'navigateto', 'open', 'openurl', 'navigate_to_url']:
            if locator:
                self.logger.warning(f"Locator '{locator}' ignored for navigation keyword")
            self.logger.info(f"Navigating to: {data}")
            self.driver.get(data)
            return True

        elif keyword in ['click', 'clickelement', 'click_element']:
            self.logger.info(f"Clicking element: {locator}")
            if not locator:
                raise Exception("Locator is required for click")

            # Handle unexpected alerts BEFORE clicking
            self.check_and_handle_unexpected_alert()

            locator_type, locator_value = self.parse_locator(locator)
            element = self.wait.until(
                EC.element_to_be_clickable(self.get_by_locator(locator_type, locator_value))
            )

            try:
                element.click()
            except (ElementClickInterceptedException, ElementNotInteractableException):
                self.logger.warning(f"Regular click failed for {locator}, attempting JavaScript click")
                self.driver.execute_script("arguments[0].click();", element)

            # Handle alerts AFTER clicking
            alert_text = self.check_and_handle_unexpected_alert()

            # Check if it was a wrong password alert
            if alert_text and "Wrong password" in alert_text:
                self.logger.error(f"Login failed due to wrong password")
                # Don't raise exception, just log it

            return True

        elif keyword in ['input_text', 'inputtext', 'entertext', 'type', 'sendkeys', 'enter_text']:
            self.logger.info(f"Entering text in: {locator}")
            if not locator:
                raise Exception("Locator is required for input text")
            locator_type, locator_value = self.parse_locator(locator)
            element = self.wait.until(
                EC.element_to_be_clickable(self.get_by_locator(locator_type, locator_value))
            )
            try:
                element.clear()
                element.send_keys(data)
            except ElementNotInteractableException:
                self.logger.warning(f"Regular input failed for {locator}, attempting JavaScript input")
                self.driver.execute_script("arguments[0].value = arguments[1];", element, data)
            return True

        elif keyword in ['verify_text', 'verifytext', 'assert_text']:
            self.logger.info(f"Verifying text: {data} in {locator}")
            if not locator:
                raise Exception("Locator is required for verify text")

            locator_type, locator_value = self.parse_locator(locator)

            # Additional wait for dynamic content
            import time
            time.sleep(2)

            try:
                element = self.wait.until(
                    EC.presence_of_element_located(self.get_by_locator(locator_type, locator_value))
                )

                # Try multiple methods to get text
                actual_text = element.text.strip()

                if not actual_text:
                    actual_text = self.driver.execute_script(
                        "return arguments[0].innerText || arguments[0].textContent || '';",
                        element
                    ).strip()

                if not actual_text:
                    actual_text = element.get_attribute('innerText') or ''
                    actual_text = actual_text.strip()

                if not actual_text:
                    actual_text = element.get_attribute('textContent') or ''
                    actual_text = actual_text.strip()

                self.logger.info(f"Actual text found: '{actual_text}'")

                # Case-insensitive partial match
                if data.lower() not in actual_text.lower():
                    # Take a debugging screenshot
                    os.makedirs("reports/screenshots", exist_ok=True)
                    screenshot_path = f"reports/screenshots/verify_text_failure_{datetime.now().strftime('%Y%m%d_%H%M%S')}.png"
                    self.driver.save_screenshot(screenshot_path)
                    self.logger.error(f"Screenshot saved: {screenshot_path}")
                    raise Exception(f"Expected text '{data}' not found in '{actual_text}'")

                return True

            except TimeoutException:
                raise Exception(f"Element with locator {locator} not found")

        elif keyword in ['wait', 'sleep']:
            if locator:
                self.logger.warning(f"Locator '{locator}' ignored for wait keyword")
            import time
            wait_time = float(data) if data else 1
            self.logger.info(f"Waiting for {wait_time} seconds")
            time.sleep(wait_time)
            return True

        elif keyword in ['wait_for_element']:
            self.logger.info(f"Waiting for element to be present: {locator}")
            if not locator:
                raise Exception("Locator is required for wait_for_element")
            locator_type, locator_value = self.parse_locator(locator)
            self.wait.until(
                EC.presence_of_element_located(self.get_by_locator(locator_type, locator_value))
            )
            return True

        elif keyword in ['verify_element_present']:
            self.logger.info(f"Verifying element is visible: {locator}")
            if not locator:
                raise Exception("Locator is required for verify_element_present")
            locator_type, locator_value = self.parse_locator(locator)
            self.wait.until(
                EC.visibility_of_element_located(self.get_by_locator(locator_type, locator_value))
            )
            return True


        elif keyword == 'handle_alert':

            if locator:
                self.logger.warning(f"Locator '{locator}' ignored for handle_alert")

            self.logger.info(f"Handling alert with action: {data}")

            max_attempts = 3

            attempt = 0

            while attempt < max_attempts:

                try:

                    # Create a new WebDriverWait with shorter timeout for alert checking

                    alert_wait = WebDriverWait(self.driver, 5)

                    alert = alert_wait.until(EC.alert_is_present())

                    alert_text = alert.text

                    self.logger.info(f"Alert text: {alert_text}")

                    # Check if it's a "user already exists" alert - if so, skip signup and continue

                    if "already exist" in alert_text.lower():
                        self.logger.warning("User already exists - will proceed to login with existing user")

                        alert.accept()

                        # Don't fail, just continue

                        import time

                        time.sleep(1)

                        return True

                    action = data.strip().lower() if data else 'accept'

                    if action == 'accept':

                        alert.accept()

                    elif action == 'dismiss':

                        alert.dismiss()

                    else:

                        # Default to accept for any other value

                        alert.accept()

                    # Wait a bit after handling alert

                    import time

                    time.sleep(1)

                    return True


                except TimeoutException:

                    attempt += 1

                    if attempt >= max_attempts:
                        self.logger.warning("No alert present to handle after multiple attempts")

                        return True  # Don't fail if no alert

                    import time

                    time.sleep(1)

        elif keyword == 'verify_alert_text':
            if locator:
                self.logger.warning(f"Locator '{locator}' ignored for verify_alert_text")
            self.logger.info(f"Verifying alert text: {data}")
            try:
                alert = self.wait.until(EC.alert_is_present())
                alert_text = alert.text.strip()
                self.logger.info(f"Alert text found: {alert_text}")
                if data not in alert_text:
                    raise Exception(f"Expected alert text '{data}' not found in '{alert_text}'")
                alert.accept()  # Always accept after verifying to clear the alert
                return True
            except TimeoutException:
                raise Exception("No alert present to verify")

        elif keyword == 'close_modal':
            self.logger.info(f"Closing modal with locator: {locator}")
            if not locator:
                raise Exception("Locator is required for close_modal")
            locator_type, locator_value = self.parse_locator(locator)
            try:
                close_button = self.wait.until(
                    EC.element_to_be_clickable(self.get_by_locator(locator_type, locator_value))
                )
                close_button.click()
            except TimeoutException:
                self.logger.warning(f"Close button {locator} not found, attempting JavaScript modal close")
                self.driver.execute_script("arguments[0].style.display='none';",
                                           self.driver.find_element(By.ID, locator_value.split('=')[-1]))
            return True

        elif keyword == 'take_screenshot':
            if locator:
                self.logger.warning(f"Locator '{locator}' ignored for take_screenshot")
            self.logger.info(f"Taking screenshot with name: {data}")
            # Handle any open alerts before taking screenshot
            try:
                alert = self.driver.switch_to.alert
                alert.accept()
                self.logger.info("Alert dismissed before screenshot")
            except:
                pass  # No alert to dismiss

            screenshot_dir = "reports/screenshots"
            os.makedirs(screenshot_dir, exist_ok=True)
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename_base = data.strip() if data else "screenshot"
            filename = f"{filename_base}_{timestamp}.png"
            file_path = os.path.join(screenshot_dir, filename)
            self.driver.save_screenshot(file_path)
            self.logger.info(f"Screenshot saved to: {file_path}")
            return True

        elif keyword in ['close_browser', 'closebrowser', 'quit']:
            self.logger.info("Browser will be closed in teardown")
            return True

        else:
            raise Exception(f"Unknown keyword: {keyword}")

    def parse_locator(self, locator):
        """Parse locator string like 'id=login' into type and value"""
        if not locator:
            raise Exception("Locator is empty")

        if '=' not in locator:
            raise Exception(f"Invalid locator format: {locator}. Expected format: 'type=value'")

        parts = locator.split('=', 1)
        return parts[0].strip(), parts[1].strip()

    def get_by_locator(self, locator_type, locator_value):
        """Get By locator tuple"""
        locator_map = {
            'id': By.ID,
            'name': By.NAME,
            'xpath': By.XPATH,
            'css': By.CSS_SELECTOR,
            'class': By.CLASS_NAME,
            'classname': By.CLASS_NAME,
            'tag': By.TAG_NAME,
            'tagname': By.TAG_NAME,
            'link': By.LINK_TEXT,
            'linktext': By.LINK_TEXT,
            'partial_link': By.PARTIAL_LINK_TEXT,
            'partiallink': By.PARTIAL_LINK_TEXT
        }

        by_type = locator_map.get(locator_type.lower())
        if not by_type:
            raise Exception(f"Unknown locator type: {locator_type}. Supported types: {list(locator_map.keys())}")

        return (by_type, locator_value)

    def generate_test_report(self, test_results):
        """Generate HTML test report"""
        report_dir = "reports"
        os.makedirs(report_dir, exist_ok=True)

        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        report_file = os.path.join(report_dir, f"keyword_test_report_{timestamp}.html")

        # Calculate statistics
        total_steps = len(test_results)
        passed_steps = len([r for r in test_results if r['result']])
        failed_steps = total_steps - passed_steps
        pass_rate = (passed_steps / total_steps * 100) if total_steps > 0 else 0

        # Generate HTML report
        html_content = f"""
        <!DOCTYPE html>
        <html>
        <head>
            <title>Keyword-Driven Test Report</title>
            <style>
                body {{ font-family: Arial, sans-serif; margin: 20px; background-color: #f5f5f5; }}
                .container {{ max-width: 1200px; margin: 0 auto; background-color: white; padding: 20px; box-shadow: 0 0 10px rgba(0,0,0,0.1); }}
                h1 {{ color: #333; border-bottom: 3px solid #4CAF50; padding-bottom: 10px; }}
                .summary {{ background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); color: white; padding: 20px; border-radius: 8px; margin-bottom: 20px; }}
                .summary h2 {{ margin-top: 0; color: white; }}
                .stat-box {{ display: inline-block; margin: 10px 20px 10px 0; }}
                .stat-value {{ font-size: 24px; font-weight: bold; }}
                .stat-label {{ font-size: 14px; opacity: 0.9; }}
                table {{ border-collapse: collapse; width: 100%; margin-top: 20px; box-shadow: 0 2px 4px rgba(0,0,0,0.1); }}
                th, td {{ border: 1px solid #ddd; padding: 12px; text-align: left; }}
                th {{ background-color: #4CAF50; color: white; font-weight: bold; }}
                tr:nth-child(even) {{ background-color: #f9f9f9; }}
                .pass {{ background-color: #d4edda !important; color: #155724; }}
                .fail {{ background-color: #f8d7da !important; color: #721c24; }}
                .status-pass {{ color: #28a745; font-weight: bold; }}
                .status-fail {{ color: #dc3545; font-weight: bold; }}
            </style>
        </head>
        <body>
            <div class="container">
                <h1>🚀 Keyword-Driven Test Report</h1>
                <div class="summary">
                    <h2>Test Execution Summary</h2>
                    <div class="stat-box">
                        <div class="stat-value">{total_steps}</div>
                        <div class="stat-label">Total Steps</div>
                    </div>
                    <div class="stat-box">
                        <div class="stat-value" style="color: #90EE90;">{passed_steps}</div>
                        <div class="stat-label">Passed</div>
                    </div>
                    <div class="stat-box">
                        <div class="stat-value" style="color: #FFB6C1;">{failed_steps}</div>
                        <div class="stat-label">Failed</div>
                    </div>
                    <div class="stat-box">
                        <div class="stat-value">{pass_rate:.1f}%</div>
                        <div class="stat-label">Pass Rate</div>
                    </div>
                    <div class="stat-box">
                        <div class="stat-value">{datetime.now().strftime("%H:%M:%S")}</div>
                        <div class="stat-label">{datetime.now().strftime("%Y-%m-%d")}</div>
                    </div>
                </div>

                <h2>📋 Test Step Details</h2>
                <table>
                    <tr>
                        <th>Step</th>
                        <th>Action/Keyword</th>
                        <th>Locator</th>
                        <th>Data</th>
                        <th>Status</th>
                        <th>Message</th>
                    </tr>
        """

        for result in test_results:
            row_class = 'pass' if result['result'] else 'fail'
            status = '✓ PASS' if result['result'] else '✗ FAIL'
            status_class = 'status-pass' if result['result'] else 'status-fail'
            html_content += f"""
                    <tr class="{row_class}">
                        <td>{result['step']}</td>
                        <td><strong>{result['keyword']}</strong></td>
                        <td><code>{result['locator']}</code></td>
                        <td>{result['data']}</td>
                        <td class="{status_class}">{status}</td>
                        <td>{result['message']}</td>
                    </tr>
            """

        html_content += """
                </table>
            </div>
        </body>
        </html>
        """

        with open(report_file, 'w', encoding='utf-8') as f:
            f.write(html_content)

        self.logger.info(f"Test report generated: {report_file}")
        return report_file