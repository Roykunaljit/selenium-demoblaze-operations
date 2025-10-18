# pages/cart_page.py

from selenium.webdriver.common.by import By
from selenium_demoblaze_framework.pages.base_page import BasePage
import time


class CartPage(BasePage):
    # ==================== Cart Items & Actions ====================
    CART_ITEMS = (By.XPATH, "//tbody[@id='tbodyid']//tr")
    TOTAL_PRICE = (By.ID, "totalp")
    PLACE_ORDER_BTN = (By.XPATH, "//button[contains(text(),'Place Order')]")
    DELETE_ITEM_BTN = (By.XPATH, "//a[contains(text(),'Delete')]")

    # ==================== Order Form (in Modal) ====================
    ORDER_NAME = (By.ID, "name")
    ORDER_COUNTRY = (By.ID, "country")
    ORDER_CITY = (By.ID, "city")
    ORDER_CARD = (By.ID, "card")
    ORDER_MONTH = (By.ID, "month")
    ORDER_YEAR = (By.ID, "year")
    PURCHASE_BTN = (By.XPATH, "//button[contains(text(),'Purchase')]")
    CLOSE_ORDER_BTN = (By.XPATH, "//div[@id='orderModal']//button[contains(text(),'Close')]")

    # ==================== Purchase Confirmation ====================
    CONFIRMATION_OK_BTN = (By.XPATH, "//button[contains(text(),'OK')]")
    CONFIRMATION_TEXT = (By.XPATH, "//div[contains(@class, 'sweet-alert')]//h2[contains(text(), 'Thank you for your purchase!')]")

    def __init__(self, driver, logger):
        super().__init__(driver, logger)

    def get_cart_items_count(self):
        """Get the number of items currently in the cart."""
        items = self.find_elements(self.CART_ITEMS)
        count = len(items)
        self.logger.info(f"Cart contains {count} item(s)")
        return count

    def get_total_price(self):
        """Get the total price displayed on the cart page."""
        total = self.get_text(self.TOTAL_PRICE)
        self.logger.info(f"Cart total price: ${total}")
        return total

    def delete_item(self, index=0):
        """Delete an item from the cart by index (0-based)."""
        delete_buttons = self.find_elements(self.DELETE_ITEM_BTN)
        if delete_buttons and 0 <= index < len(delete_buttons):
            delete_buttons[index].click()
            time.sleep(2)  # Allow DOM to update
            self.logger.info(f"Deleted cart item at index {index}")
        else:
            self.logger.warning(f"No delete button found at index {index}")

    def place_order(self):
        """Click the 'Place Order' button to open the order modal."""
        self.click(self.PLACE_ORDER_BTN)
        time.sleep(1)
        self.logger.info("Clicked 'Place Order'")

    def fill_order_form(self, name, country, city, card, month, year):
        """Fill the purchase order form in the modal."""
        self.send_keys(self.ORDER_NAME, name)
        self.send_keys(self.ORDER_COUNTRY, country)
        self.send_keys(self.ORDER_CITY, city)
        self.send_keys(self.ORDER_CARD, card)
        self.send_keys(self.ORDER_MONTH, month)
        self.send_keys(self.ORDER_YEAR, year)
        self.logger.info("Filled order form with shipping and payment details")

    def complete_purchase(self):
        """Click 'Purchase' to submit the order."""
        self.click(self.PURCHASE_BTN)
        time.sleep(2)  # Wait for confirmation modal
        self.logger.info("Completed purchase")

    def get_confirmation_text(self):
        """Retrieve the order confirmation message (includes ID, amount, etc.)."""
        confirmation = self.get_text(self.CONFIRMATION_TEXT)
        self.logger.info(f"Order confirmation received: {confirmation[:60]}...")
        return confirmation

    def close_confirmation(self):
        """Close the purchase confirmation modal."""
        self.click(self.CONFIRMATION_OK_BTN)
        self.logger.info("Closed confirmation modal")