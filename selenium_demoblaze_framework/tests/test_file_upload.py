import pytest
import os
import sys
import socket
import threading
from http.server import HTTPServer, SimpleHTTPRequestHandler
from pathlib import Path
from functools import partial

from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from selenium_demoblaze_framework.utilities.file_upload_utils import FileUploadUtils
from selenium_demoblaze_framework.utilities.custom_logger import CustomLogger
from selenium_demoblaze_framework.config.browser_config import BrowserConfig


def find_free_port():
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.bind(("", 0))
        return s.getsockname()[1]


class CustomHTTPRequestHandler(SimpleHTTPRequestHandler):
    """Custom handler that serves files from a specific directory"""

    def __init__(self, *args, directory=None, **kwargs):
        self.directory = directory
        super().__init__(*args, directory=directory, **kwargs)

    def log_message(self, format, *args):
        """Override to suppress console logging or customize it"""
        pass


class TestFileUpload:

    @pytest.fixture
    def setup(self):
        self.logger = CustomLogger.get_logger(self.__class__.__name__)
        self.browser_config = BrowserConfig()
        self.driver = self.browser_config.get_driver()
        self.file_upload_utils = FileUploadUtils(self.driver, self.logger)

        # Start local server for multiple upload test
        self.test_pages_dir = os.path.join(os.path.dirname(__file__), "..", "test_pages")

        # Create test_pages directory if it doesn't exist
        os.makedirs(self.test_pages_dir, exist_ok=True)

        # Create the HTML test file
        self._create_test_html()

        self.port = find_free_port()

        # Create handler with custom directory
        handler = partial(CustomHTTPRequestHandler, directory=self.test_pages_dir)

        self.server = HTTPServer(("localhost", self.port), handler)
        self.server_thread = threading.Thread(target=self.server.serve_forever)
        self.server_thread.daemon = True
        self.server_thread.start()

        self.logger.info(f"HTTP Server started on port {self.port}, serving from {self.test_pages_dir}")

        yield

        self.driver.quit()
        self.server.shutdown()
        self.server.server_close()

    def _create_test_html(self):
        """Create the multiple upload test HTML file"""
        html_content = """<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>Multiple File Upload Test</title>
    <style>
        body { font-family: Arial, sans-serif; padding: 20px; }
        #upload-area {
            border: 2px dashed #ccc;
            padding: 20px;
            text-align: center;
            margin: 20px 0;
        }
        #file-list { margin-top: 15px; }
        button { padding: 8px 16px; font-size: 16px; }
    </style>
</head>
<body>
    <h2>Multiple File Upload Test Page</h2>
    <p>Select one or more files and click "Upload".</p>

    <input type="file" id="file-upload" multiple />
    <br><br>
    <button id="upload-btn" onclick="uploadFiles()">Upload</button>

    <div id="upload-area">
        <p>Files will appear here after upload:</p>
        <ul id="file-list"></ul>
    </div>

    <script>
        function uploadFiles() {
            const input = document.getElementById('file-upload');
            const list = document.getElementById('file-list');
            list.innerHTML = '';
            if (input.files.length === 0) {
                alert('No files selected!');
                return;
            }
            for (let file of input.files) {
                const li = document.createElement('li');
                li.textContent = `${file.name} (${file.size} bytes)`;
                list.appendChild(li);
            }
            // Simulate successful upload
            alert(`Successfully "uploaded" ${input.files.length} file(s)!`);
        }
    </script>
</body>
</html>"""

        html_path = os.path.join(self.test_pages_dir, "multiple_upload_test.html")
        with open(html_path, 'w', encoding='utf-8') as f:
            f.write(html_content)

        self.logger.info(f"Test HTML file created at: {html_path}")

    def test_upload_single_file_send_keys_local(self, setup):
        """Test single file upload using send_keys on our local test page."""
        test_url = f"http://localhost:{self.port}/multiple_upload_test.html"
        self.driver.get(test_url)

        absolute_file_path = self.file_upload_utils.create_test_file(
            "test_files/sample.txt",
            "Single file test content"
        )
        assert absolute_file_path and os.path.exists(absolute_file_path)

        try:
            # Locate file input and upload using send_keys
            file_input = WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located((By.ID, "file-upload"))
            )

            # Clear any pre-existing value (if any) and send keys
            file_input.clear()
            file_input.send_keys(absolute_file_path)

            self.logger.info(f"Uploaded file via send_keys: {absolute_file_path}")

            # Click upload button to trigger JS
            upload_btn = WebDriverWait(self.driver, 10).until(
                EC.element_to_be_clickable((By.ID, "upload-btn"))
            )
            upload_btn.click()

            # Wait for alert and accept it
            WebDriverWait(self.driver, 5).until(EC.alert_is_present())
            alert = self.driver.switch_to.alert
            alert_text = alert.text
            alert.accept()

            # Verify the success message
            assert "Successfully" in alert_text
            self.logger.info("[PASS] Single file upload test passed (Local Server)")

        finally:
            if os.path.exists(absolute_file_path):
                os.remove(absolute_file_path)
                # Clean up directory if empty
                dir_path = os.path.dirname(absolute_file_path)
                if os.path.exists(dir_path) and not os.listdir(dir_path):
                    os.rmdir(dir_path)

    def test_upload_multiple_files_local(self, setup):
        """Test multiple file upload using our local test page."""
        test_url = f"http://localhost:{self.port}/multiple_upload_test.html"
        self.driver.get(test_url)

        # Create 3 test files
        file_paths = []
        for i in range(3):
            path = self.file_upload_utils.create_test_file(
                f"test_files/file_{i}.txt",
                f"Content of file {i}"
            )
            assert path and os.path.exists(path)
            file_paths.append(path)

        try:
            # Upload all files at once
            success = self.file_upload_utils.upload_multiple_files(
                (By.ID, "file-upload"),
                file_paths
            )
            assert success, "Multiple file upload failed"

            # Click upload button to trigger JS
            upload_btn = WebDriverWait(self.driver, 10).until(
                EC.element_to_be_clickable((By.ID, "upload-btn"))
            )
            upload_btn.click()

            # Wait for alert and accept it
            WebDriverWait(self.driver, 5).until(EC.alert_is_present())
            alert = self.driver.switch_to.alert
            alert_text = alert.text
            alert.accept()

            assert "Successfully" in alert_text
            self.logger.info("[PASS] Multiple file upload test passed (Local Server)")

        finally:
            # Clean up
            for fp in file_paths:
                if os.path.exists(fp):
                    os.remove(fp)

            # Clean up directory if empty
            dir_path = os.path.dirname(file_paths[0]) if file_paths else None
            if dir_path and os.path.exists(dir_path) and not os.listdir(dir_path):
                os.rmdir(dir_path)

    # def test_upload_single_file_guru99(self, setup):
    #     """
    #     Test single file upload on guru99.com
    #     Expected success message: "1 file has been successfully uploaded."
    #     """
    #     self.logger.info("Testing file upload on guru99.com")
    #
    #     # Navigate to guru99 file upload demo
    #     self.driver.get("https://demo.guru99.com/test/upload/")
    #
    #     # Define the path to the test file
    #     test_file_name = "SELENIUM_GRID.pdf"
    #     test_file_path = os.path.join(os.getcwd(), test_file_name)
    #
    #     # If the file doesn't exist locally, create a dummy one for testing purposes.
    #     if not os.path.exists(test_file_path):
    #         self.logger.warning(f"Test file '{test_file_name}' not found. Creating a dummy file.")
    #         # Create a minimal valid PDF with only ASCII characters in byte literal
    #         pdf_content = (
    #             b"%PDF-1.7\n"
    #             b"%\xe2\xe3\xcf\xd3\n"  # Binary marker (using hex escape sequences)
    #             b"1 0 obj\n"
    #             b"<< /Type /Catalog /Pages 2 0 R >>\n"
    #             b"endobj\n"
    #             b"2 0 obj\n"
    #             b"<< /Type /Pages /Kids [3 0 R] /Count 1 >>\n"
    #             b"endobj\n"
    #             b"3 0 obj\n"
    #             b"<< /Type /Page /Parent 2 0 R /Contents 4 0 R >>\n"
    #             b"endobj\n"
    #             b"4 0 obj\n"
    #             b"<< /Length 43 >>\n"
    #             b"stream\n"
    #             b"BT /F1 12 Tf 72 720 Td (Hello, World!) Tj ET\n"
    #             b"endstream\n"
    #             b"endobj\n"
    #             b"xref\n"
    #             b"0 5\n"
    #             b"0000000000 65535 f \n"
    #             b"0000000015 00000 n \n"
    #             b"0000000065 00000 n \n"
    #             b"0000000115 00000 n \n"
    #             b"0000000165 00000 n \n"
    #             b"trailer\n"
    #             b"<< /Size 5 /Root 1 0 R >>\n"
    #             b"startxref\n"
    #             b"215\n"
    #             b"%%EOF\n"
    #         )
    #         with open(test_file_path, 'wb') as f:
    #             f.write(pdf_content)
    #
    #     assert os.path.exists(test_file_path), f"Test file {test_file_path} does not exist."
    #
    #     try:
    #         # Locate the file input element
    #         file_input = WebDriverWait(self.driver, 10).until(
    #             EC.presence_of_element_located((By.NAME, "uploadfile_0"))
    #         )
    #
    #         # Send the file path
    #         file_input.send_keys(test_file_path)
    #         self.logger.info(f"Selected file: {test_file_path}")
    #
    #         # Check the terms checkbox
    #         terms_checkbox = self.driver.find_element(By.ID, "terms")
    #         if not terms_checkbox.is_selected():
    #             terms_checkbox.click()
    #             self.logger.info("Accepted terms of service")
    #
    #         # Click submit button
    #         submit_btn = self.driver.find_element(By.NAME, "send")
    #         submit_btn.click()
    #
    #         # Wait for the success message - FIXED XPATH
    #         # The actual message is "1 file has been successfully uploaded."
    #         # Try multiple possible selectors
    #         success_msg = WebDriverWait(self.driver, 15).until(
    #             EC.presence_of_element_located((By.XPATH, "//*[contains(text(), 'successfully uploaded')]"))
    #         )
    #
    #         # Assert that the success message is present
    #         assert "successfully uploaded" in success_msg.text.lower()
    #         self.logger.info("[PASS] File upload successful on Guru99")
    #         self.logger.info(f"Success message: {success_msg.text}")
    #
    #     except Exception as e:
    #         self.logger.error(f"[FAIL] File upload test on Guru99 failed: {e}")
    #         # Print page source for debugging
    #         self.logger.error(f"Current URL: {self.driver.current_url}")
    #         raise  # Re-raise to fail the test
    #
    #     finally:
    #         # Cleanup: Delete the dummy file if we created it
    #         if test_file_path.endswith("SELENIUM_GRID.pdf") and os.path.exists(test_file_path):
    #             os.remove(test_file_path)
    #             self.logger.info("Cleaned up test file")