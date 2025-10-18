import os

# ==============================
# TOPIC MAPPING
# Format: "Topic Name": {
#     "files": [{"path": "file.py", "lines": "approx line range or key lines"}]
# }
# ==============================

TOPICS = {
    "Browser Launching (Chrome/Firefox/Edge)": {
        "files": [
            {"path": "config/browser_config.py", "lines": "get_driver() method, lines ~45-75"},
            {"path": "tests/test_demoblaze_e2e.py", "lines": "setup_and_teardown fixture, line ~50"}
        ]
    },
    "WebDriver Methods (get, title, url, maximize, etc.)": {
        "files": [
            {"path": "pages/base_page.py",
             "lines": "get_current_url(), get_title(), refresh_page(), etc., lines ~200-220"}
        ]
    },
    "Locators (ID, Name, XPath, CSS, etc.)": {
        "files": [
            {"path": "pages/home_page.py", "lines": "All locator tuples like LOGO = (By.ID, 'nava'), lines ~10-50"},
            {"path": "pages/product_page.py", "lines": "PRODUCT_NAME = (By.XPATH, ...), lines ~8-12"}
        ]
    },
    "WebElement Methods (click, send_keys, text, etc.)": {
        "files": [
            {"path": "pages/base_page.py", "lines": "click(), send_keys(), get_text(), lines ~50-100"}
        ]
    },
    "Radio Buttons": {
    "files": [
        {
            "path": "tests/test_demoblaze_e2e.py",
            "lines": "test_33_radio_button_demo() method, lines ~890-920 — demonstrates clicking and verifying radio buttons on https://demoqa.com/radio-button using label click + JS verification"
        },
        {
            "path": "pages/base_page.py",
            "lines": "is_selected() method (line ~140) — supports checking selection state of radio buttons/checkboxes"
        },
        {
            "path": "utilities/utility_methods.py",
            "lines": "execute_javascript() used in test to verify radio button state via 'checked' property"
        }
    ]
},
    "Checkboxes": {
        "files": [
            {"path": "pages/home_page.py",
             "lines": "DAYS_CHECKBOXES dict (if used), or base_page.is_selected() supports it"},
            {"path": "pages/base_page.py", "lines": "is_selected() method, line ~140"}
        ]
    },
    "Dropdown Handling (Select class)": {
        "files": [
            {"path": "pages/base_page.py", "lines": "select_dropdown_by_text/value/index, lines ~150-170"},
            {"path": "keywords/keywords.py", "lines": "select_dropdown() method, lines ~40-60"}
        ]
    },
    "Web Tables": {
        "files": [
            {"path": "pages/home_page.py",
             "lines": "get_all_products() parses product cards as table-like data, lines ~100-120"},
            {"path": "pages/cart_page.py", "lines": "CART_ITEMS XPath, get_cart_items_count(), lines ~20-30"}
        ]
    },
    "JavaScript Executor": {
        "files": [
            {"path": "utilities/utility_methods.py",
             "lines": "execute_javascript(), execute_async_javascript(), lines ~120-130"},
            {"path": "tests/test_demoblaze_e2e.py", "lines": "test_04_javascript_execution(), lines ~280-310"}
        ]
    },
    "Scrolling (pixel, element, top/bottom)": {
        "files": [
            {"path": "utilities/utility_methods.py",
             "lines": "scroll_to_bottom(), scroll_by_pixels(), etc., lines ~90-110"},
            {"path": "tests/test_demoblaze_e2e.py", "lines": "test_07_scrolling_operations(), lines ~400-410"}
        ]
    },
    "Screenshots (full, element, auto on fail)": {
        "files": [
            {"path": "utilities/utility_methods.py",
             "lines": "take_screenshot(), take_element_screenshot(), lines ~40-80"},
            {"path": "tests/test_demoblaze_e2e.py", "lines": "test_08_screenshot_operations(), lines ~415-425"}
        ]
    },
    "Mouse Hover (ActionChains)": {
        "files": [
            {"path": "pages/base_page.py", "lines": "hover() method using ActionChains, line ~75"},
            {"path": "tests/test_demoblaze_e2e.py", "lines": "test_02_mouse_operations(), lines ~240-260"}
        ]
    },
    "Drag & Drop / Right Click / Double Click": {
        "files": [
            {"path": "pages/base_page.py", "lines": "drag_and_drop(), right_click(), double_click(), lines ~65-85"},
            {"path": "tests/test_demoblaze_e2e.py", "lines": "test_02_mouse_operations(), lines ~260-280"}
        ]
    },
    "Window/Tab Handling": {
        "files": [
            {"path": "pages/base_page.py", "lines": "switch_to_window(), get_all_window_handles(), lines ~180-190"},
            {"path": "tests/test_demoblaze_e2e.py", "lines": "test_01_browser_windows_and_tabs(), lines ~220-240"}
        ]
    },
    "Frame Handling": {
        "files": [
            {"path": "pages/base_page.py", "lines": "switch_to_frame(), switch_to_default_content(), lines ~175-180"},
            {"path": "keywords/keywords.py", "lines": "switch_to_frame(), switch_to_default_content(), lines ~120-130"}
        ]
    },
    "Alert Handling (accept/dismiss/send_keys)": {
        "files": [
            {"path": "pages/base_page.py",
             "lines": "accept_alert(), dismiss_alert(), send_keys_to_alert(), lines ~190-210"},
            {"path": "tests/test_demoblaze_e2e.py", "lines": "test_05_alerts_handling(), lines ~320-340"}
        ]
    },
    "Waits (Implicit, Explicit, Custom)": {
        "files": [
            {"path": "config/browser_config.py", "lines": "implicit_wait set in get_driver(), line ~70"},
            {"path": "pages/base_page.py", "lines": "wait_for_element_visible(), custom WebDriverWait, lines ~130-150"},
            {"path": "tests/test_demoblaze_e2e.py", "lines": "test_09_wait_strategies(), lines ~430-450"}
        ]
    },
    "File Upload (send_keys + pyautogui fallback)": {
        "files": [
            {"path": "utilities/file_upload_utils.py",
             "lines": "upload_file_using_send_keys(), upload_file_using_pyautogui(), lines ~20-80"},
            {"path": "tests/test_demoblaze_e2e.py", "lines": "test_31_file_upload(), lines ~950-980"},
            {"path": "tests/test_file_upload.py", "lines": "Full test file for single/multiple upload"}
        ]
    },
    "Broken Link Checker": {
        "files": [
            {"path": "utilities/link_checker_utils.py", "lines": "Full implementation"},
            {"path": "tests/test_demoblaze_e2e.py", "lines": "test_32_broken_links_check(), lines ~985-1000"},
            {"path": "tests/test_link_checker.py", "lines": "Dedicated test file"}
        ]
    },
    "Pytest Framework (Fixtures, Parametrize, Markers)": {
        "files": [
            {"path": "tests/test_demoblaze_e2e.py",
             "lines": "@pytest.fixture, @allure.feature, @pytest.mark.parametrize, lines ~50-100"},
            {"path": "tests/test_base.py", "lines": "class_setup fixture, lines ~10-20"}
        ]
    },
    "Page Object Model (POM)": {
        "files": [
            {"path": "pages/home_page.py", "lines": "Full POM class"},
            {"path": "pages/product_page.py", "lines": "Full POM class"},
            {"path": "pages/cart_page.py", "lines": "Full POM class"}
        ]
    },
    "Page Factory Pattern": {
        "files": [
            {"path": "utilities/page_factory.py", "lines": "FindBy decorator, PageFactory base"},
            {"path": "pages/home_page_factory.py", "lines": "HomePageFactory with @find_by decorators"},
            {"path": "tests/test_page_factory.py", "lines": "Full test coverage"}
        ]
    },
    "Data-Driven Testing (Excel, CSV, JSON, XML)": {
        "files": [
            {"path": "utilities/excel_utils.py", "lines": "Full Excel read/write"},
            {"path": "utilities/csv_utils.py", "lines": "Full CSV support"},
            {"path": "utilities/json_utils.py", "lines": "Full JSON support"},
            {"path": "utilities/xml_utils.py", "lines": "Full XML support"},
            {"path": "tests/test_demoblaze_e2e.py", "lines": "test_10 to test_13, lines ~460-520"}
        ]
    },
    "Keyword-Driven Framework": {
        "files": [
            {"path": "utilities/keyword_engine.py", "lines": "Full engine"},
            {"path": "keywords/keywords.py", "lines": "All keywords"},
            {"path": "tests/test_keyword_driven.py", "lines": "Test execution"},
            {"path": "data/keyword_test_cases.xlsx", "lines": "Test data file"}
        ]
    },
    "Modular Framework": {
        "files": [
            {"path": "pages/", "lines": "Each page is a module"},
            {"path": "utilities/", "lines": "Each utility is a module (logging, upload, etc.)"}
        ]
    },
    "Custom Logger": {
        "files": [
            {"path": "utilities/custom_logger.py", "lines": "Full implementation"},
            {"path": "pages/base_page.py", "lines": "Logger passed to all pages"}
        ]
    },
    "Selenium Grid (Parallel Execution)": {
        "files": [
            {"path": "tests/test_demoblaze_e2e.py", "lines": "Not implemented in main flow"},
            {"path": "[External] grid_parallel.py (from knowledge base)", "lines": "Threading-based parallel demo"}
        ]
    },
    "Network Emulation (Chrome CDP)": {
        "files": [
            {"path": "utilities/utility_methods.py", "lines": "set_network_conditions(), lines ~280-290"},
            {"path": "tests/test_demoblaze_e2e.py", "lines": "test_27_network_emulation(), lines ~880-890"}
        ]
    },
    "Local/Session Storage": {
        "files": [
            {"path": "utilities/utility_methods.py", "lines": "get/set/clear local/session storage, lines ~290-310"},
            {"path": "tests/test_demoblaze_e2e.py", "lines": "test_14_storage_operations(), lines ~530-540"}
        ]
    },
    "Performance Metrics": {
        "files": [
            {"path": "utilities/utility_methods.py", "lines": "get_performance_metrics(), lines ~270-275"},
            {"path": "tests/test_demoblaze_e2e.py", "lines": "test_15_performance_metrics(), lines ~545-555"}
        ]
    },
    "Faker Data Generation": {
        "files": [
            {"path": "utilities/utility_methods.py", "lines": "generate_random_email/name/phone, lines ~230-250"},
            {"path": "tests/test_demoblaze_e2e.py", "lines": "test_19_faker_data_generation(), lines ~600-610"}
        ]
    },
    "End-to-End Shopping Flow": {
        "files": [
            {"path": "tests/test_demoblaze_e2e.py", "lines": "test_20_complete_e2e_flow(), lines ~620-720"}
        ]
    },
    "Allure Reporting": {
        "files": [
            {"path": "tests/test_demoblaze_e2e.py", "lines": "@allure.feature/story decorators, lines ~220-1000"}
        ]
    },
    "HTML Test Reporting": {
        "files": [
            {"path": "utilities/keyword_engine.py", "lines": "generate_test_report(), lines ~300-400"},
            {"path": "utilities/link_checker_utils.py", "lines": "generate_link_report(), lines ~200-300"}
        ]
    }
}


def main():
    print("=" * 80)
    print("🔍 SELENIUM AUTOMATION TOPIC LOCATOR")
    print("   Shows exactly where each topic is implemented in your codebase")
    print("=" * 80)

    # Display topics
    topic_list = list(TOPICS.keys())
    for i, topic in enumerate(topic_list, 1):
        print(f"{i:2}. {topic}")

    print("\nEnter topic number to see implementation details (or 'q' to quit):")

    while True:
        choice = input("> ").strip()
        if choice.lower() == 'q':
            print("Goodbye!")
            break
        if not choice.isdigit():
            print("❌ Please enter a valid number or 'q'")
            continue

        idx = int(choice)
        if idx < 1 or idx > len(topic_list):
            print(f"❌ Please enter a number between 1 and {len(topic_list)}")
            continue

        topic = topic_list[idx - 1]
        info = TOPICS[topic]

        print("\n" + "=" * 80)
        print(f"📘 TOPIC: {topic}")
        print("=" * 80)
        for file_info in info["files"]:
            print(f"\n📁 File: {file_info['path']}")
            print(f"   📍 Location: {file_info['lines']}")
            # Optional: Check if file exists
            if os.path.exists(file_info['path']):
                print("   ✅ File exists")
            else:
                print("   ⚠️  File not found in current directory")
        print("\n" + "=" * 80)


if __name__ == "__main__":
    main()