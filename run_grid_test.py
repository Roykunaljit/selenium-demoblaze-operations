import threading
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options as ChromeOptions
from selenium.webdriver.edge.options import Options as EdgeOptions
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException

# --- Configuration ---
GRID_HUB_URL = 'http://localhost:4444'


def signup_user(driver, browser_name, username, password):
    """Sign up a new user on DemoBlaze"""
    try:
        wait = WebDriverWait(driver, 15)

        # Click Sign up menu
        signup_menu = wait.until(EC.element_to_be_clickable((By.ID, "signin2")))
        signup_menu.click()
        print(f"[{browser_name}] Sign up modal opened.")

        # Fill signup form
        signup_username = wait.until(EC.element_to_be_clickable((By.ID, "sign-username")))
        signup_username.send_keys(username)

        signup_password = wait.until(EC.element_to_be_clickable((By.ID, "sign-password")))
        signup_password.send_keys(password)

        # Click Sign up button
        signup_button = wait.until(EC.element_to_be_clickable((By.XPATH, "//button[text()='Sign up']")))
        signup_button.click()

        # Wait for alert
        try:
            WebDriverWait(driver, 5).until(EC.alert_is_present())
            alert = driver.switch_to.alert
            alert_text = alert.text
            print(f"[{browser_name}] Signup alert: {alert_text}")
            alert.accept()

            if "Sign up successful" in alert_text:
                print(f"✅ [{browser_name}] User created successfully!")
                time.sleep(1)  # Give it a moment
                return True
            else:
                print(f"⚠️ [{browser_name}] Signup issue: {alert_text}")
                return False
        except TimeoutException:
            print(f"❌ [{browser_name}] No signup confirmation alert")
            return False

    except Exception as e:
        print(f"💥 [{browser_name}] Signup error: {e}")
        return False


def login_user(driver, browser_name, username, password):
    """Login with existing credentials"""
    try:
        wait = WebDriverWait(driver, 15)

        # Click Login menu
        login_menu = wait.until(EC.element_to_be_clickable((By.ID, "login2")))
        login_menu.click()
        print(f"[{browser_name}] Login modal opened.")

        # Fill login form
        username_field = wait.until(EC.element_to_be_clickable((By.ID, "loginusername")))
        username_field.send_keys(username)

        password_field = wait.until(EC.element_to_be_clickable((By.ID, "loginpassword")))
        password_field.send_keys(password)
        print(f"[{browser_name}] Entered credentials.")

        # Click login button
        login_button = wait.until(EC.element_to_be_clickable((By.XPATH, "//button[text()='Log in']")))
        login_button.click()

        # Check for alert (error)
        try:
            WebDriverWait(driver, 3).until(EC.alert_is_present())
            alert = driver.switch_to.alert
            alert_text = alert.text
            print(f"❌ [{browser_name}] Login alert: {alert_text}")
            alert.accept()
            return False
        except TimeoutException:
            pass  # No alert is good

        # Verify success
        welcome_message = wait.until(EC.visibility_of_element_located((By.ID, "nameofuser")))
        if username in welcome_message.text:
            print(f"✅ [{browser_name}] --- LOGIN SUCCESSFUL ---")
            return True
        else:
            print(f"❌ [{browser_name}] Unexpected welcome: {welcome_message.text}")
            return False

    except Exception as e:
        print(f"💥 [{browser_name}] Login error: {e}")
        return False


def run_demoblaze_test(driver, browser_name):
    """Complete test: Sign up + Login"""
    try:
        # Create unique username using timestamp
        timestamp = str(int(time.time()))
        username = f"testuser_{timestamp}_{browser_name.lower()}"
        password = "Test@1234"

        print(f"[{browser_name}] Navigating to DemoBlaze...")
        driver.get("https://www.demoblaze.com/")

        # Step 1: Sign up
        signup_success = signup_user(driver, browser_name, username, password)

        if signup_success:
            # Step 2: Login
            login_user(driver, browser_name, username, password)
        else:
            print(f"❌ [{browser_name}] Skipping login due to signup failure")

    except Exception as e:
        print(f"💥 [{browser_name}] An error occurred: {e}")
    finally:
        driver.quit()
        print(f"🔚 [{browser_name}] Browser session closed.")


# --- Browser-Specific Functions ---
def run_on_chrome():
    print("🚀 Thread starting for Chrome...")
    chrome_options = ChromeOptions()
    remote_driver = webdriver.Remote(
        command_executor=GRID_HUB_URL,
        options=chrome_options
    )
    run_demoblaze_test(remote_driver, "Chrome")


def run_on_edge():
    print("🚀 Thread starting for Edge...")
    edge_options = EdgeOptions()
    remote_driver = webdriver.Remote(
        command_executor=GRID_HUB_URL,
        options=edge_options
    )
    run_demoblaze_test(remote_driver, "Edge")


# --- Main Execution Block ---
def main():
    print("🎉 Starting Selenium Grid parallel test for DemoBlaze...")
    print("📝 This test will create a new user and login automatically\n")

    chrome_thread = threading.Thread(target=run_on_chrome)
    edge_thread = threading.Thread(target=run_on_edge)

    start_time = time.time()

    chrome_thread.start()
    edge_thread.start()

    chrome_thread.join()
    edge_thread.join()

    end_time = time.time()

    print("\n" + "=" * 50)
    print(f"🏁 All browser tests have completed in {end_time - start_time:.2f} seconds.")
    print("=" * 50)


if __name__ == "__main__":
    main()