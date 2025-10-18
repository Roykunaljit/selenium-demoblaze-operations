import os
import subprocess
from datetime import datetime


class ReportGenerator:
    @staticmethod
    def generate_html_report():
        """Generate HTML report using pytest-html"""
        os.system('pytest --html=reports/test_report.html')

    @staticmethod
    def generate_allure_report():
        """Generate Allure report"""
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        allure_dir = f"reports/allure-reports/{timestamp}"
        os.makedirs(allure_dir, exist_ok=True)

        # Run tests with Allure
        subprocess.run([
            'pytest',
            '--alluredir=reports/allure-results'
        ])

        # Generate report
        subprocess.run([
            'allure', 'generate',
            'reports/allure-results',
            '-o', allure_dir
        ])

        # Open report
        subprocess.run(['allure', 'open', allure_dir])