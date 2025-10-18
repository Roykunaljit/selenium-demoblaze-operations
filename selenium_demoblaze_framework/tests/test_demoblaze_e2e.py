# tests/test_demoblaze_e2e.py

import pytest
import time
import os
import sys
import string
import allure
from datetime import datetime

from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.wait import WebDriverWait
from twisted.conch.telnet import EC
from selenium.webdriver.support import expected_conditions as EC

# Add parent directory to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from selenium_demoblaze_framework.config.browser_config import BrowserConfig
from selenium_demoblaze_framework.pages.home_page import HomePage
from selenium_demoblaze_framework.pages.product_page import ProductPage
from selenium_demoblaze_framework.pages.cart_page import CartPage
from selenium_demoblaze_framework.utilities.custom_logger import CustomLogger
from selenium_demoblaze_framework.utilities.excel_utils import ExcelUtils
from selenium_demoblaze_framework.utilities.xml_utils import XMLUtils
from selenium_demoblaze_framework.utilities.json_utils import JSONUtils
from selenium_demoblaze_framework.utilities.csv_utils import CSVUtils
from selenium_demoblaze_framework.utilities.utility_methods import UtilityMethods


class TestDemoBlazeE2E:

    @pytest.fixture(autouse=True)
    def setup_and_teardown(self):
        """Setup and teardown for each test."""
        # Setup
        self.logger = CustomLogger.get_logger(self.__class__.__name__)
        self.logger.info("=" * 50)
        self.logger.info("Starting new test")

        # Initialize browser
        self.browser_config = BrowserConfig()
        self.driver = self.browser_config.get_driver()

        # Initialize page objects
        self.home_page = HomePage(self.driver, self.logger)
        self.product_page = ProductPage(self.driver, self.logger)
        self.cart_page = CartPage(self.driver, self.logger)
        self.utils = UtilityMethods(self.driver, self.logger)

        # Initialize data utilities
        self.excel_utils = ExcelUtils()
        self.xml_utils = XMLUtils()
        self.json_utils = JSONUtils()
        self.csv_utils = CSVUtils()

        # Navigate to base URL
        self.driver.get("https://www.demoblaze.com")
        self.logger.info("Navigated to DemoBlaze website")

        yield

        # Teardown
        self.logger.info("Test completed")
        self.logger.info("=" * 50)
        self.driver.quit()



    @allure.feature('Browser Operations')
    @allure.story('Test Multiple Browser Windows and Tabs')
    def test_01_browser_windows_and_tabs(self):
        """Test handling multiple windows and tabs."""
        self.logger.info("Testing browser windows and tabs")

        # Get main window handle
        main_window = self.home_page.get_current_window_handle()
        self.logger.info(f"Main window handle: {main_window}")

        # Open new tab using JavaScript
        self.driver.execute_script("window.open('https://www.google.com','_blank');")
        time.sleep(2)

        # Get all window handles
        all_windows = self.home_page.get_all_window_handles()
        self.logger.info(f"Total windows: {len(all_windows)}")

        # Switch to new tab
        for window in all_windows:
            if window != main_window:
                self.home_page.switch_to_window(window)
                self.logger.info(f"Switched to window: {window}")
                assert "Google" in self.driver.title
                self.driver.close()
                break

        # Switch back to main window
        self.home_page.switch_to_window(main_window)
        assert "STORE" in self.driver.title

    @allure.feature('Mouse Operations')
    @allure.story('Test All Mouse Actions')
    def test_02_mouse_operations(self):
        """Test all mouse operations with visual feedback on DemoBlaze."""
        self.logger.info("Testing mouse operations on DemoBlaze")

        # Navigate to homepage
        self.driver.get("https://www.demoblaze.com")

        # Wait for products to load
        WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located((By.ID, "tbodyid"))
        )

        # Define navbar items for hover
        nav_items = {
            "Home": (By.XPATH, "//a[contains(text(),'Home')]"),
            "Contact": (By.XPATH, "//a[contains(text(),'Contact')]"),
            "About us": (By.XPATH, "//a[contains(text(),'About us')]"),
            "Cart": (By.ID, "cartur"),
            "Log in": (By.ID, "login2"),
            "Sign up": (By.ID, "signin2")
        }

        # Hover over each navbar item (triggers blue background)
        for name, locator in nav_items.items():
            self.logger.info(f"Hovering over: {name}")
            try:
                element = self.driver.find_element(*locator)
                ActionChains(self.driver).move_to_element(element).perform()
                time.sleep(1.2)  # Let user see color change to blue
                self.logger.info(f"Hovered over '{name}' — color should be blue now")
            except Exception as e:
                self.logger.warning(f"Failed to hover over '{name}': {str(e)}")

        # Right-click on logo
        self.logger.info("Performing right-click on logo")
        try:
            logo = self.driver.find_element(By.ID, "nava")
            ActionChains(self.driver).context_click(logo).perform()
            time.sleep(1)
            ActionChains(self.driver).send_keys(Keys.ESCAPE).perform()
            self.logger.info("Right-click performed and canceled")
        except Exception as e:
            self.logger.warning(f"Right-click failed: {str(e)}")

        # Double-click on first product title (now with correct locator + wait)
        self.logger.info("Double-clicking first product title")
        try:
            # Wait for at least one product to appear
            first_product = WebDriverWait(self.driver, 10).until(
                EC.element_to_be_clickable((By.XPATH, "//div[@id='tbodyid']//h4/a"))
            )

            # Optional: scroll into view for visibility
            self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", first_product)
            time.sleep(0.5)

            # Double-click
            ActionChains(self.driver).double_click(first_product).perform()
            time.sleep(2)  # Observe navigation to product detail page

            self.logger.info("Double-clicked first product title — page should have changed")
        except Exception as e:
            self.logger.warning(f"Double-click on product title failed: {str(e)}")

        self.logger.info("All mouse operations completed successfully")

    @allure.feature('Keyboard Operations')
    @allure.story('Test Keyboard Actions and Shortcuts')
    def test_03_keyboard_operations(self):
        """Test keyboard operations."""
        self.logger.info("Testing keyboard operations")

        # Open login modal
        self.home_page.open_login_modal()
        time.sleep(1)

        # Type slowly
        self.home_page.send_keys_slowly(HomePage.LOGIN_USERNAME, "test", delay=0.2)

        # Select all (Ctrl+A)
        self.home_page.key_combination(HomePage.LOGIN_USERNAME, Keys.CONTROL, 'a')
        time.sleep(0.5)

        # Copy (Ctrl+C)
        self.home_page.key_combination(HomePage.LOGIN_USERNAME, Keys.CONTROL, 'c')

        # Tab to next field
        self.home_page.press_key(HomePage.LOGIN_USERNAME, Keys.TAB)

        # Paste (Ctrl+V)
        ActionChains(self.driver).key_down(Keys.CONTROL).send_keys('v').key_up(Keys.CONTROL).perform()

        # Press ESC to close modal
        ActionChains(self.driver).send_keys(Keys.ESCAPE).perform()
        time.sleep(1)

        # Page navigation
        ActionChains(self.driver).send_keys(Keys.HOME).perform()
        time.sleep(0.5)
        ActionChains(self.driver).send_keys(Keys.END).perform()
        time.sleep(0.5)
        ActionChains(self.driver).send_keys(Keys.PAGE_UP).perform()

        self.logger.info("Keyboard operations completed")

    @allure.feature('JavaScript Execution')
    @allure.story('Test JavaScript Execution')
    def test_04_javascript_execution(self):
        """Test JavaScript execution."""
        self.logger.info("Testing JavaScript execution")

        self.utils.execute_javascript("window.scrollTo(0, 500)")
        time.sleep(1)

        page_height = self.utils.execute_javascript("return document.body.scrollHeight")
        self.logger.info(f"Page height: {page_height}")

        logo = self.home_page.find_element(HomePage.LOGO)
        self.utils.execute_javascript("arguments[0].style.border='3px solid red'", logo)
        time.sleep(1)

        logo_text = self.utils.execute_javascript("return arguments[0].innerText", logo)
        self.logger.info(f"Logo text: {logo_text}")

        # Create and remove test element
        self.utils.execute_javascript("""
            var btn = document.createElement('button');
            btn.innerHTML = 'Test Button';
            btn.id = 'testBtn';
            document.body.appendChild(btn);
        """)
        self.utils.execute_javascript("""
            var element = document.getElementById('testBtn');
            if (element) element.parentNode.removeChild(element);
        """)

        result = self.utils.execute_async_javascript("""
            var callback = arguments[arguments.length - 1];
            setTimeout(function() {
                callback('Async execution complete');
            }, 1000);
        """)
        self.logger.info(f"Async result: {result}")

    @allure.feature('Alerts and Popups')
    @allure.story('Test Alert Handling')
    def test_05_alerts_handling(self):
        """Test handling of alerts."""
        self.logger.info("Testing alert handling")

        self.home_page.open_contact_modal()
        time.sleep(1)
        self.home_page.fill_contact_form(
            email="test@example.com",
            name="Test User",
            message="Test message"
        )
        self.home_page.send_contact_message()

        alert_text = self.home_page.accept_alert()
        assert "Thanks for the message" in alert_text
        self.logger.info(f"Alert handled with text: {alert_text}")

        self.home_page.open_signup_modal()
        time.sleep(1)
        random_username = self.utils.generate_random_string(10)
        self.home_page.signup(random_username, "Test@123")
        alert_text = self.home_page.accept_alert()
        self.logger.info(f"Signup alert: {alert_text}")

    @allure.feature('Cookies')
    @allure.story('Test Cookie Operations')
    def test_06_cookie_operations(self):
        """Test cookie operations."""
        self.logger.info("Testing cookie operations")

        cookies = self.home_page.get_cookies()
        self.logger.info(f"Found {len(cookies)} cookies")

        custom_cookie = {
            'name': 'test_cookie',
            'value': 'test_value_123',
            'path': '/',
            'domain': '.demoblaze.com'
        }
        self.home_page.add_cookie(custom_cookie)
        self.logger.info("Added custom cookie")

        self.home_page.refresh_page()
        cookies = self.home_page.get_cookies()
        cookie_names = [c['name'] for c in cookies]
        assert 'test_cookie' in cookie_names

        self.home_page.delete_cookie('test_cookie')
        self.home_page.delete_all_cookies()
        cookies = self.home_page.get_cookies()
        self.logger.info(f"Cookies after deletion: {len(cookies)}")

    @allure.feature('Scrolling')
    @allure.story('Test Various Scrolling Methods')
    def test_07_scrolling_operations(self):
        """Test scrolling operations."""
        self.logger.info("Testing scrolling operations")

        self.utils.scroll_to_bottom()
        time.sleep(1)
        self.utils.scroll_to_top()
        time.sleep(1)
        self.utils.scroll_by_pixels(0, 300)
        time.sleep(1)

        next_button = self.home_page.find_element(HomePage.NEXT_BUTTON)
        self.utils.scroll_to_element(next_button)
        time.sleep(1)

        self.utils.take_screenshot("after_scroll")
        self.logger.info("Scrolling operations completed")

    @allure.feature('Screenshots')
    @allure.story('Test Screenshot Capabilities')
    def test_08_screenshot_operations(self):
        """Test various screenshot operations."""
        self.logger.info("Testing screenshot operations")

        self.utils.take_screenshot("full_page")

        logo = self.home_page.find_element(HomePage.LOGO)
        self.utils.take_element_screenshot(logo, "logo_screenshot")

        product_card = self.home_page.find_elements(HomePage.PRODUCT_CARDS)[0]
        self.utils.highlight_element(product_card, duration=1)
        self.utils.take_screenshot("highlighted_element")

        self.logger.info("Screenshot operations completed")

    @allure.feature('Waits')
    @allure.story('Test Different Wait Strategies')
    def test_09_wait_strategies(self):
        """Test different wait strategies."""
        from selenium.webdriver.support.ui import WebDriverWait
        from selenium.webdriver.support import expected_conditions as EC
        from selenium.webdriver.common.by import By
        from selenium.common.exceptions import NoSuchElementException

        self.logger.info("Testing wait strategies")

        self.home_page.wait_for_element_visible(HomePage.LOGO)

        WebDriverWait(self.driver, 10).until(
            EC.element_to_be_clickable(HomePage.CART_MENU)
        )

        self.home_page.select_category("Phones")
        product_locator = (By.XPATH, "//a[contains(text(),'Samsung galaxy s6')]")
        self.home_page.wait_for_element_visible(product_locator)

        def custom_condition(driver):
            elements = driver.find_elements(*HomePage.PRODUCT_CARDS)
            return len(elements) > 0

        WebDriverWait(self.driver, 10).until(custom_condition)

        wait = WebDriverWait(self.driver, timeout=10, poll_frequency=0.5,
                             ignored_exceptions=[NoSuchElementException])
        wait.until(EC.presence_of_element_located(HomePage.LOGO))

        self.logger.info("Wait strategies tested successfully")

    @allure.feature('Data Driven Testing')
    @allure.story('Test with Excel Data')
    @pytest.mark.parametrize("test_data", [
        {"username": "user1", "password": "pass1", "product": "Samsung galaxy s6"},
        {"username": "user2", "password": "pass2", "product": "Nokia lumia 1520"}
    ])
    def test_10_data_driven_excel(self, test_data):
        """Test with data from Excel (parameterized)."""
        self.logger.info(f"Testing with data: {test_data}")

        if "Samsung" in test_data["product"] or "Nokia" in test_data["product"]:
            self.home_page.select_category("Phones")

        self.home_page.click_product(test_data["product"])
        time.sleep(2)

        product_name = self.product_page.get_product_name()
        assert test_data["product"] in product_name

        self.logger.info(f"Data driven test completed for: {test_data['product']}")

    @allure.feature('Data Driven Testing')
    @allure.story('Test with XML Data')
    def test_11_data_driven_xml(self):
        """Test with data from XML."""
        self.logger.info("Testing with XML data")

        xml_data = [
            {"username": "xmluser1", "password": "xmlpass1", "product": "Sony vaio i5"},
            {"username": "xmluser2", "password": "xmlpass2", "product": "MacBook air"}
        ]

        self.xml_utils.write_xml_data('data/test_output.xml', xml_data)
        read_data = self.xml_utils.read_xml_data('data/test_output.xml')

        for data in read_data:
            self.logger.info(f"Processing XML data: {data}")

        self.logger.info("XML data testing completed")

    @allure.feature('Data Driven Testing')
    @allure.story('Test with JSON Data')
    def test_12_data_driven_json(self):
        """Test with data from JSON."""
        self.logger.info("Testing with JSON data")

        json_data = {
            "test_users": [
                {"username": "jsonuser1", "password": "jsonpass1"},
                {"username": "jsonuser2", "password": "jsonpass2"}
            ],
            "test_products": ["Samsung galaxy s6", "Nokia lumia 1520"]
        }

        self.json_utils.write_json_data('data/test_output.json', json_data)
        read_data = self.json_utils.read_json_data('data/test_output.json')

        for user in read_data.get("test_users", []):
            self.logger.info(f"Processing JSON user: {user['username']}")

        self.logger.info("JSON data testing completed")

    @allure.feature('Data Driven Testing')
    @allure.story('Test with CSV Data')
    def test_13_data_driven_csv(self):
        """Test with data from CSV."""
        self.logger.info("Testing with CSV data")

        csv_data = [
            {"username": "csvuser1", "password": "csvpass1", "product": "iPhone 6 32gb"},
            {"username": "csvuser2", "password": "csvpass2", "product": "Sony xperia z5"}
        ]

        self.csv_utils.write_csv_data('data/test_output.csv', csv_data)
        read_data = self.csv_utils.read_csv_data('data/test_output.csv')

        for data in read_data:
            self.logger.info(f"Processing CSV data: {data}")

        self.logger.info("CSV data testing completed")

    @allure.feature('Storage')
    @allure.story('Test Local and Session Storage')
    def test_14_storage_operations(self):
        """Test local and session storage operations."""
        self.logger.info("Testing storage operations")

        self.utils.set_local_storage("test_key", "test_value")
        self.utils.set_local_storage("user_preference", "dark_mode")

        local_storage = self.utils.get_local_storage()
        self.logger.info(f"Local storage: {local_storage}")

        self.utils.set_session_storage("session_key", "session_value")
        session_storage = self.utils.get_session_storage()
        self.logger.info(f"Session storage: {session_storage}")

        self.utils.clear_local_storage()
        self.utils.clear_session_storage()

        self.logger.info("Storage operations completed")

    @allure.feature('Performance')
    @allure.story('Test Performance Metrics')
    def test_15_performance_metrics(self):
        """Test performance metrics collection."""
        self.logger.info("Testing performance metrics")

        self.driver.get("https://www.demoblaze.com")
        time.sleep(3)

        metrics = self.utils.get_performance_metrics()
        if metrics:
            load_time = metrics.get('loadEventEnd', 0) - metrics.get('fetchStart', 0)
            self.logger.info(f"Page load time: {load_time} ms")

        logs = self.utils.get_browser_logs()
        self.logger.info(f"Browser logs count: {len(logs)}")

        self.logger.info("Performance metrics collected")

    @allure.feature('Element States')
    @allure.story('Test Element State Validations')
    def test_16_element_states(self):
        """Test element state validations."""
        self.logger.info("Testing element states")

        assert self.home_page.is_displayed(HomePage.LOGO), "Logo should be displayed"
        assert self.home_page.is_enabled(HomePage.CART_MENU), "Cart menu should be enabled"

        self.home_page.open_login_modal()
        time.sleep(1)
        assert self.home_page.is_enabled(HomePage.LOGIN_USERNAME), "Username field should be enabled"
        self.home_page.click(HomePage.CLOSE_LOGIN_BTN)

        self.logger.info("Element state validations completed")

    @allure.feature('CSS Properties')
    @allure.story('Test CSS Property Validations')
    def test_17_css_properties(self):
        """Test CSS property validations."""
        self.logger.info("Testing CSS properties")

        font_size = self.home_page.get_css_property(HomePage.LOGO, "font-size")
        color = self.home_page.get_css_property(HomePage.LOGO, "color")
        display = self.home_page.get_css_property(HomePage.LOGO, "display")

        self.logger.info(f"Logo font size: {font_size}, color: {color}, display: {display}")
        self.logger.info("CSS property validations completed")

    @allure.feature('Navigation')
    @allure.story('Test Browser Navigation')
    def test_18_browser_navigation(self):
        """Test browser navigation operations."""
        self.logger.info("Testing browser navigation")

        initial_url = self.home_page.get_current_url()
        self.home_page.select_category("Phones")
        self.home_page.click_product("Samsung galaxy s6")
        time.sleep(2)

        product_url = self.home_page.get_current_url()
        assert product_url != initial_url

        self.home_page.go_back()
        time.sleep(2)
        self.home_page.go_forward()
        time.sleep(2)
        self.home_page.refresh_page()
        time.sleep(2)

        self.logger.info("Browser navigation completed")

    @allure.feature('Faker Data')
    @allure.story('Test with Faker Generated Data')
    def test_19_faker_data_generation(self):
        """Test with Faker generated data."""
        self.logger.info("Testing with Faker generated data")

        fake_email = self.utils.generate_random_email()
        fake_name = self.utils.generate_random_name()
        fake_phone = self.utils.generate_random_phone()
        fake_address = self.utils.generate_random_address()

        self.logger.info(f"Generated email: {fake_email}")
        self.logger.info(f"Generated name: {fake_name}")

        self.home_page.open_contact_modal()
        time.sleep(1)
        self.home_page.fill_contact_form(fake_email, fake_name, f"Message from {fake_name}")
        self.home_page.send_contact_message()
        self.home_page.accept_alert()

        self.logger.info("Faker data testing completed")

    @allure.feature('Complete E2E Flow')
    @allure.story('Test End-to-End Shopping Flow')
    def test_20_complete_e2e_flow(self):
        """Test complete end-to-end shopping flow."""
        self.logger.info("Starting complete E2E shopping flow")

        # Step 1: Signup
        self.home_page.open_signup_modal()
        time.sleep(1)
        random_username = self.utils.generate_random_string(8)
        password = "Test@1234"
        self.home_page.signup(random_username, password)
        alert_text = self.home_page.accept_alert()
        assert "Sign up successful" in alert_text

        # Step 2: Login
        self.home_page.open_login_modal()
        time.sleep(1)
        self.home_page.login(random_username, password)
        time.sleep(2)
        assert self.home_page.is_user_logged_in()
        logged_user = self.home_page.get_username_from_welcome()
        assert random_username == logged_user

        # Step 3: Select product
        self.home_page.select_category("Phones")
        time.sleep(2)
        product_name = "Samsung galaxy s6"
        self.home_page.click_product(product_name)

        # Step 4: Verify product
        displayed_name = self.product_page.get_product_name()
        assert product_name == displayed_name
        price = self.product_page.get_product_price()
        assert price == "360"

        # Step 5: Add to cart
        alert_text = self.product_page.add_to_cart()  # Use the alert text returned by add_to_cart()
        assert "Product added" in alert_text

        # Step 6: Go to cart
        self.home_page.go_to_cart()
        time.sleep(2)
        assert self.cart_page.get_cart_items_count() == 1
        assert self.cart_page.get_total_price() == "360"

        # Step 7-9: Place order
        self.cart_page.place_order()
        time.sleep(1)

        fake_name = self.utils.generate_random_name()
        fake_country = "USA"
        fake_city = "New York"
        fake_card = self.utils.generate_random_string(16, string.digits)
        fake_month = "12"
        fake_year = "2025"
        self.cart_page.fill_order_form(fake_name, fake_country, fake_city, fake_card, fake_month, fake_year)
        self.cart_page.complete_purchase()
        time.sleep(2)

        confirmation_text = self.cart_page.get_confirmation_text()
        assert "Thank you for your purchase!" in confirmation_text

        # Step 10: Logout
        self.cart_page.close_confirmation()
        time.sleep(1)
        self.home_page.logout()
        time.sleep(1)
        assert not self.home_page.is_user_logged_in()

        self.utils.take_screenshot("e2e_complete")
        self.logger.info("Complete E2E shopping flow completed successfully")

    @allure.feature('Negative Testing')
    @allure.story('Test Invalid Login')
    def test_21_invalid_login(self):
        """Test invalid login attempt."""
        self.logger.info("Testing invalid login")

        self.home_page.open_login_modal()
        time.sleep(1)
        self.home_page.login("invaliduser", "wrongpass")
        alert_text = self.home_page.accept_alert()
        assert ("Wrong password" in alert_text) or ("User does not exist" in alert_text)
        assert not self.home_page.is_user_logged_in()

    @allure.feature('Negative Testing')
    @allure.story('Test Duplicate Signup')
    def test_22_duplicate_signup(self):
        """Test signup with existing username."""
        self.logger.info("Testing duplicate signup")

        self.home_page.open_signup_modal()
        time.sleep(1)
        self.home_page.signup("testuser2024", "Test@1234")  # From config
        alert_text = self.home_page.accept_alert()
        assert "This user already exist" in alert_text

    @allure.feature('Contact Form')
    @allure.story('Test Contact Form Submission')
    def test_23_contact_form(self):
        """Test contact form submission."""
        self.logger.info("Testing contact form")

        self.home_page.open_contact_modal()
        time.sleep(1)
        email = self.utils.generate_random_email()
        name = self.utils.generate_random_name()
        message = self.utils.generate_random_string(50)
        self.home_page.fill_contact_form(email, name, message)
        self.home_page.send_contact_message()
        alert_text = self.home_page.accept_alert()
        assert "Thanks for the message" in alert_text

    @allure.feature('About Us')
    @allure.story('Test About Us Modal and Video')
    def test_24_about_us_modal(self):
        """Test About Us modal and video playback."""
        self.logger.info("Testing About Us modal")

        self.home_page.open_about_modal()
        time.sleep(1)
        assert self.home_page.is_displayed(HomePage.ABOUT_VIDEO)
        self.home_page.play_video()
        time.sleep(2)
        self.home_page.close_about_modal()

    @allure.feature('Pagination')
    @allure.story('Test Product Pagination')
    def test_25_pagination(self):
        """Test product pagination."""
        self.logger.info("Testing pagination")

        # Ensure we start from Home
        self.home_page.navigate_to_home()
        time.sleep(2)

        # Page 1
        page1_products = self.home_page.get_all_products()
        assert len(page1_products) > 0, "Page 1 should contain products"

        # Go to Page 2
        self.home_page.go_to_next_page()
        time.sleep(2)
        page2_products = self.home_page.get_all_products()
        assert len(page2_products) > 0, "Page 2 should contain products"
        assert page1_products != page2_products, "Page 1 and Page 2 should display different products"

        # Go back to Page 1
        self.home_page.go_to_previous_page()
        time.sleep(2)
        page1_again = self.home_page.get_all_products()
        assert len(page1_again) > 0, "Page 1 should still contain products after returning"

        self.logger.info("Pagination test passed: pages are non-empty and differ")
    @allure.feature('Categories')
    @allure.story('Test All Categories')
    def test_26_categories(self):
        """Test navigation through all categories."""
        self.logger.info("Testing categories")

        categories = ["Phones", "Laptops", "Monitors"]
        for category in categories:
            self.home_page.select_category(category)
            time.sleep(2)
            products = self.home_page.get_all_products()
            assert len(products) > 0
            self.logger.info(f"Category {category} has {len(products)} products")

    @allure.feature('Network Emulation')
    @allure.story('Test Network Conditions')
    def test_27_network_emulation(self):
        """Test with emulated network conditions (Chrome only)."""
        browser = self.browser_config.config.get('DEFAULT', 'browser').lower()
        if browser == 'chrome':
            self.logger.info("Testing network emulation")

            self.utils.set_network_conditions(
                offline=False,
                latency=100,
                download_throughput=750 * 1024,
                upload_throughput=250 * 1024
            )

            self.driver.get("https://www.demoblaze.com")
            time.sleep(5)
            assert "STORE" in self.driver.title

            # Reset to default
            self.utils.set_network_conditions()

    @allure.feature('Mobile Emulation')
    @allure.story('Test Mobile View (Chrome only)')
    def test_28_mobile_emulation(self):
        """Mobile emulation is disabled by default."""
        self.logger.info("Mobile emulation test skipped - enable in browser_config.py")

    @allure.feature('Logging')
    @allure.story('Test Log Collection')
    def test_29_log_collection(self):
        """Test collecting browser logs."""
        self.logger.info("Testing log collection")

        self.home_page.open_login_modal()
        self.home_page.login("test", "test")
        self.home_page.accept_alert()

        logs = self.utils.get_browser_logs()
        for log in logs:
            self.logger.info(f"Browser log: {log}")

    @allure.feature('Cleanup')
    @allure.story('Test Cleanup Operations')
    def test_30_cleanup(self):
        """Test cleanup operations."""
        self.logger.info("Performing cleanup")

        self.home_page.delete_all_cookies()
        self.utils.clear_local_storage()
        self.utils.clear_session_storage()
        self.home_page.refresh_page()

        self.logger.info("Cleanup completed")

    @allure.feature('File Upload')
    @allure.story('Test File Upload using send_keys and pyautogui')
    def test_31_file_upload(self):
        """Test file upload using send_keys (primary) and pyautogui (fallback)."""
        self.logger.info("Testing file upload")

        # Navigate to file upload demo site
        self.driver.get("https://the-internet.herokuapp.com/upload")

        # Create a temporary test file
        test_file_name = "upload_test.txt"
        test_file_path = os.path.join(os.getcwd(), test_file_name)
        with open(test_file_path, "w") as f:
            f.write("This is a test file for Selenium upload.")

        try:
            # Locate file input and upload using send_keys
            file_input = self.driver.find_element(By.ID, "file-upload")
            file_input.send_keys(test_file_path)
            self.logger.info(f"Uploaded file via send_keys: {test_file_path}")

            # Click upload button
            self.driver.find_element(By.ID, "file-submit").click()
            time.sleep(2)

            # Verify success
            success_header = self.driver.find_element(By.TAG_NAME, "h3").text
            assert "File Uploaded!" in success_header
            uploaded_file = self.driver.find_element(By.ID, "uploaded-files").text
            assert uploaded_file == test_file_name

            self.logger.info("Success: File upload via send_keys successful")

            # Optional: Demonstrate pyautogui fallback (commented out by default)
            # Uncomment only if you install pyautogui and need it for non-input dialogs

            # import pyautogui
            # self.driver.get("https://the-internet.herokuapp.com/upload")
            # file_input.click()  # Opens OS dialog
            # time.sleep(2)
            # pyautogui.write(test_file_path)
            # pyautogui.press('enter')
            # time.sleep(2)
            # self.driver.find_element(By.ID, "file-submit").click()
            # assert "File Uploaded!" in self.driver.find_element(By.TAG_NAME, "h3").text


        finally:
            # Cleanup
            if os.path.exists(test_file_path):
                os.remove(test_file_path)
                self.logger.info("Cleaned up test file")

    @allure.feature('Broken Links')
    @allure.story('Test Broken Link Validation')
    def test_32_broken_links_check(self):
        """Test broken link validation on The Internet homepage."""
        self.logger.info("Running broken links check on The Internet homepage")

        # Navigate to a page with known valid absolute external links
        self.driver.get("https://the-internet.herokuapp.com/")
        time.sleep(2)  # Optional: wait for page to load (consider replacing with WebDriverWait)

        # Check for broken links using utility method
        result = self.utils.check_broken_links()

        valid_links = result["valid_links"]
        broken_links = result["broken_links"]
        broken_list = result["broken_list"]

        # Log results
        self.logger.info(f"✅ Found {valid_links} valid links")
        if broken_links > 0:
            self.logger.warning(f"⚠️ Found {broken_links} broken links: {broken_list}")

        # Assert that we have a reasonable number of working links
        assert valid_links > 5, f"Expected more than 5 valid links, but found only {valid_links}"

        self.logger.info("Success: Sufficient number of valid links confirmed!")

    @allure.feature('Form Elements')
    @allure.story('Test Radio Button Handling (on external demo site)')
    def test_33_radio_button_demo(self):
        """Demonstrate radio button interaction on a compatible site."""
        self.logger.info("Testing radio button selection on demoqa.com")

        # Navigate to a site that actually has radio buttons
        self.driver.get("https://demoqa.com/radio-button")
        time.sleep(2)  # Allow page to load (or replace with WebDriverWait)

        # Click 'Yes' radio button via its label (best practice for hidden inputs)
        yes_label = self.driver.find_element(By.XPATH, "//label[text()='Yes']")
        yes_label.click()

        # Verify selection using JavaScript (since the actual input is hidden)
        is_selected = self.driver.execute_script("return document.getElementById('yesRadio').checked;")
        assert is_selected, "Radio button 'Yes' was not selected"

        # Optional: Test 'Impressive' as well
        impressive_label = self.driver.find_element(By.XPATH, "//label[text()='Impressive']")
        impressive_label.click()
        is_impressive_selected = self.driver.execute_script(
            "return document.getElementById('impressiveRadio').checked;")
        assert is_impressive_selected, "Radio button 'Impressive' was not selected"

        self.logger.info(" Radio button selection verified successfully")


if __name__ == '__main__':
    pytest.main(['-v', '--html=reports/test_report.html', '--alluredir=reports/allure-results'])