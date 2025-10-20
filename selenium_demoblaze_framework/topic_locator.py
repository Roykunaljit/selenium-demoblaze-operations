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

import os
import sys


# =================================================================================
#  Comprehensive Topic Mapping for Selenium DemoBlaze Automation Framework
#  This script maps every concept from the syllabus to its implementation
#  in the codebase, providing file paths and specific locations.
# =================================================================================

# --- Helper function for colored output and file checking ---
def print_topic_details(topic_name, files_info):
    """Prints topic details with colored output and file existence check."""
    # ANSI color codes
    COLOR = {
        "HEADER": "\033[95m",
        "BLUE": "\033[94m",
        "GREEN": "\033[92m",
        "YELLOW": "\033[93m",
        "RED": "\033[91m",
        "ENDC": "\033[0m",
        "BOLD": "\033[1m",
        "UNDERLINE": "\033[4m"
    }
    print("\n" + "=" * 80)
    print(f"{COLOR['HEADER']}{COLOR['BOLD']}📘 TOPIC: {topic_name}{COLOR['ENDC']}")
    print("=" * 80)
    for file_info in files_info:
        path = file_info['path']
        location = file_info['lines']
        exists = os.path.exists(path)
        status_color = COLOR['GREEN'] if exists else COLOR['RED']
        status_text = "✅ File Exists" if exists else "❌ File NOT Found"

        print(f"\n{COLOR['BLUE']}📁 File: {COLOR['BOLD']}{path}{COLOR['ENDC']}")
        print(f"   {COLOR['YELLOW']}📍 Location:{COLOR['ENDC']} {location}")
        print(f"   {status_color}{status_text}{COLOR['ENDC']}")
    print("\n" + "=" * 80)


# ==============================
# REFINED TOPIC MAPPING
# ==============================

TOPICS = {
    "1. Introduction & Core Python Concepts": {
        "files": [
            {"path": "README.md", "lines": "Project overview demonstrating automation principles."},
            {"path": "tests/test_demoblaze_e2e.py",
             "lines": "Demonstrates practical use of OOPS (classes), loops, conditions, and collections."}
        ]
    },
    "2. Browser Launching (Chrome/Firefox/Edge)": {
        "files": [
            {"path": "config/browser_config.py",
             "lines": "Method `get_driver()` handles multi-browser setup and configuration."},
            {"path": "config/config.ini", "lines": "Browser type and options are configured here."}
        ]
    },
    "3. WebDriver Methods (get, title, url, etc.)": {
        "files": [
            {"path": "pages/base_page.py",
             "lines": "Methods like `get_current_url()`, `get_title()`, `refresh_page()`, `go_back()`, `go_forward()`."}
        ]
    },
    "4. Navigation Commands": {
        "files": [
            {"path": "pages/base_page.py", "lines": "Methods `go_back()` and `go_forward()`."},
            {"path": "tests/test_demoblaze_e2e.py",
             "lines": "Test `test_18_browser_navigation()` validates all navigation commands."}
        ]
    },
    "5. Locators (ID, XPath, CSS, Class Name, etc.)": {
        "files": [
            {"path": "pages/home_page.py",
             "lines": "All locators defined as tuples, e.g., `LOGO = (By.ID, 'nava')`, `PHONES_CATEGORY = (By.XPATH, ...)`."},
            {"path": "pages/cart_page.py", "lines": "Examples of various locators for cart elements."}
        ]
    },
    "6. WebElement Methods (click, send_keys, text, is_displayed)": {
        "files": [
            {"path": "pages/base_page.py",
             "lines": "Wrapper methods `click()`, `send_keys()`, `get_text()`, `is_displayed()`, `is_enabled()`, `is_selected()`."}
        ]
    },
    "7. Radio Buttons & Checkboxes": {
        "files": [
            {"path": "tests/test_demoblaze_e2e.py",
             "lines": "Test `test_33_radio_button_demo()` interacts with radio buttons on an external site."},
            {"path": "pages/base_page.py",
             "lines": "Method `is_selected()` is used to check the state of these elements."}
        ]
    },
    "8. Handling Multiple WebElements (find_elements)": {
        "files": [
            {"path": "pages/home_page.py",
             "lines": "Method `get_all_products()` uses `find_elements` to get a list of all product cards."},
            {"path": "pages/cart_page.py",
             "lines": "Method `get_cart_items_count()` uses `find_elements` to count table rows."}
        ]
    },
    "9. Dropdown Handling (Select Class)": {
        "files": [
            {"path": "pages/base_page.py",
             "lines": "Methods `select_dropdown_by_value/text/index` using the `Select` class."},
            {"path": "keywords/keywords.py", "lines": "Keyword `select_dropdown` also demonstrates this capability."}
        ]
    },
    "10. Web Tables": {
        "files": [
            {"path": "pages/cart_page.py",
             "lines": "The cart is a web table. Locator `CART_ITEMS` targets table rows (`//tbody//tr`)."}
        ]
    },
    "11. JavaScript Executor": {
        "files": [
            {"path": "utilities/utility_methods.py",
             "lines": "Methods `execute_javascript()` and `execute_async_javascript()`."},
            {"path": "tests/test_demoblaze_e2e.py",
             "lines": "Test `test_04_javascript_execution()` demonstrates scrolling, highlighting, and async execution."}
        ]
    },
    "12. Scrolling (Up, Down, To Element)": {
        "files": [
            {"path": "utilities/utility_methods.py",
             "lines": "Methods `scroll_to_bottom()`, `scroll_to_top()`, `scroll_to_element()`."},
            {"path": "tests/test_demoblaze_e2e.py",
             "lines": "Test `test_07_scrolling_operations()` validates all scrolling types."}
        ]
    },
    "13. Screenshots (Full Page, Element, On Failure)": {
        "files": [
            {"path": "utilities/utility_methods.py",
             "lines": "Methods `take_screenshot()` and `take_element_screenshot()`."},
            {"path": "tests/conftest.py",
             "lines": "Pytest hook `pytest_runtest_makereport` automatically takes a screenshot on test failure."},
            {"path": "tests/test_demoblaze_e2e.py",
             "lines": "Test `test_08_screenshot_operations()` explicitly tests screenshot features."}
        ]
    },
    "14. Mouse Actions (Hover, Right/Double Click, Drag & Drop)": {
        "files": [
            {"path": "pages/base_page.py",
             "lines": "Methods `hover()`, `right_click()`, `double_click()`, and `drag_and_drop()` using `ActionChains`."},
            {"path": "tests/test_demoblaze_e2e.py",
             "lines": "Test `test_02_mouse_operations()` demonstrates hover, right-click, and double-click."}
        ]
    },
    "15. Window and Tab Handling": {
        "files": [
            {"path": "pages/base_page.py",
             "lines": "Methods `switch_to_window()`, `get_current_window_handle()`, `get_all_window_handles()`."},
            {"path": "tests/test_demoblaze_e2e.py",
             "lines": "Test `test_01_browser_windows_and_tabs()` provides a full demonstration."}
        ]
    },
    "16. Frame Handling": {
        "files": [
            {"path": "pages/base_page.py",
             "lines": "Methods `switch_to_frame()` and `switch_to_default_content()` provide the capability."}
        ]
    },
    "17. Alert Handling": {
        "files": [
            {"path": "pages/base_page.py",
             "lines": "Methods `accept_alert()`, `dismiss_alert()`, and `send_keys_to_alert()`."},
            {"path": "tests/test_demoblaze_e2e.py",
             "lines": "Test `test_05_alerts_handling()` validates alert interactions."}
        ]
    },
    "18. Waits (Implicit & Explicit)": {
        "files": [
            {"path": "config/browser_config.py",
             "lines": "Implicit wait is set globally in the `get_driver()` method."},
            {"path": "pages/base_page.py",
             "lines": "`WebDriverWait` (explicit wait) is used as the primary wait strategy for all element interactions."},
            {"path": "tests/test_demoblaze_e2e.py",
             "lines": "Test `test_09_wait_strategies()` demonstrates various explicit wait conditions."}
        ]
    },
    "19. File Uploading (send_keys & pyautogui)": {
        "files": [
            {"path": "utilities/file_upload_utils.py",
             "lines": "Contains multiple upload methods like `upload_file_using_send_keys()`."},
            {"path": "tests/test_demoblaze_e2e.py",
             "lines": "Test `test_31_file_upload()` demonstrates uploading via `send_keys` on a live site."}
        ]
    },
    "20. Broken Link Checking": {
        "files": [
            {"path": "utilities/utility_methods.py",
             "lines": "Method `check_broken_links()` uses the `requests` library to validate links."},
            {"path": "tests/test_demoblaze_e2e.py",
             "lines": "Test `test_32_broken_links_check()` executes the link checker."}
        ]
    },
    "21. Pytest Framework (Fixtures, Parametrize)": {
        "files": [
            {"path": "tests/conftest.py", "lines": "Project-wide fixtures and hooks."},
            {"path": "tests/test_demoblaze_e2e.py",
             "lines": "Use of `@pytest.fixture` for setup and `@pytest.mark.parametrize` for data-driven tests."}
        ]
    },
    "22. Assertions & Validations": {
        "files": [
            {"path": "tests/test_demoblaze_e2e.py",
             "lines": "Every test uses `assert` statements to validate outcomes, e.g., `assert self.home_page.is_user_logged_in()`."}
        ]
    },
    "23. Negative Testing": {
        "files": [
            {"path": "tests/test_demoblaze_e2e.py",
             "lines": "Tests `test_21_invalid_login()` and `test_22_duplicate_signup()` check for expected error messages."}
        ]
    },
    "24. Page Object Model (POM)": {
        "files": [
            {"path": "pages/base_page.py", "lines": "The base class for all page objects, promoting reusability."},
            {"path": "pages/home_page.py",
             "lines": "A complete Page Object class for the home page, encapsulating locators and methods."}
        ]
    },
    "25. Page Factory Pattern": {
        "files": [
            {"path": "utilities/page_factory.py",
             "lines": "Custom implementation of the Page Factory pattern using decorators."},
            {"path": "pages/home_page_factory.py",
             "lines": "Example page class (`HomePageFactory`) using the `@find_by` decorator."},
            {"path": "tests/test_page_factory.py",
             "lines": "Dedicated tests to validate the Page Factory implementation."}
        ]
    },
    "26. Data-Driven Framework (Excel, CSV, JSON, XML)": {
        "files": [
            {"path": "utilities/excel_utils.py", "lines": "Utility for reading from and writing to Excel files."},
            {"path": "utilities/csv_utils.py", "lines": "Utility for handling CSV files."},
            {"path": "tests/test_demoblaze_e2e.py",
             "lines": "Tests `test_10_...` through `test_13_...` demonstrate reading data from all file types."}
        ]
    },
    "27. Keyword-Driven Framework": {
        "files": [
            {"path": "utilities/keyword_engine.py",
             "lines": "The core engine that reads keywords from Excel and executes Selenium commands."},
            {"path": "tests/test_keyword_driven.py", "lines": "Pytest test that runs the keyword engine."},
            {"path": "data/keyword_test_cases.xlsx",
             "lines": "The external Excel sheet containing test steps and data."}
        ]
    },
    "28. Modular-Driven Framework": {
        "files": [
            {"path": "project_structure.txt",
             "lines": "The project is structured into independent modules: `config`, `pages`, `tests`, `utilities`."},
            {"path": "utilities/custom_logger.py", "lines": "An example of a reusable, independent utility module."}
        ]
    },
    "29. Hybrid Framework": {
        "files": [
            {"path": "README.md",
             "lines": "The framework is a Hybrid model, combining POM, Data-Driven, and Keyword-Driven approaches for maximum flexibility."}
        ]
    },
    "30. Reporting (HTML & Allure)": {
        "files": [
            {"path": ".github/workflows/run-tests.yml",
             "lines": "Commands to generate both `pytest-html` and `Allure` reports during CI/CD."},
            {"path": "tests/test_demoblaze_e2e.py",
             "lines": "Use of `@allure.feature` and `@allure.story` decorators to structure Allure reports."}
        ]
    },
    "31. CI/CD Integration (GitHub Actions)": {
        "files": [
            {"path": ".github/workflows/run-tests.yml",
             "lines": "Complete workflow for automated testing on push/pull_request, including setup, execution, and report deployment."}
        ]
    },
    "32. Selenium Grid / Cloud Testing": {
        "files": [
            {"path": "README.md",
             "lines": "These are advanced topics not covered in the current implementation. The framework is, however, ready for Grid integration by modifying `browser_config.py` to use `webdriver.Remote`."}
        ]
    }
}


def main():
    """Main function to run the interactive topic locator."""
    print("=" * 80)
    print("🔍 SELENIUM AUTOMATION TOPIC LOCATOR")
    print("   Shows exactly where each topic is implemented in your codebase")
    print("=" * 80)

    # Display topics
    topic_list = list(TOPICS.keys())
    for topic in topic_list:
        print(f"   {topic}")

    print("\n" + "-" * 80)
    print("Enter topic number (e.g., '5') to see implementation details.")
    print("Enter 'all' to display details for every topic.")
    print("Enter 'q' to quit.")
    print("-" * 80)

    while True:
        choice = input("> ").strip().lower()
        if choice == 'q':
            print("Goodbye!")
            break
        if choice == 'all':
            for topic_name in topic_list:
                info = TOPICS[topic_name]
                print_topic_details(topic_name, info["files"])
            continue

        if not choice.isdigit():
            print("❌ Please enter a valid number, 'all', or 'q'")
            continue

        idx = int(choice)
        if not 1 <= idx <= len(topic_list):
            print(f"❌ Please enter a number between 1 and {len(topic_list)}")
            continue

        topic_name = topic_list[idx - 1]
        info = TOPICS[topic_name]
        print_topic_details(topic_name, info["files"])


if __name__ == "__main__":
    # Add project root to path to ensure file checks work from any directory
    project_root = os.path.dirname(os.path.abspath(__file__))
    os.chdir(project_root)
    sys.path.insert(0, project_root)
    main()