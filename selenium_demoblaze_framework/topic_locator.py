# import os
#
# # ==============================
# # TOPIC MAPPING
# # Format: "Topic Name": {
# #     "files": [{"path": "file.py", "lines": "approx line range or key lines"}]
# # }
# # ==============================
#
# TOPICS = {
#     "Browser Launching (Chrome/Firefox/Edge)": {
#         "files": [
#             {"path": "config/browser_config.py", "lines": "get_driver() method, lines ~45-75"},
#             {"path": "tests/test_demoblaze_e2e.py", "lines": "setup_and_teardown fixture, line ~50"}
#         ]
#     },
#     "WebDriver Methods (get, title, url, maximize, etc.)": {
#         "files": [
#             {"path": "pages/base_page.py",
#              "lines": "get_current_url(), get_title(), refresh_page(), etc., lines ~200-220"}
#         ]
#     },
#     "Locators (ID, Name, XPath, CSS, etc.)": {
#         "files": [
#             {"path": "pages/home_page.py", "lines": "All locator tuples like LOGO = (By.ID, 'nava'), lines ~10-50"},
#             {"path": "pages/product_page.py", "lines": "PRODUCT_NAME = (By.XPATH, ...), lines ~8-12"}
#         ]
#     },
#     "WebElement Methods (click, send_keys, text, etc.)": {
#         "files": [
#             {"path": "pages/base_page.py", "lines": "click(), send_keys(), get_text(), lines ~50-100"}
#         ]
#     },
#     "Radio Buttons": {
#     "files": [
#         {
#             "path": "tests/test_demoblaze_e2e.py",
#             "lines": "test_33_radio_button_demo() method, lines ~890-920 — demonstrates clicking and verifying radio buttons on https://demoqa.com/radio-button using label click + JS verification"
#         },
#         {
#             "path": "pages/base_page.py",
#             "lines": "is_selected() method (line ~140) — supports checking selection state of radio buttons/checkboxes"
#         },
#         {
#             "path": "utilities/utility_methods.py",
#             "lines": "execute_javascript() used in test to verify radio button state via 'checked' property"
#         }
#     ]
# },
#     "Checkboxes": {
#         "files": [
#             {"path": "pages/home_page.py",
#              "lines": "DAYS_CHECKBOXES dict (if used), or base_page.is_selected() supports it"},
#             {"path": "pages/base_page.py", "lines": "is_selected() method, line ~140"}
#         ]
#     },
#     "Dropdown Handling (Select class)": {
#         "files": [
#             {"path": "pages/base_page.py", "lines": "select_dropdown_by_text/value/index, lines ~150-170"},
#             {"path": "keywords/keywords.py", "lines": "select_dropdown() method, lines ~40-60"}
#         ]
#     },
#     "Web Tables": {
#         "files": [
#             {"path": "pages/home_page.py",
#              "lines": "get_all_products() parses product cards as table-like data, lines ~100-120"},
#             {"path": "pages/cart_page.py", "lines": "CART_ITEMS XPath, get_cart_items_count(), lines ~20-30"}
#         ]
#     },
#     "JavaScript Executor": {
#         "files": [
#             {"path": "utilities/utility_methods.py",
#              "lines": "execute_javascript(), execute_async_javascript(), lines ~120-130"},
#             {"path": "tests/test_demoblaze_e2e.py", "lines": "test_04_javascript_execution(), lines ~280-310"}
#         ]
#     },
#     "Scrolling (pixel, element, top/bottom)": {
#         "files": [
#             {"path": "utilities/utility_methods.py",
#              "lines": "scroll_to_bottom(), scroll_by_pixels(), etc., lines ~90-110"},
#             {"path": "tests/test_demoblaze_e2e.py", "lines": "test_07_scrolling_operations(), lines ~400-410"}
#         ]
#     },
#     "Screenshots (full, element, auto on fail)": {
#         "files": [
#             {"path": "utilities/utility_methods.py",
#              "lines": "take_screenshot(), take_element_screenshot(), lines ~40-80"},
#             {"path": "tests/test_demoblaze_e2e.py", "lines": "test_08_screenshot_operations(), lines ~415-425"}
#         ]
#     },
#     "Mouse Hover (ActionChains)": {
#         "files": [
#             {"path": "pages/base_page.py", "lines": "hover() method using ActionChains, line ~75"},
#             {"path": "tests/test_demoblaze_e2e.py", "lines": "test_02_mouse_operations(), lines ~240-260"}
#         ]
#     },
#     "Drag & Drop / Right Click / Double Click": {
#         "files": [
#             {"path": "pages/base_page.py", "lines": "drag_and_drop(), right_click(), double_click(), lines ~65-85"},
#             {"path": "tests/test_demoblaze_e2e.py", "lines": "test_02_mouse_operations(), lines ~260-280"}
#         ]
#     },
#     "Window/Tab Handling": {
#         "files": [
#             {"path": "pages/base_page.py", "lines": "switch_to_window(), get_all_window_handles(), lines ~180-190"},
#             {"path": "tests/test_demoblaze_e2e.py", "lines": "test_01_browser_windows_and_tabs(), lines ~220-240"}
#         ]
#     },
#     "Frame Handling": {
#         "files": [
#             {"path": "pages/base_page.py", "lines": "switch_to_frame(), switch_to_default_content(), lines ~175-180"},
#             {"path": "keywords/keywords.py", "lines": "switch_to_frame(), switch_to_default_content(), lines ~120-130"}
#         ]
#     },
#     "Alert Handling (accept/dismiss/send_keys)": {
#         "files": [
#             {"path": "pages/base_page.py",
#              "lines": "accept_alert(), dismiss_alert(), send_keys_to_alert(), lines ~190-210"},
#             {"path": "tests/test_demoblaze_e2e.py", "lines": "test_05_alerts_handling(), lines ~320-340"}
#         ]
#     },
#     "Waits (Implicit, Explicit, Custom)": {
#         "files": [
#             {"path": "config/browser_config.py", "lines": "implicit_wait set in get_driver(), line ~70"},
#             {"path": "pages/base_page.py", "lines": "wait_for_element_visible(), custom WebDriverWait, lines ~130-150"},
#             {"path": "tests/test_demoblaze_e2e.py", "lines": "test_09_wait_strategies(), lines ~430-450"}
#         ]
#     },
#     "File Upload (send_keys + pyautogui fallback)": {
#         "files": [
#             {"path": "utilities/file_upload_utils.py",
#              "lines": "upload_file_using_send_keys(), upload_file_using_pyautogui(), lines ~20-80"},
#             {"path": "tests/test_demoblaze_e2e.py", "lines": "test_31_file_upload(), lines ~950-980"},
#             {"path": "tests/test_file_upload.py", "lines": "Full test file for single/multiple upload"}
#         ]
#     },
#     "Broken Link Checker": {
#         "files": [
#             {"path": "utilities/link_checker_utils.py", "lines": "Full implementation"},
#             {"path": "tests/test_demoblaze_e2e.py", "lines": "test_32_broken_links_check(), lines ~985-1000"},
#             {"path": "tests/test_link_checker.py", "lines": "Dedicated test file"}
#         ]
#     },
#     "Pytest Framework (Fixtures, Parametrize, Markers)": {
#         "files": [
#             {"path": "tests/test_demoblaze_e2e.py",
#              "lines": "@pytest.fixture, @allure.feature, @pytest.mark.parametrize, lines ~50-100"},
#             {"path": "tests/test_base.py", "lines": "class_setup fixture, lines ~10-20"}
#         ]
#     },
#     "Page Object Model (POM)": {
#         "files": [
#             {"path": "pages/home_page.py", "lines": "Full POM class"},
#             {"path": "pages/product_page.py", "lines": "Full POM class"},
#             {"path": "pages/cart_page.py", "lines": "Full POM class"}
#         ]
#     },
#     "Page Factory Pattern": {
#         "files": [
#             {"path": "utilities/page_factory.py", "lines": "FindBy decorator, PageFactory base"},
#             {"path": "pages/home_page_factory.py", "lines": "HomePageFactory with @find_by decorators"},
#             {"path": "tests/test_page_factory.py", "lines": "Full test coverage"}
#         ]
#     },
#     "Data-Driven Testing (Excel, CSV, JSON, XML)": {
#         "files": [
#             {"path": "utilities/excel_utils.py", "lines": "Full Excel read/write"},
#             {"path": "utilities/csv_utils.py", "lines": "Full CSV support"},
#             {"path": "utilities/json_utils.py", "lines": "Full JSON support"},
#             {"path": "utilities/xml_utils.py", "lines": "Full XML support"},
#             {"path": "tests/test_demoblaze_e2e.py", "lines": "test_10 to test_13, lines ~460-520"}
#         ]
#     },
#     "Keyword-Driven Framework": {
#         "files": [
#             {"path": "utilities/keyword_engine.py", "lines": "Full engine"},
#             {"path": "keywords/keywords.py", "lines": "All keywords"},
#             {"path": "tests/test_keyword_driven.py", "lines": "Test execution"},
#             {"path": "data/keyword_test_cases.xlsx", "lines": "Test data file"}
#         ]
#     },
#     "Modular Framework": {
#         "files": [
#             {"path": "pages/", "lines": "Each page is a module"},
#             {"path": "utilities/", "lines": "Each utility is a module (logging, upload, etc.)"}
#         ]
#     },
#     "Custom Logger": {
#         "files": [
#             {"path": "utilities/custom_logger.py", "lines": "Full implementation"},
#             {"path": "pages/base_page.py", "lines": "Logger passed to all pages"}
#         ]
#     },
#     "Selenium Grid (Parallel Execution)": {
#         "files": [
#             {"path": "tests/test_demoblaze_e2e.py", "lines": "Not implemented in main flow"},
#             {"path": "[External] grid_parallel.py (from knowledge base)", "lines": "Threading-based parallel demo"}
#         ]
#     },
#     "Network Emulation (Chrome CDP)": {
#         "files": [
#             {"path": "utilities/utility_methods.py", "lines": "set_network_conditions(), lines ~280-290"},
#             {"path": "tests/test_demoblaze_e2e.py", "lines": "test_27_network_emulation(), lines ~880-890"}
#         ]
#     },
#     "Local/Session Storage": {
#         "files": [
#             {"path": "utilities/utility_methods.py", "lines": "get/set/clear local/session storage, lines ~290-310"},
#             {"path": "tests/test_demoblaze_e2e.py", "lines": "test_14_storage_operations(), lines ~530-540"}
#         ]
#     },
#     "Performance Metrics": {
#         "files": [
#             {"path": "utilities/utility_methods.py", "lines": "get_performance_metrics(), lines ~270-275"},
#             {"path": "tests/test_demoblaze_e2e.py", "lines": "test_15_performance_metrics(), lines ~545-555"}
#         ]
#     },
#     "Faker Data Generation": {
#         "files": [
#             {"path": "utilities/utility_methods.py", "lines": "generate_random_email/name/phone, lines ~230-250"},
#             {"path": "tests/test_demoblaze_e2e.py", "lines": "test_19_faker_data_generation(), lines ~600-610"}
#         ]
#     },
#     "End-to-End Shopping Flow": {
#         "files": [
#             {"path": "tests/test_demoblaze_e2e.py", "lines": "test_20_complete_e2e_flow(), lines ~620-720"}
#         ]
#     },
#     "Allure Reporting": {
#         "files": [
#             {"path": "tests/test_demoblaze_e2e.py", "lines": "@allure.feature/story decorators, lines ~220-1000"}
#         ]
#     },
#     "HTML Test Reporting": {
#         "files": [
#             {"path": "utilities/keyword_engine.py", "lines": "generate_test_report(), lines ~300-400"},
#             {"path": "utilities/link_checker_utils.py", "lines": "generate_link_report(), lines ~200-300"}
#         ]
#     }
# }
#
#
# def main():
#     print("=" * 80)
#     print("🔍 SELENIUM AUTOMATION TOPIC LOCATOR")
#     print("   Shows exactly where each topic is implemented in your codebase")
#     print("=" * 80)
#
#     # Display topics
#     topic_list = list(TOPICS.keys())
#     for i, topic in enumerate(topic_list, 1):
#         print(f"{i:2}. {topic}")
#
#     print("\nEnter topic number to see implementation details (or 'q' to quit):")
#
#     while True:
#         choice = input("> ").strip()
#         if choice.lower() == 'q':
#             print("Goodbye!")
#             break
#         if not choice.isdigit():
#             print("❌ Please enter a valid number or 'q'")
#             continue
#
#         idx = int(choice)
#         if idx < 1 or idx > len(topic_list):
#             print(f"❌ Please enter a number between 1 and {len(topic_list)}")
#             continue
#
#         topic = topic_list[idx - 1]
#         info = TOPICS[topic]
#
#         print("\n" + "=" * 80)
#         print(f"📘 TOPIC: {topic}")
#         print("=" * 80)
#         for file_info in info["files"]:
#             print(f"\n📁 File: {file_info['path']}")
#             print(f"   📍 Location: {file_info['lines']}")
#             # Optional: Check if file exists
#             if os.path.exists(file_info['path']):
#                 print("   ✅ File exists")
#             else:
#                 print("   ⚠️  File not found in current directory")
#         print("\n" + "=" * 80)
#
#
# if __name__ == "__main__":
#     main()

# import os
# import sys
#
#
# # =================================================================================
# #  Comprehensive Topic Mapping for Selenium DemoBlaze Automation Framework
# #  This script maps every concept from the syllabus to its implementation
# #  in the codebase, providing file paths and specific locations.
# # =================================================================================
#
# # --- Helper function for colored output and file checking ---
# def print_topic_details(topic_name, files_info):
#     """Prints topic details with colored output and file existence check."""
#     # ANSI color codes
#     COLOR = {
#         "HEADER": "\033[95m",
#         "BLUE": "\033[94m",
#         "GREEN": "\033[92m",
#         "YELLOW": "\033[93m",
#         "RED": "\033[91m",
#         "ENDC": "\033[0m",
#         "BOLD": "\033[1m",
#         "UNDERLINE": "\033[4m"
#     }
#     print("\n" + "=" * 80)
#     print(f"{COLOR['HEADER']}{COLOR['BOLD']}📘 TOPIC: {topic_name}{COLOR['ENDC']}")
#     print("=" * 80)
#     for file_info in files_info:
#         path = file_info['path']
#         location = file_info['lines']
#         exists = os.path.exists(path)
#         status_color = COLOR['GREEN'] if exists else COLOR['RED']
#         status_text = "✅ File Exists" if exists else "❌ File NOT Found"
#
#         print(f"\n{COLOR['BLUE']}📁 File: {COLOR['BOLD']}{path}{COLOR['ENDC']}")
#         print(f"   {COLOR['YELLOW']}📍 Location:{COLOR['ENDC']} {location}")
#         print(f"   {status_color}{status_text}{COLOR['ENDC']}")
#     print("\n" + "=" * 80)
#
#
# # ==============================
# # REFINED TOPIC MAPPING
# # ==============================
#
# TOPICS = {
#     "1. Introduction & Core Python Concepts": {
#         "files": [
#             {"path": "README.md", "lines": "Project overview demonstrating automation principles."},
#             {"path": "tests/test_demoblaze_e2e.py",
#              "lines": "Demonstrates practical use of OOPS (classes), loops, conditions, and collections."}
#         ]
#     },
#     "2. Browser Launching (Chrome/Firefox/Edge)": {
#         "files": [
#             {"path": "config/browser_config.py",
#              "lines": "Method `get_driver()` handles multi-browser setup and configuration."},
#             {"path": "config/config.ini", "lines": "Browser type and options are configured here."}
#         ]
#     },
#     "3. WebDriver Methods (get, title, url, etc.)": {
#         "files": [
#             {"path": "pages/base_page.py",
#              "lines": "Methods like `get_current_url()`, `get_title()`, `refresh_page()`, `go_back()`, `go_forward()`."}
#         ]
#     },
#     "4. Navigation Commands": {
#         "files": [
#             {"path": "pages/base_page.py", "lines": "Methods `go_back()` and `go_forward()`."},
#             {"path": "tests/test_demoblaze_e2e.py",
#              "lines": "Test `test_18_browser_navigation()` validates all navigation commands."}
#         ]
#     },
#     "5. Locators (ID, XPath, CSS, Class Name, etc.)": {
#         "files": [
#             {"path": "pages/home_page.py",
#              "lines": "All locators defined as tuples, e.g., `LOGO = (By.ID, 'nava')`, `PHONES_CATEGORY = (By.XPATH, ...)`."},
#             {"path": "pages/cart_page.py", "lines": "Examples of various locators for cart elements."}
#         ]
#     },
#     "6. WebElement Methods (click, send_keys, text, is_displayed)": {
#         "files": [
#             {"path": "pages/base_page.py",
#              "lines": "Wrapper methods `click()`, `send_keys()`, `get_text()`, `is_displayed()`, `is_enabled()`, `is_selected()`."}
#         ]
#     },
#     "7. Radio Buttons": {
#     "files": [
#         {"path": "tests/test_demoblaze_e2e.py", "lines": "Test `test_33_radio_button_demo()` provides a full demonstration."},
#         {"path": "pages/base_page.py", "lines": "Method `is_selected()` is used to check the state."}
#     ]
# },
# "8. Radio Buttons & Checkboxes": {
#     "files": [
#         {"path": "tests/test_demoblaze_e2e.py",
#          "lines": "Test `test_33_radio_button_demo()` interacts with radio buttons on an external site."},
#         {"path": "tests/test_checkboxes.py",
#          "lines": "Test `test_local_checkbox_interaction()` provides a 100% reliable demonstration by creating and testing against its own local HTML page."},
#         {"path": "pages/base_page.py",
#          "lines": "Method `is_selected()` is used to check the state of both element types."}
#     ]
# },
#     "9. Handling Multiple WebElements (find_elements)": {
#         "files": [
#             {"path": "pages/home_page.py",
#              "lines": "Method `get_all_products()` uses `find_elements` to get a list of all product cards."},
#             {"path": "pages/cart_page.py",
#              "lines": "Method `get_cart_items_count()` uses `find_elements` to count table rows."}
#         ]
#     },
#     "10. Dropdown Handling (Select Class)": {
#         "files": [
#             {"path": "pages/base_page.py",
#              "lines": "Methods `select_dropdown_by_value/text/index` using the `Select` class."},
#             {"path": "keywords/keywords.py", "lines": "Keyword `select_dropdown` also demonstrates this capability."}
#         ]
#     },
#     "11. Web Tables": {
#         "files": [
#             {"path": "pages/cart_page.py",
#              "lines": "The cart is a web table. Locator `CART_ITEMS` targets table rows (`//tbody//tr`)."}
#         ]
#     },
#     "12. JavaScript Executor": {
#         "files": [
#             {"path": "utilities/utility_methods.py",
#              "lines": "Methods `execute_javascript()` and `execute_async_javascript()`."},
#             {"path": "tests/test_demoblaze_e2e.py",
#              "lines": "Test `test_04_javascript_execution()` demonstrates scrolling, highlighting, and async execution."}
#         ]
#     },
#     "13. Scrolling (Up, Down, To Element)": {
#         "files": [
#             {"path": "utilities/utility_methods.py",
#              "lines": "Methods `scroll_to_bottom()`, `scroll_to_top()`, `scroll_to_element()`."},
#             {"path": "tests/test_demoblaze_e2e.py",
#              "lines": "Test `test_07_scrolling_operations()` validates all scrolling types."}
#         ]
#     },
#     "14. Screenshots (Full Page, Element, On Failure)": {
#         "files": [
#             {"path": "utilities/utility_methods.py",
#              "lines": "Methods `take_screenshot()` and `take_element_screenshot()`."},
#             {"path": "tests/conftest.py",
#              "lines": "Pytest hook `pytest_runtest_makereport` automatically takes a screenshot on test failure."},
#             {"path": "tests/test_demoblaze_e2e.py",
#              "lines": "Test `test_08_screenshot_operations()` explicitly tests screenshot features."}
#         ]
#     },
#     "15. Mouse Actions (Hover, Right/Double Click, Drag & Drop)": {
#         "files": [
#             {"path": "pages/base_page.py",
#              "lines": "Methods `hover()`, `right_click()`, `double_click()`, and `drag_and_drop()` using `ActionChains`."},
#             {"path": "tests/test_demoblaze_e2e.py",
#              "lines": "Test `test_02_mouse_operations()` demonstrates hover, right-click, and double-click."}
#         ]
#     },
#     "16. Window and Tab Handling": {
#         "files": [
#             {"path": "pages/base_page.py",
#              "lines": "Methods `switch_to_window()`, `get_current_window_handle()`, `get_all_window_handles()`."},
#             {"path": "tests/test_demoblaze_e2e.py",
#              "lines": "Test `test_01_browser_windows_and_tabs()` provides a full demonstration."}
#         ]
#     },
#     "17. Frame Handling": {
#         "files": [
#             {"path": "pages/base_page.py",
#              "lines": "Methods `switch_to_frame()` and `switch_to_default_content()` provide the capability."}
#         ]
#     },
#     "18. Alert Handling": {
#         "files": [
#             {"path": "pages/base_page.py",
#              "lines": "Methods `accept_alert()`, `dismiss_alert()`, and `send_keys_to_alert()`."},
#             {"path": "tests/test_demoblaze_e2e.py",
#              "lines": "Test `test_05_alerts_handling()` validates alert interactions."}
#         ]
#     },
#     "19. Waits (Implicit & Explicit)": {
#         "files": [
#             {"path": "config/browser_config.py",
#              "lines": "Implicit wait is set globally in the `get_driver()` method."},
#             {"path": "pages/base_page.py",
#              "lines": "`WebDriverWait` (explicit wait) is used as the primary wait strategy for all element interactions."},
#             {"path": "tests/test_demoblaze_e2e.py",
#              "lines": "Test `test_09_wait_strategies()` demonstrates various explicit wait conditions."}
#         ]
#     },
#     "20. File Uploading (send_keys & pyautogui)": {
#         "files": [
#             {"path": "utilities/file_upload_utils.py",
#              "lines": "Contains multiple upload methods like `upload_file_using_send_keys()`."},
#             {"path": "tests/test_demoblaze_e2e.py",
#              "lines": "Test `test_31_file_upload()` demonstrates uploading via `send_keys` on a live site."}
#         ]
#     },
#     "21. Broken Link Checking": {
#         "files": [
#             {"path": "utilities/utility_methods.py",
#              "lines": "Method `check_broken_links()` uses the `requests` library to validate links."},
#             {"path": "tests/test_demoblaze_e2e.py",
#              "lines": "Test `test_32_broken_links_check()` executes the link checker."}
#         ]
#     },
#     "22. Pytest Framework (Fixtures, Parametrize)": {
#         "files": [
#             {"path": "tests/conftest.py", "lines": "Project-wide fixtures and hooks."},
#             {"path": "tests/test_demoblaze_e2e.py",
#              "lines": "Use of `@pytest.fixture` for setup and `@pytest.mark.parametrize` for data-driven tests."}
#         ]
#     },
#     "23. Assertions & Validations": {
#         "files": [
#             {"path": "tests/test_demoblaze_e2e.py",
#              "lines": "Every test uses `assert` statements to validate outcomes, e.g., `assert self.home_page.is_user_logged_in()`."}
#         ]
#     },
#     "24. Negative Testing": {
#         "files": [
#             {"path": "tests/test_demoblaze_e2e.py",
#              "lines": "Tests `test_21_invalid_login()` and `test_22_duplicate_signup()` check for expected error messages."}
#         ]
#     },
#     "25. Page Object Model (POM)": {
#         "files": [
#             {"path": "pages/base_page.py", "lines": "The base class for all page objects, promoting reusability."},
#             {"path": "pages/home_page.py",
#              "lines": "A complete Page Object class for the home page, encapsulating locators and methods."}
#         ]
#     },
#     "26. Page Factory Pattern": {
#         "files": [
#             {"path": "utilities/page_factory.py",
#              "lines": "Custom implementation of the Page Factory pattern using decorators."},
#             {"path": "pages/home_page_factory.py",
#              "lines": "Example page class (`HomePageFactory`) using the `@find_by` decorator."},
#             {"path": "tests/test_page_factory.py",
#              "lines": "Dedicated tests to validate the Page Factory implementation."}
#         ]
#     },
#     "27. Data-Driven Framework (Excel, CSV, JSON, XML)": {
#         "files": [
#             {"path": "utilities/excel_utils.py", "lines": "Utility for reading from and writing to Excel files."},
#             {"path": "utilities/csv_utils.py", "lines": "Utility for handling CSV files."},
#             {"path": "tests/test_demoblaze_e2e.py",
#              "lines": "Tests `test_10_...` through `test_13_...` demonstrate reading data from all file types."}
#         ]
#     },
#     "28. Keyword-Driven Framework": {
#         "files": [
#             {"path": "utilities/keyword_engine.py",
#              "lines": "The core engine that reads keywords from Excel and executes Selenium commands."},
#             {"path": "tests/test_keyword_driven.py", "lines": "Pytest test that runs the keyword engine."},
#             {"path": "data/keyword_test_cases.xlsx",
#              "lines": "The external Excel sheet containing test steps and data."}
#         ]
#     },
#     "29. Modular-Driven Framework": {
#         "files": [
#             {"path": "project_structure.txt",
#              "lines": "The project is structured into independent modules: `config`, `pages`, `tests`, `utilities`."},
#             {"path": "utilities/custom_logger.py", "lines": "An example of a reusable, independent utility module."}
#         ]
#     },
#     "30. Hybrid Framework": {
#         "files": [
#             {"path": "README.md",
#              "lines": "The framework is a Hybrid model, combining POM, Data-Driven, and Keyword-Driven approaches for maximum flexibility."}
#         ]
#     },
#     "31. Reporting (HTML & Allure)": {
#         "files": [
#             {"path": ".github/workflows/run-tests.yml",
#              "lines": "Commands to generate both `pytest-html` and `Allure` reports during CI/CD."},
#             {"path": "tests/test_demoblaze_e2e.py",
#              "lines": "Use of `@allure.feature` and `@allure.story` decorators to structure Allure reports."}
#         ]
#     },
#     "32. CI/CD Integration (GitHub Actions)": {
#         "files": [
#             {"path": ".github/workflows/run-tests.yml",
#              "lines": "Complete workflow for automated testing on push/pull_request, including setup, execution, and report deployment."}
#         ]
#     },
#     "33. Selenium Grid / Cloud Testing": {
#         "files": [
#             {"path": "README.md",
#              "lines": "These are advanced topics not covered in the current implementation. The framework is, however, ready for Grid integration by modifying `browser_config.py` to use `webdriver.Remote`."}
#         ]
#     }
# }
#
#
# def main():
#     """Main function to run the interactive topic locator."""
#     print("=" * 80)
#     print("🔍 SELENIUM AUTOMATION TOPIC LOCATOR")
#     print("   Shows exactly where each topic is implemented in your codebase")
#     print("=" * 80)
#
#     # Display topics
#     topic_list = list(TOPICS.keys())
#     for topic in topic_list:
#         print(f"   {topic}")
#
#     print("\n" + "-" * 80)
#     print("Enter topic number (e.g., '5') to see implementation details.")
#     print("Enter 'all' to display details for every topic.")
#     print("Enter 'q' to quit.")
#     print("-" * 80)
#
#     while True:
#         choice = input("> ").strip().lower()
#         if choice == 'q':
#             print("Goodbye!")
#             break
#         if choice == 'all':
#             for topic_name in topic_list:
#                 info = TOPICS[topic_name]
#                 print_topic_details(topic_name, info["files"])
#             continue
#
#         if not choice.isdigit():
#             print("❌ Please enter a valid number, 'all', or 'q'")
#             continue
#
#         idx = int(choice)
#         if not 1 <= idx <= len(topic_list):
#             print(f"❌ Please enter a number between 1 and {len(topic_list)}")
#             continue
#
#         topic_name = topic_list[idx - 1]
#         info = TOPICS[topic_name]
#         print_topic_details(topic_name, info["files"])
#
#
# if __name__ == "__main__":
#     # Add project root to path to ensure file checks work from any directory
#     project_root = os.path.dirname(os.path.abspath(__file__))
#     os.chdir(project_root)
#     sys.path.insert(0, project_root)
#     main()

#
# import os
# import sys


# =================================================================================
#  Comprehensive Topic Mapping for Selenium DemoBlaze Automation Framework
# #  This script provides detailed explanations of each automation concept and maps
# #  it directly to its implementation within this project's codebase.
# # =================================================================================
#
#
# # --- Helper function for colored output and file checking ---
# def print_topic_details(topic_name, files_info):
#     """Prints topic details with colored output and file existence check."""
#     # ANSI color codes for better readability
#     COLOR = {
#         "HEADER": "\033[95m", "BLUE": "\033[94m", "GREEN": "\033[92m",
#         "YELLOW": "\033[93m", "RED": "\033[91m", "ENDC": "\033[0m",
#         "BOLD": "\033[1m", "UNDERLINE": "\033[4m"
#     }
#     print("\n" + "=" * 100)
#     print(f"{COLOR['HEADER']}{COLOR['BOLD']}📘 TOPIC: {topic_name}{COLOR['ENDC']}")
#     print("=" * 100)
#     for file_info in files_info:
#         path = file_info['path']
#         description = file_info['description']
#         exists = os.path.exists(path)
#
#         # Show absolute path for debugging
#         abs_path = os.path.abspath(path)
#
#         status_color = COLOR['GREEN'] if exists else COLOR['RED']
#         status_text = "✅ File Exists" if exists else "❌ File NOT Found"
#
#         print(
#             f"\n{COLOR['BLUE']}📁 Reference File: {COLOR['BOLD']}{path}{COLOR['ENDC']}  ({status_color}{status_text}{COLOR['ENDC']})")
#         if not exists:
#             print(f"   {COLOR['RED']}🔍 Looked at: {abs_path}{COLOR['ENDC']}")
#         print(f"\n{COLOR['YELLOW']}💡 Description & Implementation Details:{COLOR['ENDC']}\n{description}")
#     print("\n" + "=" * 100)
#
#
# # =================================================================================
# #                             REFINED TOPIC MAPPING
# # =================================================================================
#
# TOPICS = {
#     # --- Framework Fundamentals ---
#     "1. Hybrid Framework Architecture": {
#         "files": [
#             {
#                 "path": "README.md",
#                 "description": (
#                     "CONCEPT: A Hybrid Framework combines the strengths of multiple framework types to create a more robust, flexible, and scalable solution.\n\n"
#                     "PROJECT IMPLEMENTATION:\n"
#                     "This project is a classic Hybrid Framework that integrates:\n"
#                     "1. Page Object Model (POM): For separating UI elements and interactions from test logic (see Topic 9).\n"
#                     "2. Data-Driven Framework: For running the same test logic with multiple datasets from external files (see Topic 11).\n"
#                     "3. Keyword-Driven Framework: For abstracting complex actions into simple keywords, allowing test creation in a data table (see Topic 12).\n"
#                     "4. Modular Framework: The project is broken down into logical, reusable modules (`config`, `pages`, `utilities`, `tests`)."
#                 )
#             }
#         ]
#     },
#     "2. Pytest Framework (Fixtures & Markers)": {
#         "files": [
#             {
#                 "path": "tests/test_demoblaze_e2e.py",
#                 "description": (
#                     "CONCEPT: A fixture is a function that runs before (and optionally after) a test function. It's used for setup and teardown, such as creating a browser session, logging in a user, or loading test data.\n\n"
#                     "PROJECT IMPLEMENTATION:\n"
#                     "The `@pytest.fixture(autouse=True)` in `setup_and_teardown` is the heart of every test class. For each test function, this fixture automatically:\n"
#                     "  - BEFORE THE TEST (`yield`): Initializes a logger, creates a fresh browser instance using `BrowserConfig`, instantiates all Page Objects (`HomePage`, `ProductPage`, etc.), and navigates to the base URL.\n"
#                     "  - AFTER THE TEST (after `yield`): Logs completion and calls `driver.quit()` to cleanly close the browser and end the session. This ensures every test runs in isolation."
#                 )
#             },
#             {
#                 "path": "pytest.ini",
#                 "description": (
#                     "CONCEPT: Markers are custom tags used to group tests (e.g., 'smoke', 'regression'). You can then choose to run only a specific group of tests.\n\n"
#                     "PROJECT IMPLEMENTATION:\n"
#                     "This file defines custom markers like `smoke` and `regression`. A test can be marked with `@pytest.mark.smoke` to be included in the smoke test suite. You can run only these tests using the command: `pytest -m smoke`."
#                 )
#             }
#         ]
#     },
#     # --- Core Selenium Interactions ---
#     "3. Browser Launching & Configuration": {
#         "files": [
#             {
#                 "path": "config/browser_config.py",
#                 "description": (
#                     "CONCEPT: WebDriver configuration involves setting up the browser driver (e.g., chromedriver) and applying specific options like headless mode, window size, or performance flags.\n\n"
#                     "PROJECT IMPLEMENTATION:\n"
#                     "The `get_driver()` method is the central factory for creating WebDriver instances. It reads the `config.ini` file to determine which browser to launch (`chrome`, `edge`, `firefox`).\n"
#                     "  - It calls browser-specific methods like `get_chrome_options()` to apply all configurations (headless, window size, disabling GPU, etc.).\n"
#                     "  - It uses `webdriver-manager` to automatically download and manage the correct driver executables, avoiding manual setup."
#                 )
#             }
#         ]
#     },
#     "4. Locators & WebElement Interaction": {
#         "files": [
#             {
#                 "path": "pages/home_page.py",
#                 "description": (
#                     "CONCEPT: Locators are strategies used to find elements on a web page (e.g., By.ID, By.XPATH). Once an element is found, you can interact with it using methods like `.click()`, `.send_keys()`, or retrieve its properties like `.text`.\n\n"
#                     "PROJECT IMPLEMENTATION:\n"
#                     "  - LOCATORS: This file defines all locators as constant tuples at the top of the class, e.g., `LOGO = (By.ID, 'nava')`. This makes them easy to manage and reuse.\n"
#                     "  - INTERACTIONS: Methods like `login(username, password)` use these locators to perform actions: `self.send_keys(self.LOGIN_USERNAME, username)`."
#                 )
#             },
#             {
#                 "path": "pages/base_page.py",
#                 "description": (
#                     "CONCEPT: To improve reliability and reusability, it's best to create wrapper methods for common Selenium interactions.\n\n"
#                     "PROJECT IMPLEMENTATION:\n"
#                     "This base class contains robust wrapper methods for all standard interactions. For example, the `click()` method first waits for the element to be clickable (`EC.element_to_be_clickable`). If a standard click fails (e.g., the element is obscured), it has a fallback mechanism to perform a click using JavaScript (`driver.execute_script`). This makes the tests much more stable."
#                 )
#             }
#         ]
#     },
#     # --- Advanced Interactions & Topics ---
#     "5. Waits (Implicit & Explicit)": {
#         "files": [
#             {
#                 "path": "config/browser_config.py",
#                 "description": (
#                     "CONCEPT: An implicit wait tells WebDriver to poll the DOM for a certain amount of time when trying to find an element if it's not immediately available. It is set once per session.\n\n"
#                     "PROJECT IMPLEMENTATION:\n"
#                     "At the end of the `get_driver()` method, `driver.implicitly_wait(...)` is called. The wait time is loaded from `config.ini`, making it easy to configure."
#                 )
#             },
#             {
#                 "path": "pages/base_page.py",
#                 "description": (
#                     "CONCEPT: An explicit wait is a code you define to wait for a certain condition to occur before proceeding further in the code. It is more precise and reliable than an implicit wait.\n\n"
#                     "PROJECT IMPLEMENTATION:\n"
#                     "This framework relies heavily on explicit waits for maximum stability. A `WebDriverWait` instance is initialized in the `__init__` method. Every interaction method, like `find_element()`, `click()`, etc., uses this wait with an Expected Condition (`EC`), such as `EC.presence_of_element_located` or `EC.element_to_be_clickable`. This ensures the script only proceeds when the app is ready."
#                 )
#             }
#         ]
#     },
#     "6. Handling Dropdowns, Checkboxes & Radio Buttons": {
#         "files": [
#             {
#                 "path": "tests/test_dropdown.py",
#                 "description": (
#                     "CONCEPT: Standard dropdowns (`<select>` tags) are handled using Selenium's `Select` class. This provides easy methods to select options by their text, value, or index.\n\n"
#                     "PROJECT IMPLEMENTATION:\n"
#                     "Since the DemoBlaze site has no dropdowns, this dedicated test file was created. It starts a local web server with a custom HTML page containing a dropdown. The test then calls the methods from `base_page.py` (`select_dropdown_by_value`, `select_dropdown_by_text`, etc.) to interact with the dropdown and verifies the selection was successful. This proves the framework's capability."
#                 )
#             },
#             {
#                 "path": "tests/test_checkboxes.py",
#                 "description": (
#                     "CONCEPT: Checkboxes are input elements that can be checked for their selection state using the `.is_selected()` method.\n\n"
#                     "PROJECT IMPLEMENTATION:\n"
#                     "Similar to the dropdowns test, this file creates a local HTML page with checkboxes to provide a reliable test environment. It uses the `base_page.click()` method to toggle the checkboxes and `base_page.is_selected()` to assert their initial and final states."
#                 )
#             }
#         ]
#     },
#     "7. Mouse Actions (ActionChains)": {
#         "files": [
#             {
#                 "path": "pages/base_page.py",
#                 "description": (
#                     "CONCEPT: The `ActionChains` class is used to automate complex user interactions like hovering, right-clicking, double-clicking, and dragging-and-dropping.\n\n"
#                     "PROJECT IMPLEMENTATION:\n"
#                     "This file provides wrapper methods for these actions: `hover()`, `right_click()`, `double_click()`, and `drag_and_drop()`. Each method creates an `ActionChains` instance, chains the desired action, and calls `.perform()` to execute it."
#                 )
#             },
#             {
#                 "path": "tests/test_demoblaze_e2e.py",
#                 "description": (
#                     "The `test_02_mouse_operations()` test specifically validates these actions by hovering over menu items, right-clicking the logo, and double-clicking a product to navigate to its page."
#                 )
#             }
#         ]
#     },
#     "8. Alert, Frame, and Window Handling": {
#         "files": [
#             {
#                 "path": "pages/base_page.py",
#                 "description": (
#                     "CONCEPT: Selenium provides methods to switch the driver's focus between different contexts like browser windows/tabs, iframes, and JavaScript alerts.\n\n"
#                     "PROJECT IMPLEMENTATION:\n"
#                     "This file contains dedicated methods for each context:\n"
#                     "  - ALERTS: `accept_alert()`, `dismiss_alert()`, and `send_keys_to_alert()` wait for an alert to be present and then interact with it.\n"
#                     "  - WINDOWS: `switch_to_window()`, `get_all_window_handles()` allow the test to move between different browser tabs.\n"
#                     "  - FRAMES: `switch_to_frame()` and `switch_to_default_content()` are provided for handling iframes."
#                 )
#             },
#             {
#                 "path": "tests/test_demoblaze_e2e.py",
#                 "description": (
#                     "The `test_01_browser_windows_and_tabs()` and `test_05_alerts_handling()` tests demonstrate these capabilities in action."
#                 )
#             }
#         ]
#     },
#     # --- Framework Design Patterns ---
#     "9. Page Object Model (POM)": {
#         "files": [
#             {
#                 "path": "pages/home_page.py",
#                 "description": (
#                     "CONCEPT: POM is a design pattern that creates an object repository for web UI elements. The advantages are reduced code duplication and improved maintenance. Each page of the application has a corresponding Page Class.\n\n"
#                     "PROJECT IMPLEMENTATION:\n"
#                     "This file is a perfect example of a Page Class. It contains two main sections:\n"
#                     "1. Locators: All `By` locators for the home page elements are defined as class variables.\n"
#                     "2. Methods: Public methods like `select_category()`, `click_product()`, and `login()` represent the services that the page offers. Test scripts call these methods instead of directly interacting with Selenium, abstracting away the implementation details."
#                 )
#             }
#         ]
#     },
#     "10. Page Factory Pattern": {
#         "files": [
#             {
#                 "path": "utilities/page_factory.py",
#                 "description": (
#                     "CONCEPT: Page Factory is a way to automatically initialize the elements of a Page Object. Instead of writing `driver.find_element` for each element, you annotate a field with a locator, and the framework finds it for you when you access it.\n\n"
#                     "PROJECT IMPLEMENTATION:\n"
#                     "This file contains a custom implementation of the Page Factory pattern. The `@find_by` decorator is used to associate a locator with a method. When the method is called, the decorator's logic intercepts the call, finds the element on the page, caches it for performance, and returns it."
#                 )
#             },
#             {
#                 "path": "pages/home_page_factory.py",
#                 "description": (
#                     "This is an example of a Page Class built using our custom Page Factory. Notice how elements like `logo` and `cart_menu` are defined as methods decorated with `@find_by`. The business logic methods (`login`, `signup`) then use these decorated methods to get the elements they need to interact with."
#                 )
#             }
#         ]
#     },
#     "11. Data-Driven Framework": {
#         "files": [
#             {
#                 "path": "utilities/excel_utils.py",
#                 "description": (
#                     "CONCEPT: A Data-Driven Framework separates test data from test scripts. This allows the same test script to be run with multiple sets of data from an external source, such as an Excel, CSV, or JSON file.\n\n"
#                     "PROJECT IMPLEMENTATION:\n"
#                     "This project has a robust data-driven capability. The `utilities` package contains parsers for multiple file types (`excel_utils.py`, `csv_utils.py`, `json_utils.py`, `xml_utils.py`)."
#                 )
#             },
#             {
#                 "path": "tests/test_demoblaze_e2e.py",
#                 "description": (
#                     "The tests from `test_10` to `test_13` are true data-driven tests. For example, `test_10_data_driven_excel` calls `self.excel_utils.read_excel_data()` to load product data from `data/test_data.xlsx`. It then iterates through each product in a loop, performing the same UI validation steps for each one. This demonstrates the core principle of separating data from logic."
#                 )
#             }
#         ]
#     },
#     "12. Keyword-Driven Framework": {
#         "files": [
#             {
#                 "path": "utilities/keyword_engine.py",
#                 "description": (
#                     "CONCEPT: A Keyword-Driven Framework is an advanced form of data-driven testing where not just the data, but the test steps themselves are stored in an external file. An 'Engine' reads this file and translates the keywords into Selenium actions.\n\n"
#                     "PROJECT IMPLEMENTATION:\n"
#                     "The `KeywordEngine` class is the heart of this framework. Its `execute_test_case` method reads the `keyword_test_cases.xlsx` file using pandas. It then loops through each row, feeding the 'Action', 'Locator', and 'Value' to the `execute_keyword` method. This method acts as a large dispatcher, mapping a keyword string like 'click' or 'input_text' to the corresponding Selenium function call."
#                 )
#             },
#             {
#                 "path": "tests/test_keyword_driven.py",
#                 "description": (
#                     "This file acts as the 'runner' for the keyword-driven test. Its only job is to set up the driver, create an instance of the `KeywordEngine`, and command it to execute the test defined in the Excel file. This demonstrates a complete separation of the test execution logic from the test case definition."
#                 )
#             }
#         ]
#     },
#     # --- Advanced Topics & Reporting ---
#     "13. Selenium Grid & Parallel Execution": {
#         "files": [
#             {
#                 "path": "run_grid_test.py",
#                 "description": (
#                     "CONCEPT: Selenium Grid allows you to run your tests on remote machines and in parallel across different browsers. It uses a Hub-Node architecture. The Hub receives test requests, and the Nodes execute them on actual browsers.\n\n"
#                     "PROJECT IMPLEMENTATION:\n"
#                     "This standalone script was created to safely demonstrate Grid functionality. It uses Python's `threading` module to create two separate threads: one for Chrome and one for Edge. Both threads connect to the Grid Hub's URL (`http://localhost:4444`) using `webdriver.Remote(...)` instead of a local `webdriver.Chrome()`. By starting both threads simultaneously, it executes a login test on both browsers in parallel, significantly reducing total execution time."
#                 )
#             }
#         ]
#     },
#     "14. Reporting (Allure & HTML)": {
#         "files": [
#             {
#                 "path": "tests/test_demoblaze_e2e.py",
#                 "description": (
#                     "CONCEPT: Allure is a powerful, flexible test reporting tool that creates interactive web reports with rich details, including steps, attachments (like screenshots), timings, and history.\n\n"
#                     "PROJECT IMPLEMENTATION:\n"
#                     "The test methods in this file are decorated with `@allure.feature(...)` and `@allure.story(...)`. These decorators organize the tests into a logical structure within the Allure report. The `conftest.py` file also contains a hook that automatically attaches a screenshot to the Allure report whenever a test fails."
#                 )
#             },
#             {
#                 "path": "pytest.ini",
#                 "description": (
#                     "This configuration file tells Pytest to automatically generate both a simple `pytest-html` report (`--html=reports/test-report.html`) and the raw data files for Allure (`--alluredir=reports/allure-results`) on every run."
#                 )
#             }
#         ]
#     }
# }
#
#
# def find_project_root():
#     """
#     Find the project root directory by looking for pytest.ini or other markers.
#     Returns the absolute path to the project root.
#     """
#     # Start from the script's directory
#     current_dir = os.path.dirname(os.path.abspath(__file__))
#
#     # Marker files that indicate project root
#     markers = ['pytest.ini', 'config.ini', 'requirements.txt', 'setup.py', '.git']
#
#     # Check current directory and up to 3 parent directories
#     for _ in range(4):
#         # Check if any marker exists in current directory
#         for marker in markers:
#             if os.path.exists(os.path.join(current_dir, marker)):
#                 return current_dir
#
#         # Move up one directory
#         parent = os.path.dirname(current_dir)
#         if parent == current_dir:  # Reached root of filesystem
#             break
#         current_dir = parent
#
#     # If no markers found, return script directory
#     return os.path.dirname(os.path.abspath(__file__))
#
#
# def main():
#     """Main function to run the interactive topic locator."""
#
#     # Find and set the project root
#     project_root = find_project_root()
#     os.chdir(project_root)
#
#     print("=" * 100)
#     print("🔍 SELENIUM AUTOMATION TOPIC LOCATOR")
#     print("   This script provides a detailed breakdown of where each automation concept is implemented.")
#     print("=" * 100)
#     print(f"\n📂 Project Root: {project_root}")
#     print(f"📂 Current Working Directory: {os.getcwd()}\n")
#
#     topic_list = list(TOPICS.keys())
#     for i, topic_name in enumerate(topic_list, 1):
#         print(f"   {i:2}. {topic_name.split('. ')[1]}")
#
#     print("\n" + "-" * 100)
#     print("Enter a topic number (e.g., '2' for Pytest Framework) to see its detailed implementation.")
#     print("Enter 'all' to display details for every topic.")
#     print("Enter 'q' to quit.")
#     print("-" * 100)
#
#     while True:
#         choice = input("> ").strip().lower()
#         if choice == 'q':
#             print("Goodbye!")
#             break
#         if choice == 'all':
#             for topic_name in topic_list:
#                 print_topic_details(topic_name, TOPICS[topic_name]["files"])
#             print("\nDisplayed all topics. Enter another number, 'all', or 'q'.")
#             continue
#
#         if not choice.isdigit():
#             print("❌ Invalid input. Please enter a number, 'all', or 'q'.")
#             continue
#
#         try:
#             idx = int(choice)
#             if 1 <= idx <= len(topic_list):
#                 topic_name = topic_list[idx - 1]
#                 print_topic_details(topic_name, TOPICS[topic_name]["files"])
#                 print(f"\nDisplayed details for '{topic_name.split('. ')[1]}'. Enter another number, 'all', or 'q'.")
#             else:
#                 print(f"❌ Number out of range. Please enter a number between 1 and {len(topic_list)}.")
#         except (ValueError, IndexError):
#             print("❌ Invalid number. Please try again.")
#
#
# if __name__ == "__main__":
#     main()

import os
import sys

# =================================================================================
#  Comprehensive Topic Mapping for Selenium DemoBlaze Automation Framework
#  This script provides detailed explanations of each automation concept and maps
#  it directly to its implementation within this project's codebase.
# =================================================================================


# --- Helper function for colored output and file checking ---
def print_topic_details(topic_name, files_info):
    """Prints topic details with colored output and file existence check."""
    # ANSI color codes for better readability
    COLOR = {
        "HEADER": "\033[95m", "BLUE": "\033[94m", "GREEN": "\033[92m",
        "YELLOW": "\033[93m", "RED": "\033[91m", "ENDC": "\033[0m",
        "BOLD": "\033[1m", "UNDERLINE": "\033[4m"
    }
    print("\n" + "=" * 100)
    print(f"{COLOR['HEADER']}{COLOR['BOLD']}📘 TOPIC: {topic_name}{COLOR['ENDC']}")
    print("=" * 100)
    for file_info in files_info:
        path = file_info['path']
        description = file_info['description']
        exists = os.path.exists(path)
        status_color = COLOR['GREEN'] if exists else COLOR['RED']
        status_text = "✅ File Exists" if exists else "❌ File NOT Found"

        print(f"\n{COLOR['BLUE']}📁 Reference File: {COLOR['BOLD']}{path}{COLOR['ENDC']}  ({status_color}{status_text}{COLOR['ENDC']})")
        print(f"\n{COLOR['YELLOW']}💡 Description & Implementation Details:{COLOR['ENDC']}\n{description}")
    print("\n" + "=" * 100)


# =================================================================================
#                             REFINED TOPIC MAPPING
# =================================================================================

TOPICS = {
    # --- Framework Fundamentals ---
    "1. Hybrid Framework Architecture": {
        "files": [
            {
                "path": "README.md",
                "description": (
                    "CONCEPT: A Hybrid Framework combines the strengths of multiple framework types to create a more robust, flexible, and scalable solution.\n\n"
                    "PROJECT IMPLEMENTATION:\n"
                    "This project is a classic Hybrid Framework that integrates:\n"
                    "1. Page Object Model (POM): For separating UI elements and interactions from test logic (see Topic 25).\n"
                    "2. Data-Driven Framework: For running the same test logic with multiple datasets from external files (see Topic 27).\n"
                    "3. Keyword-Driven Framework: For abstracting complex actions into simple keywords, allowing test creation in a data table (see Topic 28).\n"
                    "4. Modular Framework: The project is broken down into logical, reusable modules (`config`, `pages`, `utilities`, `tests`)."
                )
            }
        ]
    },
    "2. Pytest Framework (Fixtures & Markers)": {
        "files": [
            {
                "path": "tests/test_demoblaze_e2e.py",
                "description": (
                    "CONCEPT: A fixture is a function that runs before (and optionally after) a test function. It's used for setup and teardown, such as creating a browser session, logging in a user, or loading test data.\n\n"
                    "PROJECT IMPLEMENTATION:\n"
                    "The `@pytest.fixture(autouse=True)` in `setup_and_teardown` is the heart of every test class. For each test function, this fixture automatically:\n"
                    "  - BEFORE THE TEST (`yield`): Initializes a logger, creates a fresh browser instance using `BrowserConfig`, instantiates all Page Objects (`HomePage`, `ProductPage`, etc.), and navigates to the base URL.\n"
                    "  - AFTER THE TEST (after `yield`): Logs completion and calls `driver.quit()` to cleanly close the browser and end the session. This ensures every test runs in isolation."
                )
            },
            {
                "path": "C:\\Users\\Ascendion\\PycharmProjects\\PythonProject1\\pytest.ini",
                "description": (
                    "CONCEPT: Markers are custom tags used to group tests (e.g., 'smoke', 'regression'). You can then choose to run only a specific group of tests.\n\n"
                    "PROJECT IMPLEMENTATION:\n"
                    "This file defines custom markers like `smoke` and `regression`. A test can be marked with `@pytest.mark.smoke` to be included in the smoke test suite. You can run only these tests using the command: `pytest -m smoke`."
                )
            }
        ]
    },
    # --- Core Selenium Interactions ---
    "3. Browser Launching & Configuration": {
        "files": [
            {
                "path": "config/browser_config.py",
                "description": (
                    "CONCEPT: WebDriver configuration involves setting up the browser driver (e.g., chromedriver) and applying specific options like headless mode, window size, or performance flags.\n\n"
                    "PROJECT IMPLEMENTATION:\n"
                    "The `get_driver()` method is the central factory for creating WebDriver instances. It reads the `config.ini` file to determine which browser to launch (`chrome`, `edge`, `firefox`).\n"
                    "  - It calls browser-specific methods like `get_chrome_options()` to apply all configurations (headless, window size, disabling GPU, etc.).\n"
                    "  - It uses `webdriver-manager` to automatically download and manage the correct driver executables, avoiding manual setup."
                )
            }
        ]
    },
    "4. Locators & WebElement Interaction": {
        "files": [
            {
                "path": "pages/home_page.py",
                "description": (
                    "CONCEPT: Locators are strategies used to find elements on a web page (e.g., By.ID, By.XPATH). Once an element is found, you can interact with it using methods like `.click()`, `.send_keys()`, or retrieve its properties like `.text`.\n\n"
                    "PROJECT IMPLEMENTATION:\n"
                    "  - LOCATORS: This file defines all locators as constant tuples at the top of the class, e.g., `LOGO = (By.ID, 'nava')`. This makes them easy to manage and reuse.\n"
                    "  - INTERACTIONS: Methods like `login(username, password)` use these locators to perform actions: `self.send_keys(self.LOGIN_USERNAME, username)`."
                )
            },
            {
                "path": "pages/base_page.py",
                "description": (
                    "CONCEPT: To improve reliability and reusability, it's best to create wrapper methods for common Selenium interactions.\n\n"
                    "PROJECT IMPLEMENTATION:\n"
                    "This base class contains robust wrapper methods for all standard interactions. For example, the `click()` method first waits for the element to be clickable (`EC.element_to_be_clickable`). If a standard click fails (e.g., the element is obscured), it has a fallback mechanism to perform a click using JavaScript (`driver.execute_script`). This makes the tests much more stable."
                )
            }
        ]
    },
    # --- Advanced Interactions & Topics ---
    "5. Waits (Implicit & Explicit)": {
        "files": [
            {
                "path": "config/browser_config.py",
                "description": (
                    "CONCEPT: An implicit wait tells WebDriver to poll the DOM for a certain amount of time when trying to find an element if it's not immediately available. It is set once per session.\n\n"
                    "PROJECT IMPLEMENTATION:\n"
                    "At the end of the `get_driver()` method, `driver.implicitly_wait(...)` is called. The wait time is loaded from `config.ini`, making it easy to configure."
                )
            },
            {
                "path": "pages/base_page.py",
                "description": (
                    "CONCEPT: An explicit wait is a code you define to wait for a certain condition to occur before proceeding further in the code. It is more precise and reliable than an implicit wait.\n\n"
                    "PROJECT IMPLEMENTATION:\n"
                    "This framework relies heavily on explicit waits for maximum stability. A `WebDriverWait` instance is initialized in the `__init__` method. Every interaction method, like `find_element()`, `click()`, etc., uses this wait with an Expected Condition (`EC`), such as `EC.presence_of_element_located` or `EC.element_to_be_clickable`. This ensures the script only proceeds when the app is ready."
                )
            }
        ]
    },
    "6. Handling Dropdowns, Checkboxes & Radio Buttons": {
        "files": [
            {
                "path": "tests/test_dropdowns.py",
                "description": (
                    "CONCEPT: Standard dropdowns (`<select>` tags) are handled using Selenium's `Select` class. This provides easy methods to select options by their text, value, or index.\n\n"
                    "PROJECT IMPLEMENTATION:\n"
                    "Since the DemoBlaze site has no dropdowns, this dedicated test file was created. It starts a local web server with a custom HTML page containing a dropdown. The test then calls the methods from `base_page.py` (`select_dropdown_by_value`, `select_dropdown_by_text`, etc.) to interact with the dropdown and verifies the selection was successful. This proves the framework's capability."
                )
            },
            {
                "path": "tests/test_checkboxes.py",
                "description": (
                    "CONCEPT: Checkboxes are input elements that can be checked for their selection state using the `.is_selected()` method.\n\n"
                    "PROJECT IMPLEMENTATION:\n"
                    "Similar to the dropdowns test, this file creates a local HTML page with checkboxes to provide a reliable test environment. It uses the `base_page.click()` method to toggle the checkboxes and `base_page.is_selected()` to assert their initial and final states."
                )
            }
        ]
    },
    "7. Mouse Actions (ActionChains)": {
        "files": [
            {
                "path": "pages/base_page.py",
                "description": (
                    "CONCEPT: The `ActionChains` class is used to automate complex user interactions like hovering, right-clicking, double-clicking, and dragging-and-dropping.\n\n"
                    "PROJECT IMPLEMENTATION:\n"
                    "This file provides wrapper methods for these actions: `hover()`, `right_click()`, `double_click()`, and `drag_and_drop()`. Each method creates an `ActionChains` instance, chains the desired action, and calls `.perform()` to execute it."
                )
            },
            {
                "path": "tests/test_demoblaze_e2e.py",
                "description": (
                    "The `test_02_mouse_operations()` test specifically validates these actions by hovering over menu items, right-clicking the logo, and double-clicking a product to navigate to its page."
                )
            }
        ]
    },
    "8. Alert, Frame, and Window Handling": {
        "files": [
            {
                "path": "pages/base_page.py",
                "description": (
                    "CONCEPT: Selenium provides methods to switch the driver's focus between different contexts like browser windows/tabs, iframes, and JavaScript alerts.\n\n"
                    "PROJECT IMPLEMENTATION:\n"
                    "This file contains dedicated methods for each context:\n"
                    "  - ALERTS: `accept_alert()`, `dismiss_alert()`, and `send_keys_to_alert()` wait for an alert to be present and then interact with it.\n"
                    "  - WINDOWS: `switch_to_window()`, `get_all_window_handles()` allow the test to move between different browser tabs.\n"
                    "  - FRAMES: `switch_to_frame()` and `switch_to_default_content()` are provided for handling iframes."
                )
            },
            {
                "path": "tests/test_demoblaze_e2e.py",
                "description": (
                    "The `test_01_browser_windows_and_tabs()` and `test_05_alerts_handling()` tests demonstrate these capabilities in action."
                )
            }
        ]
    },
    # --- Framework Design Patterns ---
    "9. Page Object Model (POM)": {
        "files": [
            {
                "path": "pages/home_page.py",
                "description": (
                    "CONCEPT: POM is a design pattern that creates an object repository for web UI elements. The advantages are reduced code duplication and improved maintenance. Each page of the application has a corresponding Page Class.\n\n"
                    "PROJECT IMPLEMENTATION:\n"
                    "This file is a perfect example of a Page Class. It contains two main sections:\n"
                    "1. Locators: All `By` locators for the home page elements are defined as class variables.\n"
                    "2. Methods: Public methods like `select_category()`, `click_product()`, and `login()` represent the services that the page offers. Test scripts call these methods instead of directly interacting with Selenium, abstracting away the implementation details."
                )
            }
        ]
    },
    "10. Page Factory Pattern": {
        "files": [
            {
                "path": "utilities/page_factory.py",
                "description": (
                    "CONCEPT: Page Factory is a way to automatically initialize the elements of a Page Object. Instead of writing `driver.find_element` for each element, you annotate a field with a locator, and the framework finds it for you when you access it.\n\n"
                    "PROJECT IMPLEMENTATION:\n"
                    "This file contains a custom implementation of the Page Factory pattern. The `@find_by` decorator is used to associate a locator with a method. When the method is called, the decorator's logic intercepts the call, finds the element on the page, caches it for performance, and returns it."
                )
            },
            {
                "path": "pages/home_page_factory.py",
                "description": (
                    "This is an example of a Page Class built using our custom Page Factory. Notice how elements like `logo` and `cart_menu` are defined as methods decorated with `@find_by`. The business logic methods (`login`, `signup`) then use these decorated methods to get the elements they need to interact with."
                )
            }
        ]
    },
    "11. Data-Driven Framework": {
        "files": [
            {
                "path": "utilities/excel_utils.py",
                "description": (
                    "CONCEPT: A Data-Driven Framework separates test data from test scripts. This allows the same test script to be run with multiple sets of data from an external source, such as an Excel, CSV, or JSON file.\n\n"
                    "PROJECT IMPLEMENTATION:\n"
                    "This project has a robust data-driven capability. The `utilities` package contains parsers for multiple file types (`excel_utils.py`, `csv_utils.py`, `json_utils.py`, `xml_utils.py`)."
                )
            },
            {
                "path": "tests/test_demoblaze_e2e.py",
                "description": (
                    "The tests from `test_10` to `test_13` are true data-driven tests. For example, `test_10_data_driven_excel` calls `self.excel_utils.read_excel_data()` to load product data from `data/test_data.xlsx`. It then iterates through each product in a loop, performing the same UI validation steps for each one. This demonstrates the core principle of separating data from logic."
                )
            }
        ]
    },
    "12. Keyword-Driven Framework": {
        "files": [
            {
                "path": "utilities/keyword_engine.py",
                "description": (
                    "CONCEPT: A Keyword-Driven Framework is an advanced form of data-driven testing where not just the data, but the test steps themselves are stored in an external file. An 'Engine' reads this file and translates the keywords into Selenium actions.\n\n"
                    "PROJECT IMPLEMENTATION:\n"
                    "The `KeywordEngine` class is the heart of this framework. Its `execute_test_case` method reads the `keyword_test_cases.xlsx` file using pandas. It then loops through each row, feeding the 'Action', 'Locator', and 'Value' to the `execute_keyword` method. This method acts as a large dispatcher, mapping a keyword string like 'click' or 'input_text' to the corresponding Selenium function call."
                )
            },
            {
                "path": "tests/test_keyword_driven.py",
                "description": (
                    "This file acts as the 'runner' for the keyword-driven test. Its only job is to set up the driver, create an instance of the `KeywordEngine`, and command it to execute the test defined in the Excel file. This demonstrates a complete separation of the test execution logic from the test case definition."
                )
            }
        ]
    },
    # --- Advanced Topics & Reporting ---
    "13. Selenium Grid & Parallel Execution": {
        "files": [
            {
                "path": "C:\\Users\\Ascendion\\PycharmProjects\\PythonProject1\\run_grid_test.py",
                "description": (
                    "CONCEPT: Selenium Grid allows you to run your tests on remote machines and in parallel across different browsers. It uses a Hub-Node architecture. The Hub receives test requests, and the Nodes execute them on actual browsers.\n\n"
                    "PROJECT IMPLEMENTATION:\n"
                    "This standalone script was created to safely demonstrate Grid functionality. It uses Python's `threading` module to create two separate threads: one for Chrome and one for Edge. Both threads connect to the Grid Hub's URL (`http://localhost:4444`) using `webdriver.Remote(...)` instead of a local `webdriver.Chrome()`. By starting both threads simultaneously, it executes a login test on both browsers in parallel, significantly reducing total execution time."
                )
            }
        ]
    },
    "14. Reporting (Allure & HTML)": {
        "files": [
            {
                "path": "tests/test_demoblaze_e2e.py",
                "description": (
                    "CONCEPT: Allure is a powerful, flexible test reporting tool that creates interactive web reports with rich details, including steps, attachments (like screenshots), timings, and history.\n\n"
                    "PROJECT IMPLEMENTATION:\n"
                    "The test methods in this file are decorated with `@allure.feature(...)` and `@allure.story(...)`. These decorators organize the tests into a logical structure within the Allure report. The `conftest.py` file also contains a hook that automatically attaches a screenshot to the Allure report whenever a test fails."
                )
            },
            {
                "path": "C:\\Users\\Ascendion\\PycharmProjects\\PythonProject1\\pytest.ini",
                "description": (
                    "This configuration file tells Pytest to automatically generate both a simple `pytest-html` report (`--html=reports/test-report.html`) and the raw data files for Allure (`--alluredir=reports/allure-results`) on every run."
                )
            }
        ]
    }
}


def main():
    """Main function to run the interactive topic locator."""
    print("=" * 100)
    print("🔍 SELENIUM AUTOMATION TOPIC LOCATOR")
    print("   This script provides a detailed breakdown of where each automation concept is implemented.")
    print("=" * 100)

    topic_list = list(TOPICS.keys())
    for i, topic_name in enumerate(topic_list, 1):
        print(f"   {i:2}. {topic_name.split('. ')[1]}")

    print("\n" + "-" * 100)
    print("Enter a topic number (e.g., '9' for POM) to see its detailed implementation.")
    print("Enter 'all' to display details for every topic.")
    print("Enter 'q' to quit.")
    print("-" * 100)

    while True:
        choice = input("> ").strip().lower()
        if choice == 'q':
            print("Goodbye!")
            break
        if choice == 'all':
            for topic_name in topic_list:
                print_topic_details(topic_name, TOPICS[topic_name]["files"])
            print("\nDisplayed all topics. Enter another number, 'all', or 'q'.")
            continue

        if not choice.isdigit():
            print("❌ Invalid input. Please enter a number, 'all', or 'q'.")
            continue

        try:
            idx = int(choice)
            if 1 <= idx <= len(topic_list):
                topic_name = topic_list[idx - 1]
                print_topic_details(topic_name, TOPICS[topic_name]["files"])
                print(f"\nDisplayed details for '{topic_name.split('. ')[1]}'. Enter another number, 'all', or 'q'.")
            else:
                print(f"❌ Number out of range. Please enter a number between 1 and {len(topic_list)}.")
        except (ValueError, IndexError):
            print("❌ Invalid number. Please try again.")


if __name__ == "__main__":
    # Ensure the script can find the project files by setting the CWD to the project root
    project_root = os.path.dirname(os.path.abspath(__file__))
    os.chdir(project_root)
    # This check is just for the script's own file discovery logic
    if not os.path.isdir("selenium_demoblaze_framework"):
        # If the script is run from a different CWD, try to go up one level
        parent_dir = os.path.dirname(project_root)
        if os.path.isdir(os.path.join(parent_dir, "selenium_demoblaze_framework")):
            os.chdir(parent_dir)
    main()