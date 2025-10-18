import requests
from selenium.webdriver.common.by import By
from selenium.common.exceptions import StaleElementReferenceException
from urllib.parse import urljoin, urlparse
from datetime import datetime
import os
import time


class LinkCheckerUtils:
    def __init__(self, driver, logger):
        self.driver = driver
        self.logger = logger
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
        })

    def check_all_links(self, check_images=False):
        """
        Find and check all links (and optionally images) on the current page.
        Highlights broken links with red border.
        Returns list of results.
        """
        results = []
        elements_to_check = []

        # Get all <a> tags
        try:
            links = self.driver.find_elements(By.TAG_NAME, "a")
            for el in links:
                elements_to_check.append(('link', el))
        except Exception as e:
            self.logger.error(f"Error fetching links: {e}")

        # Optionally get all <img> tags
        if check_images:
            try:
                images = self.driver.find_elements(By.TAG_NAME, "img")
                for el in images:
                    elements_to_check.append(('image', el))
            except Exception as e:
                self.logger.error(f"Error fetching images: {e}")

        self.logger.info(f"Found {len(elements_to_check)} elements to check")

        for index, (el_type, element) in enumerate(elements_to_check, 1):
            try:
                if el_type == 'link':
                    url = element.get_attribute("href")
                    text = element.text or "No text"
                else:  # image
                    url = element.get_attribute("src")
                    text = element.get_attribute("alt") or "Image"

                if not url:
                    continue

                self.logger.info(f"Checking {el_type} {index}/{len(elements_to_check)}: {url}")

                is_broken, status_code, status_text = self.check_link_status(url)

                results.append({
                    'url': url,
                    'text': text,
                    'type': el_type,
                    'is_broken': is_broken,
                    'status_code': status_code,
                    'status_text': status_text
                })

                # 🔴 Highlight broken links/images on the page
                if is_broken:
                    try:
                        self.driver.execute_script(
                            "arguments[0].style.border = '3px solid red'; "
                            "arguments[0].title = 'BROKEN LINK';",
                            element
                        )
                        self.logger.warning(f"Highlighted broken {el_type}: {url}")
                    except StaleElementReferenceException:
                        self.logger.warning(f"Could not highlight broken {el_type} (element stale): {url}")
                    except Exception as e:
                        self.logger.error(f"Failed to highlight element: {e}")

                # Optional: small delay to avoid overwhelming server
                time.sleep(0.1)

            except StaleElementReferenceException:
                self.logger.warning(f"Skipping stale element during link check")
                continue
            except Exception as e:
                self.logger.error(f"Error checking element: {str(e)}")

        return results

    def check_internal_links_only(self, base_url):
        """
        Check only internal links (same domain as base_url)
        """
        results = []
        elements = self.driver.find_elements(By.TAG_NAME, "a")

        parsed_base = urlparse(base_url)
        base_domain = parsed_base.netloc

        for el in elements:
            try:
                url = el.get_attribute("href")
                if not url:
                    continue

                # Skip non-HTTP links
                if url.startswith(('javascript:', 'mailto:', 'tel:', '#')):
                    continue

                parsed_url = urlparse(url)
                link_domain = parsed_url.netloc

                # Check if internal: same domain or relative URL
                if not link_domain or link_domain == base_domain:
                    is_broken, status_code, status_text = self.check_link_status(url)
                    text = el.text or "No text"
                    results.append({
                        'url': url,
                        'text': text,
                        'type': 'link',
                        'is_broken': is_broken,
                        'status_code': status_code,
                        'status_text': status_text
                    })

                    # 🔴 Highlight broken internal links
                    if is_broken:
                        try:
                            self.driver.execute_script(
                                "arguments[0].style.border = '3px solid red'; "
                                "arguments[0].title = 'BROKEN INTERNAL LINK';",
                                el
                            )
                        except:
                            pass

            except Exception as e:
                self.logger.warning(f"Error checking internal link: {e}")
                continue

        return results

    def check_external_links_only(self, base_url):
        """
        Check only external links (different domain than base_url)
        """
        results = []
        elements = self.driver.find_elements(By.TAG_NAME, "a")

        parsed_base = urlparse(base_url)
        base_domain = parsed_base.netloc

        for el in elements:
            try:
                url = el.get_attribute("href")
                if not url:
                    continue

                if url.startswith(('javascript:', 'mailto:', 'tel:', '#')):
                    continue

                parsed_url = urlparse(url)
                link_domain = parsed_url.netloc

                # Check if external: different domain and not empty
                if link_domain and link_domain != base_domain:
                    is_broken, status_code, status_text = self.check_link_status(url)
                    text = el.text or "No text"
                    results.append({
                        'url': url,
                        'text': text,
                        'type': 'link',
                        'is_broken': is_broken,
                        'status_code': status_code,
                        'status_text': status_text
                    })

                    # 🔴 Highlight broken external links
                    if is_broken:
                        try:
                            self.driver.execute_script(
                                "arguments[0].style.border = '3px solid red'; "
                                "arguments[0].title = 'BROKEN EXTERNAL LINK';",
                                el
                            )
                        except:
                            pass

            except Exception as e:
                self.logger.warning(f"Error checking external link: {e}")
                continue

        return results

    def check_link_status(self, url):
        """
        Check if a URL is accessible.
        Returns (is_broken, status_code, status_text)
        """
        try:
            # Skip non-HTTP(S) links
            if url.strip().startswith(('javascript:', 'mailto:', 'tel:', '#', 'data:')):
                return False, None, "Skipped (non-HTTP)"

            # Normalize URL
            if url.startswith("//"):
                url = "https:" + url
            elif url.startswith("www."):
                url = "https://" + url

            if not url.startswith(("http://", "https://")):
                return True, None, "Invalid URL scheme"

            # Try HEAD first (faster)
            response = self.session.head(url, timeout=10, allow_redirects=True)

            # If HEAD returns error, try GET (some servers block HEAD)
            if response.status_code >= 400:
                response = self.session.get(url, timeout=10, allow_redirects=True)

            if response.status_code >= 400:
                return True, response.status_code, response.reason
            else:
                return False, response.status_code, "OK"

        except requests.exceptions.Timeout:
            return True, None, "Timeout"
        except requests.exceptions.ConnectionError:
            return True, None, "Connection Error"
        except requests.exceptions.RequestException as e:
            return True, None, f"Request Error: {str(e)}"
        except Exception as e:
            return True, None, f"Unexpected Error: {str(e)}"

    def generate_link_report(self, results, output_file=None):
        """
        Generate an HTML report of link check results
        """
        total_links = len(results)
        broken_links = len([r for r in results if r['is_broken']])
        working_links = total_links - broken_links

        html_content = f"""
        <!DOCTYPE html>
        <html>
        <head>
            <title>🔗 Link Check Report</title>
            <style>
                body {{ font-family: Arial, sans-serif; margin: 20px; background-color: #f5f5f5; }}
                .container {{ max-width: 1200px; margin: 0 auto; background-color: white; padding: 20px; box-shadow: 0 0 10px rgba(0,0,0,0.1); }}
                h1 {{ color: #333; border-bottom: 3px solid #4CAF50; padding-bottom: 10px; }}
                .summary {{ margin-bottom: 20px; padding: 20px; background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); color: white; border-radius: 8px; }}
                .stat-box {{ display: inline-block; margin: 10px 20px 10px 0; }}
                .stat-value {{ font-size: 24px; font-weight: bold; }}
                .stat-label {{ font-size: 14px; opacity: 0.9; }}
                table {{ border-collapse: collapse; width: 100%; margin-top: 20px; box-shadow: 0 2px 4px rgba(0,0,0,0.1); }}
                th, td {{ border: 1px solid #ddd; padding: 12px; text-align: left; }}
                th {{ background-color: #4CAF50; color: white; font-weight: bold; }}
                tr:nth-child(even) {{ background-color: #f9f9f9; }}
                .broken {{ background-color: #ffcccc !important; }}
                .ok {{ background-color: #ccffcc !important; }}
                .status-broken {{ color: #dc3545; font-weight: bold; }}
                .status-ok {{ color: #28a745; font-weight: bold; }}
            </style>
        </head>
        <body>
            <div class="container">
                <h1>🔗 Link Check Report</h1>
                <div class="summary">
                    <h2>Summary Statistics</h2>
                    <div class="stat-box">
                        <div class="stat-value">{total_links}</div>
                        <div class="stat-label">Total Links/Images</div>
                    </div>
                    <div class="stat-box">
                        <div class="stat-value" style="color: #FFB6C1;">{broken_links}</div>
                        <div class="stat-label">Broken</div>
                    </div>
                    <div class="stat-box">
                        <div class="stat-value" style="color: #90EE90;">{working_links}</div>
                        <div class="stat-label">Working</div>
                    </div>
                    <div class="stat-box">
                        <div class="stat-value">{(working_links / total_links * 100):.1f}%</div>
                        <div class="stat-label">Success Rate</div>
                    </div>
                    <div class="stat-box">
                        <div class="stat-value">{datetime.now().strftime("%H:%M:%S")}</div>
                        <div class="stat-label">{datetime.now().strftime("%Y-%m-%d")}</div>
                    </div>
                </div>

                <h2>📋 Details</h2>
                <table>
                    <tr>
                        <th>Type</th>
                        <th>URL</th>
                        <th>Text/Alt</th>
                        <th>Status Code</th>
                        <th>Status</th>
                        <th>Message</th>
                    </tr>
        """

        for result in results:
            row_class = 'broken' if result['is_broken'] else 'ok'
            status_class = 'status-broken' if result['is_broken'] else 'status-ok'
            status_icon = '✗' if result['is_broken'] else '✓'

            url = (result['url'] or '').replace('<', '<').replace('>', '>')
            text = (result['text'] or '').replace('<', '<').replace('>', '>')

            html_content += f"""
                <tr class="{row_class}">
                    <td>{result['type'].upper()}</td>
                    <td><a href="{url}" target="_blank">{url}</a></td>
                    <td>{text}</td>
                    <td>{result['status_code'] or 'N/A'}</td>
                    <td class="{status_class}">{status_icon} {'BROKEN' if result['is_broken'] else 'OK'}</td>
                    <td>{result['status_text']}</td>
                </tr>
            """

        html_content += """
                </table>
            </div>
        </body>
        </html>
        """

        # Save report
        report_dir = "reports"
        os.makedirs(report_dir, exist_ok=True)
        if output_file is None:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            output_file = os.path.join(report_dir, f"link_check_report_{timestamp}.html")

        with open(output_file, 'w', encoding='utf-8') as f:
            f.write(html_content)

        self.logger.info(f" Link report saved: {output_file}")
        return output_file