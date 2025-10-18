# import os
# import time
# import pyautogui
# from selenium.webdriver.common.by import By
# from selenium.webdriver.support.ui import WebDriverWait
# from selenium.webdriver.support import expected_conditions as EC
# from selenium.common.exceptions import TimeoutException
# import tkinter as tk
# from tkinter import filedialog
#
#
# class FileUploadUtils:
#     def __init__(self, driver, logger):
#         self.driver = driver
#         self.logger = logger
#         self.wait = WebDriverWait(driver, 10)
#
#     def upload_file_using_send_keys(self, file_input_locator, file_path):
#         """
#         Upload file using send_keys method (most reliable)
#         """
#         try:
#             if not os.path.exists(file_path):
#                 raise FileNotFoundError(f"File not found: {file_path}")
#
#             # Convert to absolute path if not already
#             absolute_path = os.path.abspath(file_path)
#
#             file_input = self.wait.until(EC.presence_of_element_located(file_input_locator))
#             file_input.send_keys(absolute_path)
#             self.logger.info(f"File uploaded using send_keys: {absolute_path}")
#             return True
#         except Exception as e:
#             self.logger.error(f"Failed to upload file using send_keys: {str(e)}")
#             return False
#
#     def upload_file_using_autoit(self, file_path, window_title="Open"):
#         """
#         Upload file using AutoIT (Windows only)
#         """
#         try:
#             import autoit
#             autoit.win_wait_active(window_title, 10)
#             autoit.control_send(window_title, "Edit1", file_path)
#             autoit.control_click(window_title, "Button1")
#             self.logger.info(f"File uploaded using AutoIT: {file_path}")
#             return True
#         except Exception as e:
#             self.logger.error(f"Failed to upload file using AutoIT: {str(e)}")
#             return False
#
#     def upload_file_using_pyautogui(self, file_path):
#         """
#         Upload file using PyAutoGUI (cross-platform)
#         """
#         try:
#             # Wait for file dialog to appear
#             time.sleep(2)
#
#             # Type the file path
#             pyautogui.write(file_path)
#             time.sleep(1)
#
#             # Press Enter to confirm
#             pyautogui.press('enter')
#             self.logger.info(f"File uploaded using PyAutoGUI: {file_path}")
#             return True
#         except Exception as e:
#             self.logger.error(f"Failed to upload file using PyAutoGUI: {str(e)}")
#             return False
#
#     def upload_file_using_robot(self, file_path):
#         """
#         Upload file using Java Robot (via JavaScript)
#         """
#         try:
#             script = """
#                 var robot = new java.awt.Robot();
#                 var path = arguments[0];
#                 for (var i = 0; i < path.length; i++) {
#                     robot.keyPress(path.charCodeAt(i));
#                     robot.keyRelease(path.charCodeAt(i));
#                 }
#                 robot.keyPress(java.awt.event.KeyEvent.VK_ENTER);
#                 robot.keyRelease(java.awt.event.KeyEvent.VK_ENTER);
#             """
#             self.driver.execute_script(script, file_path)
#             self.logger.info(f"File uploaded using Robot: {file_path}")
#             return True
#         except Exception as e:
#             self.logger.error(f"Failed to upload file using Robot: {str(e)}")
#             return False
#
#     def upload_multiple_files(self, file_input_locator, file_paths):
#         """
#         Upload multiple files at once
#         """
#         try:
#             file_input = self.wait.until(EC.presence_of_element_located(file_input_locator))
#
#             # Convert all paths to absolute paths
#             absolute_paths = [os.path.abspath(fp) for fp in file_paths]
#
#             # Join file paths with newline character
#             file_paths_str = '\n'.join(absolute_paths)
#             file_input.send_keys(file_paths_str)
#
#             self.logger.info(f"Multiple files uploaded: {len(file_paths)} files")
#             return True
#         except Exception as e:
#             self.logger.error(f"Failed to upload multiple files: {str(e)}")
#             return False
#
#     def create_test_file(self, file_path, content="Test file content"):
#         """
#         Create a test file for upload testing - returns absolute path
#         """
#         try:
#             # Create directory if it doesn't exist
#             os.makedirs(os.path.dirname(file_path), exist_ok=True)
#
#             # Write the file
#             with open(file_path, 'w') as f:
#                 f.write(content)
#
#             # Return absolute path
#             absolute_path = os.path.abspath(file_path)
#             self.logger.info(f"Test file created: {absolute_path}")
#             return absolute_path
#         except Exception as e:
#             self.logger.error(f"Failed to create test file: {str(e)}")
#             return None
#
#     def verify_file_upload(self, success_indicator_locator=None, timeout=10):
#         """
#         Verify if file upload was successful
#         """
#         try:
#             if success_indicator_locator:
#                 element = self.wait.until(EC.presence_of_element_located(success_indicator_locator))
#                 return element.is_displayed()
#             else:
#                 # Check for any success message or change in page
#                 time.sleep(timeout)
#                 return True
#         except TimeoutException:
#             return False
#
#     def handle_file_upload_dialog(self, file_path, method="pyautogui"):
#         """
#         Handle file upload dialog using specified method
#         """
#         methods = {
#             "pyautogui": self.upload_file_using_pyautogui,
#             "autoit": self.upload_file_using_autoit,
#             "robot": self.upload_file_using_robot
#         }
#
#         if method in methods:
#             return methods[method](file_path)
#         else:
#             self.logger.error(f"Unknown upload method: {method}")
#             return False
#
#     def select_file_dialog(self, title="Select a file"):
#         """
#         Open file selection dialog (for manual testing)
#         """
#         try:
#             root = tk.Tk()
#             root.withdraw()  # Hide the main window
#             file_path = filedialog.askopenfilename(title=title)
#             root.destroy()
#             return file_path
#         except Exception as e:
#             self.logger.error(f"Failed to open file dialog: {str(e)}")
#             return None

import os
import time
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException

# Conditional import of pyautogui
try:
    import pyautogui

    PYAUTOGUI_AVAILABLE = True
except (ImportError, KeyError):
    PYAUTOGUI_AVAILABLE = False

# Optional: Import for tkinter
try:
    import tkinter as tk
    from tkinter import filedialog

    TKINTER_AVAILABLE = True
except ImportError:
    TKINTER_AVAILABLE = False


class FileUploadUtils:
    def __init__(self, driver, logger):
        self.driver = driver
        self.logger = logger
        self.wait = WebDriverWait(driver, 10)

    def upload_file_using_send_keys(self, file_input_locator, file_path):
        """
        Upload file using send_keys method (most reliable)
        """
        try:
            if not os.path.exists(file_path):
                raise FileNotFoundError(f"File not found: {file_path}")

            # Convert to absolute path if not already
            absolute_path = os.path.abspath(file_path)

            file_input = self.wait.until(EC.presence_of_element_located(file_input_locator))
            file_input.send_keys(absolute_path)
            self.logger.info(f"File uploaded using send_keys: {absolute_path}")
            return True
        except Exception as e:
            self.logger.error(f"Failed to upload file using send_keys: {str(e)}")
            return False

    def upload_file_using_autoit(self, file_path, window_title="Open"):
        """
        Upload file using AutoIT (Windows only)
        """
        try:
            import autoit
            autoit.win_wait_active(window_title, 10)
            autoit.control_send(window_title, "Edit1", file_path)
            autoit.control_click(window_title, "Button1")
            self.logger.info(f"File uploaded using AutoIT: {file_path}")
            return True
        except Exception as e:
            self.logger.error(f"Failed to upload file using AutoIT: {str(e)}")
            return False

    def upload_file_using_pyautogui(self, file_path):
        """
        Upload file using PyAutoGUI (cross-platform)
        """
        if not PYAUTOGUI_AVAILABLE:
            self.logger.warning("PyAutoGUI is not available in this environment")
            return False

        try:
            # Wait for file dialog to appear
            time.sleep(2)

            # Type the file path
            pyautogui.write(file_path)
            time.sleep(1)

            # Press Enter to confirm
            pyautogui.press('enter')
            self.logger.info(f"File uploaded using PyAutoGUI: {file_path}")
            return True
        except Exception as e:
            self.logger.error(f"Failed to upload file using PyAutoGUI: {str(e)}")
            return False

    def upload_file_using_robot(self, file_path):
        """
        Upload file using Java Robot (via JavaScript)
        """
        try:
            script = """
                var robot = new java.awt.Robot();
                var path = arguments[0];
                for (var i = 0; i < path.length; i++) {
                    robot.keyPress(path.charCodeAt(i));
                    robot.keyRelease(path.charCodeAt(i));
                }
                robot.keyPress(java.awt.event.KeyEvent.VK_ENTER);
                robot.keyRelease(java.awt.event.KeyEvent.VK_ENTER);
            """
            self.driver.execute_script(script, file_path)
            self.logger.info(f"File uploaded using Robot: {file_path}")
            return True
        except Exception as e:
            self.logger.error(f"Failed to upload file using Robot: {str(e)}")
            return False

    def upload_multiple_files(self, file_input_locator, file_paths):
        """
        Upload multiple files at once
        """
        try:
            file_input = self.wait.until(EC.presence_of_element_located(file_input_locator))

            # Convert all paths to absolute paths
            absolute_paths = [os.path.abspath(fp) for fp in file_paths]

            # Join file paths with newline character
            file_paths_str = '\n'.join(absolute_paths)
            file_input.send_keys(file_paths_str)

            self.logger.info(f"Multiple files uploaded: {len(file_paths)} files")
            return True
        except Exception as e:
            self.logger.error(f"Failed to upload multiple files: {str(e)}")
            return False

    def create_test_file(self, file_path, content="Test file content"):
        """
        Create a test file for upload testing - returns absolute path
        """
        try:
            # Create directory if it doesn't exist
            os.makedirs(os.path.dirname(file_path), exist_ok=True)

            # Write the file
            with open(file_path, 'w') as f:
                f.write(content)

            # Return absolute path
            absolute_path = os.path.abspath(file_path)
            self.logger.info(f"Test file created: {absolute_path}")
            return absolute_path
        except Exception as e:
            self.logger.error(f"Failed to create test file: {str(e)}")
            return None

    def verify_file_upload(self, success_indicator_locator=None, timeout=10):
        """
        Verify if file upload was successful
        """
        try:
            if success_indicator_locator:
                element = self.wait.until(EC.presence_of_element_located(success_indicator_locator))
                return element.is_displayed()
            else:
                # Check for any success message or change in page
                time.sleep(timeout)
                return True
        except TimeoutException:
            return False

    def handle_file_upload_dialog(self, file_path, method="send_keys"):
        """
        Handle file upload dialog using specified method
        """
        methods = {
            "send_keys": lambda fp: True,  # send_keys doesn't open dialog
            "pyautogui": self.upload_file_using_pyautogui,
            "autoit": self.upload_file_using_autoit,
            "robot": self.upload_file_using_robot
        }

        if method in methods:
            if method == "pyautogui" and not PYAUTOGUI_AVAILABLE:
                self.logger.warning("PyAutoGUI method requested but not available")
                return False
            return methods[method](file_path)
        else:
            self.logger.error(f"Unknown upload method: {method}")
            return False

    def select_file_dialog(self, title="Select a file"):
        """
        Open file selection dialog (for manual testing)
        """
        if not TKINTER_AVAILABLE:
            self.logger.warning("Tkinter is not available in this environment")
            return None

        try:
            root = tk.Tk()
            root.withdraw()  # Hide the main window
            file_path = filedialog.askopenfilename(title=title)
            root.destroy()
            return file_path
        except Exception as e:
            self.logger.error(f"Failed to open file dialog: {str(e)}")
            return None