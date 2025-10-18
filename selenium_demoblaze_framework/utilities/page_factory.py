from functools import wraps
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


class FindBy:
    """Custom FindBy decorator for Page Factory pattern"""

    def __init__(self, by=By.ID, value=None, multiple=False):
        self.by = by
        self.value = value
        self.multiple = multiple
        self._element = None
        self._elements = None

    def __call__(self, func):
        """Make this class callable as a decorator"""

        @wraps(func)
        def wrapper(instance):
            if self.multiple:
                if self._elements is None:
                    self._elements = instance.driver.find_elements(self.by, self.value)
                return self._elements
            else:
                if self._element is None:
                    self._element = instance.driver.find_element(self.by, self.value)
                return self._element

        return wrapper

    def reset(self):
        """Reset cached elements"""
        self._element = None
        self._elements = None


def find_by(by=By.ID, value=None, multiple=False):
    """Factory function to create FindBy decorator"""
    return FindBy(by, value, multiple)


class PageFactory:
    """Base class for Page Factory pattern"""

    def __init__(self, driver):
        self.driver = driver
        self.wait = WebDriverWait(driver, 10)
        self._cache = {}

    def find_element_with_wait(self, by, value, timeout=10):
        """Find element with explicit wait"""
        wait = WebDriverWait(self.driver, timeout)
        return wait.until(EC.presence_of_element_located((by, value)))

    def find_elements_with_wait(self, by, value, timeout=10):
        """Find elements with explicit wait"""
        wait = WebDriverWait(self.driver, timeout)
        wait.until(EC.presence_of_element_located((by, value)))
        return self.driver.find_elements(by, value)

    def clear_cache(self):
        """Clear all cached elements"""
        self._cache.clear()

        # Clear cached elements in FindBy decorators
        for attr_name in dir(self):
            attr = getattr(self, attr_name)
            if hasattr(attr, '__wrapped__'):
                if hasattr(attr, '__self__') and isinstance(attr.__self__, FindBy):
                    attr.__self__.reset()