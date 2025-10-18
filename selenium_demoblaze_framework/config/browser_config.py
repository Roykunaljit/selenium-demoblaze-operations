# config/browser_config.py

from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.firefox.service import Service as FirefoxService
from selenium.webdriver.edge.service import Service as EdgeService
from webdriver_manager.chrome import ChromeDriverManager
from webdriver_manager.firefox import GeckoDriverManager
from webdriver_manager.microsoft import EdgeChromiumDriverManager
from selenium.webdriver.chrome.options import Options as ChromeOptions
from selenium.webdriver.firefox.options import Options as FirefoxOptions
from selenium.webdriver.edge.options import Options as EdgeOptions
import configparser
import os


class BrowserConfig:
    def __init__(self):
        """Initialize the BrowserConfig class and load config.ini."""
        self.config = configparser.ConfigParser()
        config_path = os.path.join(os.path.dirname(__file__), 'config.ini')
        self.config.read(config_path)

    def get_chrome_options(self):
        """Configure Chrome options with all possible settings."""
        options = ChromeOptions()

        # Basic options
        if self.config.getboolean('DEFAULT', 'headless_mode'):
            options.add_argument('--headless')

        options.add_argument(f'--window-size={self.config.get("BROWSER_OPTIONS", "window_size")}')

        if self.config.getboolean('BROWSER_OPTIONS', 'start_maximized'):
            options.add_argument('--start-maximized')

        # Advanced stability/performance options
        if self.config.getboolean('BROWSER_OPTIONS', 'disable_gpu'):
            options.add_argument('--disable-gpu')
        if self.config.getboolean('BROWSER_OPTIONS', 'no_sandbox'):
            options.add_argument('--no-sandbox')
        if self.config.getboolean('BROWSER_OPTIONS', 'disable_dev_shm'):
            options.add_argument('--disable-dev-shm-usage')

        options.add_argument('--disable-extensions')
        options.add_argument('--disable-popup-blocking')
        options.add_argument('--ignore-certificate-errors')
        options.add_argument('--disable-web-security')
        options.add_argument('--allow-running-insecure-content')

        # Experimental options
        prefs = {
            'download.default_directory': os.path.join(os.getcwd(), 'downloads'),
            'download.prompt_for_download': False,
            'download.directory_upgrade': True,
            'safebrowsing.enabled': False,
            'profile.default_content_settings.popups': 0,
            'profile.content_settings.exceptions.automatic_downloads.*.setting': 1
        }
        options.add_experimental_option('prefs', prefs)
        options.add_experimental_option('excludeSwitches', ['enable-logging'])
        options.add_experimental_option('useAutomationExtension', False)

        # Enable performance logging
        options.set_capability('goog:loggingPrefs', {'performance': 'ALL'})

        return options

    def get_firefox_options(self):
        """Configure Firefox options."""
        options = FirefoxOptions()

        if self.config.getboolean('DEFAULT', 'headless_mode'):
            options.add_argument('--headless')

        window_size = self.config.get("BROWSER_OPTIONS", "window_size")
        width, height = window_size.split(',')
        options.add_argument(f'--width={width.strip()}')
        options.add_argument(f'--height={height.strip()}')

        # Firefox-specific preferences
        options.set_preference('dom.webnotifications.enabled', False)
        options.set_preference('geo.enabled', False)
        options.set_preference('media.volume_scale', 'linear')

        # Download preferences
        options.set_preference("browser.download.folderList", 2)
        options.set_preference("browser.download.manager.showWhenStarting", False)
        options.set_preference("browser.download.dir", os.path.join(os.getcwd(), 'downloads'))
        options.set_preference("browser.helperApps.neverAsk.saveToDisk",
                               "application/octet-stream,application/pdf,text/csv,application/csv,application/zip")

        return options

    def get_edge_options(self):
        """Configure Edge options."""
        options = EdgeOptions()

        if self.config.getboolean('DEFAULT', 'headless_mode'):
            options.add_argument('--headless')

        options.add_argument(f'--window-size={self.config.get("BROWSER_OPTIONS", "window_size")}')
        if self.config.getboolean('BROWSER_OPTIONS', 'start_maximized'):
            options.add_argument('--start-maximized')

        if self.config.getboolean('BROWSER_OPTIONS', 'disable_gpu'):
            options.add_argument('--disable-gpu')
        if self.config.getboolean('BROWSER_OPTIONS', 'no_sandbox'):
            options.add_argument('--no-sandbox')
        if self.config.getboolean('BROWSER_OPTIONS', 'disable_dev_shm'):
            options.add_argument('--disable-dev-shm-usage')

        options.add_argument('--disable-extensions')
        options.add_argument('--disable-popup-blocking')
        options.add_argument('--ignore-certificate-errors')

        return options

    def get_driver(self, browser_name=None):
        """Get configured WebDriver instance for the specified browser."""
        if not browser_name:
            browser_name = self.config.get('DEFAULT', 'browser').lower()

        if browser_name == 'chrome':
            service = ChromeService(ChromeDriverManager().install())
            driver = webdriver.Chrome(service=service, options=self.get_chrome_options())
        elif browser_name == 'firefox':
            service = FirefoxService(GeckoDriverManager().install())
            driver = webdriver.Firefox(service=service, options=self.get_firefox_options())
        elif browser_name == 'edge':
            service = EdgeService(EdgeChromiumDriverManager().install())
            driver = webdriver.Edge(service=service, options=self.get_edge_options())
        else:
            raise ValueError(f"Browser '{browser_name}' is not supported. Use 'chrome', 'firefox', or 'edge'.")

        # Set global timeouts
        driver.implicitly_wait(self.config.getint('DEFAULT', 'implicit_wait'))
        driver.set_page_load_timeout(self.config.getint('DEFAULT', 'page_load_timeout'))

        return driver