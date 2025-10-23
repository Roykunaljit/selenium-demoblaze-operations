# from functools import wraps
# from selenium.webdriver.common.by import By
# from selenium.webdriver.support.ui import WebDriverWait
# from selenium.webdriver.support import expected_conditions as EC
#
#
# class FindBy:
#     """Custom FindBy decorator for Page Factory pattern"""
#
#     def __init__(self, by=By.ID, value=None, multiple=False):
#         self.by = by
#         self.value = value
#         self.multiple = multiple
#         self._element = None
#         self._elements = None
#
#     def __call__(self, func):
#         """Make this class callable as a decorator"""
#
#         @wraps(func)
#         def wrapper(instance):
#             if self.multiple:
#                 if self._elements is None:
#                     self._elements = instance.driver.find_elements(self.by, self.value)
#                 return self._elements
#             else:
#                 if self._element is None:
#                     self._element = instance.driver.find_element(self.by, self.value)
#                 return self._element
#
#         return wrapper
#
#     def reset(self):
#         """Reset cached elements"""
#         self._element = None
#         self._elements = None
#
#
# def find_by(by=By.ID, value=None, multiple=False):
#     """Factory function to create FindBy decorator"""
#     return FindBy(by, value, multiple)
#
#
# class PageFactory:
#     """Base class for Page Factory pattern"""
#
#     def __init__(self, driver):
#         self.driver = driver
#         self.wait = WebDriverWait(driver, 10)
#         self._cache = {}
#
#     def find_element_with_wait(self, by, value, timeout=10):
#         """Find element with explicit wait"""
#         wait = WebDriverWait(self.driver, timeout)
#         return wait.until(EC.presence_of_element_located((by, value)))
#
#     def find_elements_with_wait(self, by, value, timeout=10):
#         """Find elements with explicit wait"""
#         wait = WebDriverWait(self.driver, timeout)
#         wait.until(EC.presence_of_element_located((by, value)))
#         return self.driver.find_elements(by, value)
#
#     def clear_cache(self):
#         """Clear all cached elements"""
#         self._cache.clear()
#
#         # Clear cached elements in FindBy decorators
#         for attr_name in dir(self):
#             attr = getattr(self, attr_name)
#             if hasattr(attr, '__wrapped__'):
#                 if hasattr(attr, '__self__') and isinstance(attr.__self__, FindBy):
#                     attr.__self__.reset()

# utilities/page_factory.py
from functools import wraps
from selenium.webdriver.common.by import By
from selenium.common.exceptions import StaleElementReferenceException
import threading


class FindBy:
    """Thread-safe FindBy decorator for Page Factory pattern"""

    def __init__(self, by=By.ID, value=None, multiple=False):
        self.by = by
        self.value = value
        self.multiple = multiple
        self.cache_key = f"_cache_{by}_{value}_{multiple}"
        self._lock = threading.Lock()  # Thread safety

    def __call__(self, func):
        """Make this class callable as a decorator"""

        @wraps(func)
        def wrapper(instance):
            # Initialize instance-level cache if needed
            if not hasattr(instance, '_element_cache'):
                instance._element_cache = {}

            # Try to get cached element
            if self.cache_key in instance._element_cache:
                try:
                    cached = instance._element_cache[self.cache_key]

                    # Verify element is still valid (stale check)
                    if self.multiple:
                        if cached and len(cached) > 0:
                            # Check if first element is still in DOM
                            _ = cached[0].tag_name  # Will raise exception if stale
                            return cached
                    else:
                        # Check if element is still in DOM
                        _ = cached.tag_name  # Will raise exception if stale
                        return cached

                except (StaleElementReferenceException, AttributeError):
                    # Element is stale, will re-find below
                    del instance._element_cache[self.cache_key]

            # Find fresh element(s) with thread safety
            with self._lock:
                # Double-check after acquiring lock (another thread might have found it)
                if self.cache_key not in instance._element_cache:
                    if self.multiple:
                        elements = instance.driver.find_elements(self.by, self.value)
                        instance._element_cache[self.cache_key] = elements
                    else:
                        element = instance.driver.find_element(self.by, self.value)
                        instance._element_cache[self.cache_key] = element

                return instance._element_cache[self.cache_key]

        return wrapper

    def reset(self):
        """Reset is now handled by instance cache"""
        pass  # Not needed with instance-level cache


def find_by(by=By.ID, value=None, multiple=False):
    """Factory function to create FindBy decorator"""
    return FindBy(by, value, multiple)


class PageFactory:
    """Base class for Page Factory pattern with thread-safe caching"""

    def __init__(self, driver):
        self.driver = driver
        self._element_cache = {}  # Instance-level cache (thread-safe per instance)

    def clear_cache(self):
        """Clear all cached elements"""
        self._element_cache.clear()

    def find_element_with_wait(self, by, value, timeout=10):
        """Find element with explicit wait"""
        from selenium.webdriver.support.ui import WebDriverWait
        from selenium.webdriver.support import expected_conditions as EC

        wait = WebDriverWait(self.driver, timeout)
        return wait.until(EC.presence_of_element_located((by, value)))

    def find_elements_with_wait(self, by, value, timeout=10):
        """Find elements with explicit wait"""
        from selenium.webdriver.support.ui import WebDriverWait
        from selenium.webdriver.support import expected_conditions as EC

        wait = WebDriverWait(self.driver, timeout)
        wait.until(EC.presence_of_element_located((by, value)))
        return self.driver.find_elements(by, value)