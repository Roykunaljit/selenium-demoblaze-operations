from selenium.webdriver.common.by import By
from selenium_demoblaze_framework.pages.base_page import BasePage
import time


class LoginPage(BasePage):
    # Login Modal
    LOGIN_USERNAME = (By.ID, "loginusername")
    LOGIN_PASSWORD = (By.ID, "loginpassword")
    LOGIN_BUTTON = (By.XPATH, "//button[contains(text(),'Log in')]")
    CLOSE_LOGIN_BTN = (By.XPATH, "//div[@id='logInModal']//button[contains(text(),'Close')]")

    # Signup Modal
    SIGNUP_USERNAME = (By.ID, "sign-username")
    SIGNUP_PASSWORD = (By.ID, "sign-password")
    SIGNUP_BUTTON = (By.XPATH, "//button[contains(text(),'Sign up')]")
    CLOSE_SIGNUP_BTN = (By.XPATH, "//div[@id='signInModal']//button[contains(text(),'Close')]")

    def __init__(self, driver, logger):
        super().__init__(driver, logger)

    def login(self, username, password):
        """Perform login"""
        self.send_keys(self.LOGIN_USERNAME, username)
        self.send_keys(self.LOGIN_PASSWORD, password)
        self.click(self.LOGIN_BUTTON)
        self.logger.info(f"Logged in with username: {username}")

    def signup(self, username, password):
        """Perform signup"""
        self.send_keys(self.SIGNUP_USERNAME, username)
        self.send_keys(self.SIGNUP_PASSWORD, password)
        self.click(self.SIGNUP_BUTTON)
        self.logger.info(f"Signed up with username: {username}")