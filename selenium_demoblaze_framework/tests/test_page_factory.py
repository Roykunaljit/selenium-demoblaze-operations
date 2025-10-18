import pytest
import os
import sys
import time

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from selenium_demoblaze_framework.pages.home_page_factory import HomePageFactory
from selenium_demoblaze_framework.utilities.custom_logger import CustomLogger
from selenium_demoblaze_framework.config.browser_config import BrowserConfig


class TestPageFactory:
    @pytest.fixture
    def setup(self):
        self.logger = CustomLogger.get_logger(self.__class__.__name__)
        self.browser_config = BrowserConfig()
        self.driver = self.browser_config.get_driver()
        self.driver.maximize_window()  # Maximize window to ensure all elements are visible
        self.home_page = HomePageFactory(self.driver, self.logger)

        self.driver.get("https://www.demoblaze.com")
        time.sleep(3)  # Wait for page to fully load

        yield

        self.driver.quit()

    def test_page_factory_single_elements(self, setup):
        """Test Page Factory single element initialization"""
        try:
            # Test that elements can be accessed through decorators
            logo = self.home_page.logo()
            assert logo is not None, "Logo element not found"
            assert self.home_page.is_displayed(logo), "Logo not displayed"

            home_menu = self.home_page.home_menu()
            assert home_menu is not None, "Home menu element not found"
            assert self.home_page.is_enabled(home_menu), "Home menu not enabled"

            cart_menu = self.home_page.cart_menu()
            assert cart_menu is not None, "Cart menu element not found"

            login_menu = self.home_page.login_menu()
            assert login_menu is not None, "Login menu element not found"

            self.logger.info("[PASS] Single elements test passed")
        except Exception as e:
            self.logger.error(f"[FAIL] Single elements test failed: {str(e)}")
            raise

    def test_page_factory_multiple_elements(self, setup):
        """Test Page Factory multiple elements initialization"""
        try:
            # Wait for products to load
            time.sleep(2)

            # Test multiple elements
            product_titles = self.home_page.product_titles()
            assert len(product_titles) > 0, "No product titles found"

            product_cards = self.home_page.product_cards()
            assert len(product_cards) > 0, "No product cards found"

            # Get fresh product prices
            product_prices = self.driver.find_elements("css selector", "div.card h5")
            assert len(product_prices) > 0, "No product prices found"

            self.logger.info(f"Found {len(product_titles)} products")
            self.logger.info("[PASS] Multiple elements test passed")
        except Exception as e:
            self.logger.error(f"[FAIL] Multiple elements test failed: {str(e)}")
            raise

    def test_page_factory_navigation(self, setup):
        """Test Page Factory navigation methods"""
        try:
            # Test category selection
            self.home_page.select_category("Phones")
            time.sleep(2)
            products = self.home_page.get_all_products()
            assert len(products) > 0, "No products found in Phones category"

            # Test navigation back to home
            self.home_page.navigate_to_home()
            time.sleep(1)
            assert "STORE" in self.home_page.get_page_title(), "Not on home page"

            self.logger.info("[PASS] Navigation test passed")
        except Exception as e:
            self.logger.error(f"[FAIL] Navigation test failed: {str(e)}")
            raise

    def test_page_factory_login_flow(self, setup):
        """Test complete login flow using Page Factory"""
        try:
            # Open signup modal
            self.home_page.open_signup_modal()

            # Signup with random user
            import random
            import string
            random_username = ''.join(random.choices(string.ascii_lowercase + string.digits, k=8))
            password = "Test@1234"

            self.home_page.signup(random_username, password)

            # Handle signup alert
            time.sleep(2)  # Wait for alert
            try:
                alert = self.driver.switch_to.alert
                alert_text = alert.text
                alert.accept()
                self.logger.info(f"Signup alert: {alert_text}")
            except:
                pass

            time.sleep(3)  # Wait for modal to close

            # Open login modal
            self.home_page.open_login_modal()

            # Login
            self.home_page.login(random_username, password)
            time.sleep(3)

            # Verify login
            assert self.home_page.is_user_logged_in(), "User not logged in"
            welcome_msg = self.home_page.get_welcome_message()
            assert random_username in welcome_msg, f"Username '{random_username}' not in welcome message '{welcome_msg}'"

            # Logout
            self.home_page.logout()
            time.sleep(2)
            assert not self.home_page.is_user_logged_in(), "User still logged in after logout"

            self.logger.info("[PASS] Login flow test passed")
        except Exception as e:
            self.logger.error(f"[FAIL] Login flow test failed: {str(e)}")
            raise

    def test_page_factory_product_details(self, setup):
        """Test getting product details"""
        try:
            # Wait for products to load
            time.sleep(2)

            # Get product details
            products = self.home_page.get_product_details()
            assert len(products) > 0, "No product details found"

            # Verify each product has name and price
            for product in products:
                assert 'name' in product, "Product missing name"
                assert 'price' in product, "Product missing price"
                assert product['name'] != "", "Product name is empty"
                assert product['price'] != "", "Product price is empty"

            self.logger.info(f"[PASS] Product details test passed - Found {len(products)} products")
        except Exception as e:
            self.logger.error(f"[FAIL] Product details test failed: {str(e)}")
            raise

    def test_page_factory_search_functionality(self, setup):
        """Test product search functionality"""
        try:
            # Wait for products to load fully
            time.sleep(3)

            # Search for known products that are usually on the page
            found_product = False
            for product_name in ["Samsung", "Nokia", "Sony", "HTC", "Apple", "MacBook"]:
                if self.home_page.search_product(product_name):
                    self.logger.info(f"Found product: {product_name}")
                    found_product = True
                    break

            assert found_product, "No known products found on page"

            # Search for non-existent product
            assert not self.home_page.search_product("NonExistentProduct123"), "Non-existent product found"

            self.logger.info("[PASS] Search functionality test passed")
        except Exception as e:
            self.logger.error(f"[FAIL] Search functionality test failed: {str(e)}")
            raise

    def test_page_factory_element_caching(self, setup):
        """Test that elements are properly cached"""
        try:
            # Get logo element twice
            logo1 = self.home_page.logo()
            logo2 = self.home_page.logo()

            # Elements should be the same object (cached)
            assert logo1 == logo2, "Element caching not working"

            # Get product list twice
            products1 = self.home_page.product_titles()
            products2 = self.home_page.product_titles()

            # Lists should be the same object (cached)
            assert products1 == products2, "Element list caching not working"

            self.logger.info("[PASS] Element caching test passed")
        except Exception as e:
            self.logger.error(f"[FAIL] Element caching test failed: {str(e)}")
            raise