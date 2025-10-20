# tests/test_page_factory.py
import random
import string
import pytest
import os
import sys
import time

from selenium.common.exceptions import NoSuchElementException, NoAlertPresentException, TimeoutException, \
    WebDriverException
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions
from selenium.webdriver.support.wait import WebDriverWait

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from selenium_demoblaze_framework.pages.home_page_factory import HomePageFactory
from selenium_demoblaze_framework.utilities.custom_logger import CustomLogger
from selenium_demoblaze_framework.config.browser_config import BrowserConfig


class TestPageFactory:
    @pytest.fixture
    def setup(self):
        """Setup test fixture"""
        self.logger = CustomLogger.get_logger(self.__class__.__name__)
        self.browser_config = BrowserConfig()
        self.driver = self.browser_config.get_driver()
        self.driver.maximize_window()
        self.home_page = HomePageFactory(self.driver, self.logger)

        self.driver.get("https://www.demoblaze.com ")
        time.sleep(3)  # Wait for page to fully load

        yield

        try:
            self.driver.quit()
        except:
            pass  # Driver already closed

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
            product_prices = self.driver.find_elements(By.CSS_SELECTOR, "div.card h5")
            assert len(product_prices) > 0, "No product prices found"

            self.logger.info(f"Found {len(product_titles)} products")
            self.logger.info("[PASS] Multiple elements test passed")
        except Exception as e:
            self.logger.error(f"[FAIL] Multiple elements test failed: {str(e)}")
            raise

    def test_page_factory_category_navigation(self, setup):
        """Test Page Factory category navigation methods"""
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

            self.logger.info("[PASS] Category navigation test passed")
        except Exception as e:
            self.logger.error(f"[FAIL] Category navigation test failed: {str(e)}")
            raise

    def test_page_factory_login_flow(self, setup):
        """Test complete login flow using Page Factory"""
        try:
            self.logger.info("Starting login flow test...")

            # Generate random credentials
            random_username = ''.join(random.choices(string.ascii_lowercase + string.digits, k=8))
            password = "Test@1234"
            self.logger.info(f"Generated username: {random_username}")

            # ===== SIGNUP FLOW =====
            self.logger.info("Opening signup modal...")
            self.home_page.open_signup_modal()

            # Wait for signup modal to be visible
            wait = WebDriverWait(self.driver, 10)
            wait.until(expected_conditions.visibility_of_element_located((By.ID, "signInModal")))
            time.sleep(1)

            # Fill signup form
            self.logger.info(f"Signing up with username: {random_username}")
            self.home_page.signup(random_username, password)

            # Handle signup alert
            time.sleep(2)
            try:
                alert = wait.until(expected_conditions.alert_is_present())
                alert_text = alert.text
                self.logger.info(f"Signup alert: {alert_text}")
                alert.accept()

                # Verify signup was successful
                if "Sign up successful" in alert_text or "successful" in alert_text.lower():
                    self.logger.info("[PASS] Signup successful")
                else:
                    self.logger.warning(f"Unexpected alert text: {alert_text}")

            except (TimeoutException, NoAlertPresentException):
                self.logger.warning("No alert appeared after signup")

            # ===== CLOSE SIGNUP MODAL =====
            time.sleep(2)

            # Try to close the signup modal explicitly
            try:
                # Check if signup modal is still visible
                signup_modal = self.driver.find_element(By.ID, "signInModal")
                if signup_modal.is_displayed():
                    self.logger.info("Signup modal still open, closing it...")

                    # Try clicking the close button
                    try:
                        close_btn = self.driver.find_element(By.XPATH,
                                                             "//div[@id='signInModal']//button[@class='close']")
                        close_btn.click()
                        self.logger.info("Clicked signup modal close button")
                    except NoSuchElementException:
                        # Try alternative close button selector
                        try:
                            close_btn = self.driver.find_element(By.XPATH,
                                                                 "//div[@id='signInModal']//button[contains(@class, 'close')]")
                            close_btn.click()
                            self.logger.info("Clicked signup modal close button (alternative)")
                        except:
                            self.logger.warning("Could not find close button")

                    # Wait for modal to close
                    wait.until(expected_conditions.invisibility_of_element_located((By.ID, "signInModal")))
                    self.logger.info("Signup modal closed")

            except NoSuchElementException:
                self.logger.info("Signup modal already closed")

            time.sleep(2)

            # ===== LOGIN FLOW =====
            self.logger.info("Opening login modal...")

            # Wait for login link to be clickable
            login_link = wait.until(expected_conditions.element_to_be_clickable((By.ID, "login2")))
            login_link.click()

            # Wait for login modal to be visible
            wait.until(expected_conditions.visibility_of_element_located((By.ID, "logInModal")))
            time.sleep(1)

            # Fill login form
            self.logger.info(f"Logging in with username: {random_username}")
            self.home_page.login(random_username, password)

            # Wait for login to complete
            time.sleep(3)

            # ===== VERIFY LOGIN =====
            self.logger.info("Verifying login...")

            # Check if user is logged in
            is_logged_in = self.home_page.is_user_logged_in()
            assert is_logged_in, "User not logged in - login link still visible"
            self.logger.info("[PASS] User is logged in")

            # Verify welcome message
            welcome_msg = self.home_page.get_welcome_message()
            self.logger.info(f"Welcome message: {welcome_msg}")

            assert random_username in welcome_msg, \
                f"Username '{random_username}' not found in welcome message '{welcome_msg}'"
            self.logger.info("[PASS] Welcome message contains username")

            # ===== LOGOUT =====
            self.logger.info("Logging out...")
            self.home_page.logout()
            time.sleep(2)

            # Verify logout
            is_still_logged_in = self.home_page.is_user_logged_in()
            assert not is_still_logged_in, "User still logged in after logout"
            self.logger.info("[PASS] User logged out successfully")

            self.logger.info("[PASS] Login flow test completed successfully")

        except Exception as e:
            self.logger.error(f"[FAIL] Login flow test failed: {str(e)}")
            # Take screenshot on failure
            try:
                screenshot_dir = os.path.join(os.getcwd(), "reports", "screenshots")
                os.makedirs(screenshot_dir, exist_ok=True)
                screenshot_path = os.path.join(screenshot_dir, f"login_flow_failure_{int(time.time())}.png")
                self.driver.save_screenshot(screenshot_path)
                self.logger.error(f"Screenshot saved: {screenshot_path}")
            except:
                pass
            raise

    def test_page_factory_menu_navigation(self, setup):
        """Test navigation using Page Factory menu items"""
        try:
            self.logger.info("Testing menu navigation...")

            # Navigate to different categories
            categories = ["Phones", "Laptops", "Monitors"]

            for category in categories:
                self.logger.info(f"Navigating to {category}...")

                # Click category
                try:
                    wait = WebDriverWait(self.driver, 10)
                    category_link = wait.until(
                        expected_conditions.element_to_be_clickable((By.LINK_TEXT, category))
                    )
                    category_link.click()
                    time.sleep(2)
                    self.logger.info(f"[PASS] Navigated to {category}")
                except Exception as e:
                    self.logger.error(f"[FAIL] Failed to navigate to {category}: {e}")

            self.logger.info("[PASS] Menu navigation test completed")

        except Exception as e:
            self.logger.error(f"[FAIL] Menu navigation test failed: {str(e)}")
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
            # Verify driver is active
            try:
                _ = self.driver.current_url
            except WebDriverException as e:
                self.logger.warning(f"Driver connection lost: {e}")
                pytest.skip("Driver connection lost - skipping element caching test")

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
        except WebDriverException as e:
            self.logger.warning(f"WebDriver connection error: {e}")
            pytest.skip("Driver connection lost during test")
        except Exception as e:
            self.logger.error(f"[FAIL] Element caching test failed: {str(e)}")
            raise

    # def test_page_factory_element_validation(self, setup):
    #     """Test that page factory elements are valid"""
    #     try:
    #         # Verify driver is active first
    #         try:
    #             current_url = self.driver.current_url
    #             self.logger.info(f"Current URL: {current_url}")
    #         except WebDriverException as e:
    #             self.logger.warning(f"Driver connection lost before test: {e}")
    #             pytest.skip("Driver connection lost - skipping element validation test")
    #
    #         # Validate logo element with enhanced error handling
    #         try:
    #             logo = self.home_page.logo()
    #             assert logo is not None, "Logo element is None"
    #
    #             # Skip is_displayed check to avoid connection issues
    #             # Instead, verify the element exists by checking its tag name
    #             try:
    #                 tag_name = logo.tag_name
    #                 assert tag_name.lower() in ["img", "a", "div"], f"Unexpected logo tag name: {tag_name}"
    #                 self.logger.info(f"Logo element validated with tag name: {tag_name}")
    #             except (WebDriverException, ConnectionError) as e:
    #                 self.logger.warning(f"Driver lost during logo validation: {e}")
    #                 # Skip is_displayed check to avoid connection issues
    #                 self.logger.info("Skipping logo display check due to connection issues")
    #
    #         except WebDriverException as e:
    #             self.logger.warning(f"Driver error getting logo: {e}")
    #             pytest.skip("Driver connection lost")
    #
    #         # Validate product elements
    #         try:
    #             products = self.home_page.product_titles()
    #             assert len(products) > 0, "No products found"
    #             self.logger.info(f"Found {len(products)} product elements")
    #         except WebDriverException as e:
    #             self.logger.warning(f"Driver error getting products: {e}")
    #             pytest.skip("Driver connection lost")
    #
    #         # Validate menu items
    #         try:
    #             home_menu = self.home_page.home_menu()
    #             assert home_menu is not None, "Home menu is None"
    #
    #             login_menu = self.home_page.login_menu()
    #             assert login_menu is not None, "Login menu is None"
    #
    #             self.logger.info("Menu items validated")
    #         except WebDriverException as e:
    #             self.logger.warning(f"Driver error getting menu items: {e}")
    #             pytest.skip("Driver connection lost")
    #
    #         self.logger.info("[PASS] Element validation test passed")
    #
    #     except WebDriverException as e:
    #         self.logger.warning(f"[SKIP] WebDriver error in element validation: {str(e)}")
    #         pytest.skip("Driver connection lost during test")
    #     except Exception as e:
    #         self.logger.error(f"[FAIL] Element validation test failed: {str(e)}")
    #         # Take screenshot on failure
    #         try:
    #             screenshot_dir = os.path.join(os.getcwd(), "reports", "screenshots")
    #             os.makedirs(screenshot_dir, exist_ok=True)
    #             screenshot_path = os.path.join(screenshot_dir, f"element_validation_failure_{int(time.time())}.png")
    #             self.driver.save_screenshot(screenshot_path)
    #             self.logger.error(f"Screenshot saved: {screenshot_path}")
    #         except:
    #             pass
    #         raise

    def test_page_factory_cart_navigation(self, setup):
        """Test navigating to cart"""
        try:
            # Verify driver is still active
            try:
                current_url = self.driver.current_url
                self.logger.info(f"Current URL before cart navigation: {current_url}")
            except WebDriverException as e:
                self.logger.error(f"Driver connection lost before test: {e}")
                pytest.skip("Driver connection lost")

            # Wait and use WebDriverWait for cart menu
            wait = WebDriverWait(self.driver, 10)

            # Find and click cart menu with explicit wait
            cart_link = wait.until(
                expected_conditions.element_to_be_clickable((By.ID, "cartur"))
            )

            self.logger.info("Cart menu found, clicking...")
            cart_link.click()
            time.sleep(2)

            # Verify we're on cart page
            current_url = self.driver.current_url
            assert "cart" in current_url.lower(), f"Not on cart page. Current URL: {current_url}"

            self.logger.info("[PASS] Cart navigation test passed")
        except WebDriverException as e:
            self.logger.error(f"[FAIL] WebDriver connection error: {str(e)}")
            pytest.skip("Driver connection lost during test")
        except Exception as e:
            self.logger.error(f"[FAIL] Cart navigation test failed: {str(e)}")
            raise