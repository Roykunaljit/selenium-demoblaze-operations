from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

import pytest
import os
import sys
import socket
import threading
from http.server import HTTPServer, SimpleHTTPRequestHandler
from pathlib import Path
from functools import partial

from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait

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

    def test_upload_single_file_send_keys(self, setup):
        """Test single file upload on The Internet."""
        self.driver.get("https://the-internet.herokuapp.com/upload")

        absolute_file_path = self.file_upload_utils.create_test_file(
            "test_files/sample.txt",
            "Single file test content"
        )
        assert absolute_file_path and os.path.exists(absolute_file_path)

        try:
            success = self.file_upload_utils.upload_file_using_send_keys(
                (By.ID, "file-upload"),
                absolute_file_path
            )
            assert success, "File upload failed"

            self.driver.find_element(By.ID, "file-submit").click()

            # Wait for the success message
            success_heading = WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located((By.TAG_NAME, "h3"))
            )
            assert "File Uploaded!" in success_heading.text
            self.logger.info("✅ Single file upload test passed")

        finally:
            if os.path.exists(absolute_file_path):
                os.remove(absolute_file_path)
                # Clean up directory if empty
                dir_path = os.path.dirname(absolute_file_path)
                if os.path.exists(dir_path) and not os.listdir(dir_path):
                    os.rmdir(dir_path)

    def test_upload_multiple_files(self, setup):
        """Test multiple file upload using local test page."""
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
            self.logger.info("✅ Multiple file upload test passed")

        finally:
            # Clean up
            for fp in file_paths:
                if os.path.exists(fp):
                    os.remove(fp)

            # Clean up directory if empty
            dir_path = os.path.dirname(file_paths[0]) if file_paths else None
            if dir_path and os.path.exists(dir_path) and not os.listdir(dir_path):
                os.rmdir(dir_path)