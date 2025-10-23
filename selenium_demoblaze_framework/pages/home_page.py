# pages/home_page.py
from selenium.common import TimeoutException, NoSuchElementException, WebDriverException
from selenium.webdriver.common.by import By
from selenium_demoblaze_framework.pages.base_page import BasePage
import time


class HomePage(BasePage):
    # ==================== Header & Navigation ====================
    LOGO = (By.ID, "nava")
    HOME_MENU = (By.XPATH, "//a[contains(text(),'Home')]")
    CONTACT_MENU = (By.XPATH, "//a[contains(text(),'Contact')]")
    ABOUT_US_MENU = (By.XPATH, "//a[contains(text(),'About us')]")
    CART_MENU = (By.ID, "cartur")
    LOGIN_MENU = (By.ID, "login2")
    SIGNUP_MENU = (By.ID, "signin2")
    LOGOUT_MENU = (By.ID, "logout2")
    WELCOME_USER = (By.ID, "nameofuser")
    LOGOUT_BUTTON = (By.ID, "logout2")

    # ==================== Categories ====================
    PHONES_CATEGORY = (By.XPATH, "//a[contains(text(),'Phones')]")
    LAPTOPS_CATEGORY = (By.XPATH, "//a[contains(text(),'Laptops')]")
    MONITORS_CATEGORY = (By.XPATH, "//a[contains(text(),'Monitors')]")
    CATEGORIES_LINK = (By.ID, "cat")

    # ==================== Carousel ====================
    CAROUSEL_NEXT = (By.XPATH, "//span[@class='carousel-control-next-icon']")
    CAROUSEL_PREV = (By.XPATH, "//span[@class='carousel-control-prev-icon']")
    CAROUSEL_INDICATORS = (By.XPATH, "//ol[@class='carousel-indicators']//li")

    # ==================== Products ====================
    PRODUCT_CARDS = (By.CLASS_NAME, "card")
    PRODUCT_TITLES = (By.CLASS_NAME, "card-title")
    PRODUCT_PRICES = (By.XPATH, "//div[@class='card-block']//h5")
    PRODUCT_DESCRIPTIONS = (By.ID, "article")

    # ==================== Pagination ====================
    NEXT_BUTTON = (By.ID, "next2")
    PREVIOUS_BUTTON = (By.ID, "prev2")

    # ==================== Contact Modal ====================
    CONTACT_EMAIL = (By.ID, "recipient-email")
    CONTACT_NAME = (By.ID, "recipient-name")
    CONTACT_MESSAGE = (By.ID, "message-text")
    SEND_MESSAGE_BTN = (By.XPATH, "//button[contains(text(),'Send message')]")
    CLOSE_CONTACT_BTN = (By.XPATH, "//div[@id='exampleModal']//button[contains(text(),'Close')]")

    # ==================== About Us Modal ====================
    ABOUT_VIDEO = (By.ID, "example-video")
    PLAY_VIDEO_BTN = (By.CLASS_NAME, "vjs-play-control")
    CLOSE_ABOUT_BTN = (By.XPATH, "//div[@id='videoModal']//button[contains(text(),'Close')]")

    # ==================== Login Modal ====================
    LOGIN_USERNAME = (By.ID, "loginusername")
    LOGIN_PASSWORD = (By.ID, "loginpassword")
    LOGIN_BUTTON = (By.XPATH, "//button[contains(text(),'Log in')]")
    CLOSE_LOGIN_BTN = (By.XPATH, "//div[@id='logInModal']//button[contains(text(),'Close')]")

    # ==================== Signup Modal ====================
    SIGNUP_USERNAME = (By.ID, "sign-username")
    SIGNUP_PASSWORD = (By.ID, "sign-password")
    SIGNUP_BUTTON = (By.XPATH, "//button[contains(text(),'Sign up')]")
    CLOSE_SIGNUP_BTN = (By.XPATH, "//div[@id='signInModal']//button[contains(text(),'Close')]")

    def __init__(self, driver, logger):
        super().__init__(driver, logger)
        self.logger = logger

    def navigate_to_home(self):
        """Navigate to home page."""
        self.click(self.HOME_MENU)
        self.logger.info("Navigated to Home page")

    def select_category(self, category_name):
        """Select product category: 'Phones', 'Laptops', or 'Monitors'."""
        category_name = category_name.lower()
        if category_name == "phones":
            self.click(self.PHONES_CATEGORY)
        elif category_name == "laptops":
            self.click(self.LAPTOPS_CATEGORY)
        elif category_name == "monitors":
            self.click(self.MONITORS_CATEGORY)
        else:
            raise ValueError(f"Unsupported category: {category_name}")
        time.sleep(2)  # Wait for products to load (AJAX)
        self.logger.info(f"Selected category: {category_name}")

    def get_all_products(self):
        """Get all products visible on the current page."""
        products = []
        product_cards = self.find_elements(self.PRODUCT_CARDS)

        for card in product_cards:
            try:
                title_element = card.find_element(By.CLASS_NAME, "card-title")
                price_element = card.find_element(By.TAG_NAME, "h5")
                title = title_element.text.strip()
                price = price_element.text.strip().replace('$', '')
                products.append({"title": title, "price": price})
            except Exception as e:
                self.logger.warning(f"Could not parse product card: {e}")
                continue

        self.logger.info(f"Found {len(products)} products")
        return products

    def click_product(self, product_name):
        """Click on a specific product by its visible name."""
        # Use a more robust XPath that matches partial text
        product_xpath = (By.XPATH, f"//a[contains(text(), '{product_name}')]")
        self.click(product_xpath)
        time.sleep(2)  # Wait for product detail page to load
        self.logger.info(f"Clicked on product: {product_name}")

    def navigate_carousel(self, direction="next"):
        """Navigate the homepage carousel: 'next' or 'prev'."""
        if direction == "next":
            self.click(self.CAROUSEL_NEXT)
        elif direction == "prev":
            self.click(self.CAROUSEL_PREV)
        else:
            raise ValueError("Direction must be 'next' or 'prev'")
        self.logger.info(f"Navigated carousel: {direction}")

    def go_to_next_page(self):
        """Go to the next page of products (pagination)."""
        self.click(self.NEXT_BUTTON)
        time.sleep(2)
        self.logger.info("Navigated to next page")

    def go_to_previous_page(self):
        """Go to the previous page of products (pagination)."""
        self.click(self.PREVIOUS_BUTTON)
        time.sleep(2)
        self.logger.info("Navigated to previous page")

    def open_contact_modal(self):
        """Open the Contact modal."""
        self.click(self.CONTACT_MENU)
        time.sleep(1)
        self.logger.info("Opened contact modal")

    def fill_contact_form(self, email, name, message):
        """Fill out the contact form in the modal."""
        self.send_keys(self.CONTACT_EMAIL, email)
        self.send_keys(self.CONTACT_NAME, name)
        self.send_keys(self.CONTACT_MESSAGE, message)
        self.logger.info(f"Filled contact form with email: {email}, name: {name}")

    def send_contact_message(self):
        """Click 'Send message' in the contact modal."""
        self.click(self.SEND_MESSAGE_BTN)
        self.logger.info("Sent contact message")

    def open_about_modal(self):
        """Open the 'About Us' modal."""
        self.click(self.ABOUT_US_MENU)
        time.sleep(1)
        self.logger.info("Opened About Us modal")

    def play_video(self):
        """Play the video inside the About Us modal."""
        self.click(self.PLAY_VIDEO_BTN)
        self.logger.info("Playing video")

    def close_about_modal(self):
        """Close the About Us modal."""
        self.click(self.CLOSE_ABOUT_BTN)
        self.logger.info("Closed About Us modal")

    def open_login_modal(self):
        """Open the Login modal."""
        self.click(self.LOGIN_MENU)
        time.sleep(1)
        self.logger.info("Opened login modal")

    def login(self, username, password):
        """Perform login via the modal."""
        self.send_keys(self.LOGIN_USERNAME, username)
        self.send_keys(self.LOGIN_PASSWORD, password)
        self.click(self.LOGIN_BUTTON)
        self.logger.info(f"Logged in with username: {username}")

    def open_signup_modal(self):
        """Open the Sign Up modal."""
        self.click(self.SIGNUP_MENU)
        time.sleep(1)
        self.logger.info("Opened signup modal")

    def signup(self, username, password):
        """Perform sign up via the modal."""
        self.send_keys(self.SIGNUP_USERNAME, username)
        self.send_keys(self.SIGNUP_PASSWORD, password)
        self.click(self.SIGNUP_BUTTON)
        self.logger.info(f"Signed up with username: {username}")

    def logout(self):
        """Log out the current user."""
        self.click(self.LOGOUT_MENU)
        self.logger.info("Logged out")

    def is_user_logged_in(self):
        """Check if a user is currently logged in."""
        try:
            # Condition 1: Logout button must be present and displayed
            logout_btn = self.driver.find_element(*self.LOGOUT_BUTTON)  # e.g., (By.ID, "logout2")
            if not logout_btn.is_displayed():
                return False

            # Condition 2: Welcome text must contain "Welcome"
            welcome_text = self.get_text(self.WELCOME_USER)  # (By.ID, "nameofuser")
            return "Welcome" in welcome_text and len(welcome_text.strip()) > 8  # e.g., "Welcome abc"

        except (TimeoutException, NoSuchElementException, WebDriverException):
            return False

    def get_username_from_welcome(self):
        """Extract and return the username from the welcome message."""
        welcome_text = self.get_text(self.WELCOME_USER)
        if welcome_text.startswith("Welcome "):
            return welcome_text.replace("Welcome ", "")
        return welcome_text

    def go_to_cart(self):
        """Navigate to the shopping cart page."""
        self.click(self.CART_MENU)
        time.sleep(2)
        self.logger.info("Navigated to cart")