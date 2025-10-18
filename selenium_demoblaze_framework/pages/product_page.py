# pages/product_page.py

from selenium.webdriver.common.by import By
from selenium_demoblaze_framework.pages.base_page import BasePage
import time


class ProductPage(BasePage):
    # ==================== Product Details Locators ====================
    PRODUCT_NAME = (By.XPATH, "//h2[@class='name']")
    PRODUCT_PRICE = (By.XPATH, "//h3[@class='price-container']")
    PRODUCT_DESCRIPTION = (By.ID, "more-information")
    PRODUCT_IMAGE = (By.XPATH, "//div[@class='item active']//img")
    ADD_TO_CART_BTN = (By.XPATH, "//a[contains(text(),'Add to cart')]")

    def __init__(self, driver, logger):
        super().__init__(driver, logger)

    def get_product_name(self):
        """Get the displayed product name."""
        name = self.get_text(self.PRODUCT_NAME)
        self.logger.info(f"Retrieved product name: {name}")
        return name

    def get_product_price(self):
        """Get and clean the product price (remove '$' and tax note)."""
        price_text = self.get_text(self.PRODUCT_PRICE)
        # Clean price string: remove currency symbol and extra text
        cleaned_price = price_text.replace("$", "").replace(" *includes tax", "").strip()
        self.logger.info(f"Retrieved and cleaned product price: {cleaned_price}")
        return cleaned_price

    def get_product_description(self):
        """Get the product description text."""
        description = self.get_text(self.PRODUCT_DESCRIPTION)
        self.logger.info(f"Retrieved product description (preview): {description[:50]}...")
        return description

    def add_to_cart(self):
        """Click 'Add to cart' button and handle alert."""
        self.click(self.ADD_TO_CART_BTN)
        # Wait for success alert and accept it
        alert_text = self.accept_alert(timeout=5)
        if alert_text:
            self.logger.info(f"Product added to cart. Alert: {alert_text}")
        else:
            self.logger.warning("No alert appeared after adding to cart.")
        time.sleep(2)  # Allow UI to update
        self.logger.info("Completed 'Add to cart' action")
        return alert_text

    def is_product_image_displayed(self):
        """Check if the main product image is displayed."""
        is_displayed = self.is_displayed(self.PRODUCT_IMAGE)
        self.logger.info(f"Product image displayed: {is_displayed}")
        return is_displayed