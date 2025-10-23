from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium_demoblaze_framework.pages.base_page_factory import BasePageFactory
from selenium_demoblaze_framework.utilities.page_factory import find_by
import time


class HomePageFactory(BasePageFactory):
    """Home page using Page Factory pattern"""

    def __init__(self, driver, logger=None):
        super().__init__(driver, logger)
        self.wait = WebDriverWait(driver, 15)

    # Single element locators
    @find_by(By.ID, "nava")
    def logo(self):
        pass

    @find_by(By.XPATH, "//a[contains(text(),'Home')]")
    def home_menu(self):
        pass

    @find_by(By.ID, "cartur")
    def cart_menu(self):
        pass

    @find_by(By.ID, "login2")
    def login_menu(self):
        pass

    @find_by(By.ID, "signin2")
    def signup_menu(self):
        pass

    @find_by(By.ID, "logout2")
    def logout_menu(self):
        pass

    @find_by(By.ID, "nameofuser")
    def welcome_text(self):
        pass

    # Multiple elements locators - Fixed selectors
    @find_by(By.CSS_SELECTOR, "h4.card-title a", multiple=True)
    def product_titles(self):
        pass

    @find_by(By.CLASS_NAME, "card", multiple=True)
    def product_cards(self):
        pass

    @find_by(By.CSS_SELECTOR, "div.card h5", multiple=True)
    def product_prices(self):
        pass

    # Category elements
    @find_by(By.LINK_TEXT, "Phones")
    def phones_category(self):
        pass

    @find_by(By.LINK_TEXT, "Laptops")
    def laptops_category(self):
        pass

    @find_by(By.LINK_TEXT, "Monitors")
    def monitors_category(self):
        pass

    # Modal elements for signup
    @find_by(By.ID, "sign-username")
    def signup_username(self):
        pass

    @find_by(By.ID, "sign-password")
    def signup_password(self):
        pass

    @find_by(By.XPATH, "//button[text()='Sign up']")
    def signup_button(self):
        pass

    # Modal elements for login
    @find_by(By.ID, "loginusername")
    def login_username(self):
        pass

    @find_by(By.ID, "loginpassword")
    def login_password(self):
        pass

    @find_by(By.XPATH, "//button[text()='Log in']")
    def login_button(self):
        pass

    # Business methods
    def navigate_to_home(self):
        """Navigate to home page"""
        home_btn = self.wait.until(EC.element_to_be_clickable((By.XPATH, "//a[contains(text(),'Home')]")))
        home_btn.click()
        time.sleep(1)

    def select_category(self, category_name):
        """Select product category"""
        if category_name.lower() == "phones":
            phones = self.wait.until(EC.element_to_be_clickable((By.LINK_TEXT, "Phones")))
            phones.click()
        elif category_name.lower() == "laptops":
            laptops = self.wait.until(EC.element_to_be_clickable((By.LINK_TEXT, "Laptops")))
            laptops.click()
        elif category_name.lower() == "monitors":
            monitors = self.wait.until(EC.element_to_be_clickable((By.LINK_TEXT, "Monitors")))
            monitors.click()
        time.sleep(2)

    def get_all_products(self):
        """Get all product titles"""
        time.sleep(2)  # Wait for products to load
        # Get fresh elements
        products = self.driver.find_elements(By.CSS_SELECTOR, "h4.card-title a")
        return [p.text for p in products if p.text]

    def get_product_details(self):
        """Get product names and prices"""
        time.sleep(2)  # Wait for products to load

        # Get fresh elements
        titles = self.driver.find_elements(By.CSS_SELECTOR, "h4.card-title a")
        prices = self.driver.find_elements(By.CSS_SELECTOR, "div.card h5")

        products = []
        for i in range(min(len(titles), len(prices))):
            products.append({
                'name': titles[i].text,
                'price': prices[i].text
            })
        return products

    def open_login_modal(self):
        """Open login modal"""
        login_btn = self.wait.until(EC.element_to_be_clickable((By.ID, "login2")))
        login_btn.click()
        # Wait for modal to be visible
        self.wait.until(EC.visibility_of_element_located((By.ID, "logInModal")))
        self.wait.until(EC.element_to_be_clickable((By.ID, "loginusername")))
        time.sleep(1)  # Additional wait for animation

    def open_signup_modal(self):
        """Open signup modal"""
        signup_btn = self.wait.until(EC.element_to_be_clickable((By.ID, "signin2")))
        signup_btn.click()
        # Wait for modal to be visible
        self.wait.until(EC.visibility_of_element_located((By.ID, "signInModal")))
        self.wait.until(EC.element_to_be_clickable((By.ID, "sign-username")))
        time.sleep(1)  # Additional wait for animation

    def login(self, username, password):
        """Perform login with better wait conditions"""
        try:
            # Wait for modal and fields to be ready
            self.wait.until(EC.visibility_of_element_located((By.ID, "logInModal")))

            # Get elements with wait
            username_field = self.wait.until(EC.element_to_be_clickable((By.ID, "loginusername")))
            password_field = self.wait.until(EC.element_to_be_clickable((By.ID, "loginpassword")))
            login_btn = self.wait.until(EC.element_to_be_clickable((By.XPATH, "//button[text()='Log in']")))

            # Clear and enter data
            username_field.clear()
            username_field.send_keys(username)
            password_field.clear()
            password_field.send_keys(password)

            # Click login
            login_btn.click()
            time.sleep(2)

        except Exception as e:
            if self.logger:
                self.logger.error(f"Login failed: {str(e)}")
            # Try JavaScript as fallback
            self.driver.execute_script("""
                document.getElementById('loginusername').value = arguments[0];
                document.getElementById('loginpassword').value = arguments[1];
                document.querySelector('#logInModal button.btn-primary').click();
            """, username, password)
            time.sleep(2)

    def signup(self, username, password):
        """Perform signup with better wait conditions"""
        try:
            # Wait for modal and fields to be ready
            self.wait.until(EC.visibility_of_element_located((By.ID, "signInModal")))

            # Get elements with wait
            username_field = self.wait.until(EC.element_to_be_clickable((By.ID, "sign-username")))
            password_field = self.wait.until(EC.element_to_be_clickable((By.ID, "sign-password")))
            signup_btn = self.wait.until(EC.element_to_be_clickable((By.XPATH, "//button[text()='Sign up']")))

            # Clear and enter data
            username_field.clear()
            username_field.send_keys(username)
            password_field.clear()
            password_field.send_keys(password)

            # Click signup
            signup_btn.click()
            time.sleep(1)

        except Exception as e:
            if self.logger:
                self.logger.error(f"Signup failed: {str(e)}")
            # Try JavaScript as fallback
            self.driver.execute_script("""
                document.getElementById('sign-username').value = arguments[0];
                document.getElementById('sign-password').value = arguments[1];
                document.querySelector('#signInModal button.btn-primary').click();
            """, username, password)
            time.sleep(1)

    def logout(self):
        """Perform logout"""
        try:
            logout_btn = self.wait.until(EC.element_to_be_clickable((By.ID, "logout2")))
            logout_btn.click()
            time.sleep(1)
            return True
        except:
            return False

    def is_user_logged_in(self):
        """Check if user is logged in"""
        try:
            welcome = self.wait.until(EC.presence_of_element_located((By.ID, "nameofuser")))
            return welcome.is_displayed() and "Welcome" in welcome.text
        except:
            return False

    def get_welcome_message(self):
        """Get welcome message text"""
        try:
            welcome = self.wait.until(EC.presence_of_element_located((By.ID, "nameofuser")))
            return welcome.text
        except:
            return ""

    def search_product(self, product_name):
        """Search for a product"""
        time.sleep(3)  # Wait for page to fully load

        # Refresh product list
        products = self.driver.find_elements(By.CSS_SELECTOR, "h4.card-title a")

        for product in products:
            product_text = product.text
            if product_text and product_name.lower() in product_text.lower():
                if self.logger:
                    self.logger.info(f"Found product: {product_text}")
                return True

        # Log all products found for debugging
        if self.logger:
            all_products = [p.text for p in products if p.text]
            self.logger.info(f"Products on page: {all_products}")

        return False

    def click_logo(self):
        logo_element = self.logo()  # ← This uses @find_by and caching
        self.click_element(logo_element)