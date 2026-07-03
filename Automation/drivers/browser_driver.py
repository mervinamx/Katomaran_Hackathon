"""
============================================
  Tichi Login Automation - Browser Driver
============================================
Handles WebDriver setup, teardown, and screenshot capture.
"""

import os
import time
from datetime import datetime

from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager

from config.settings import Config


class BrowserDriver:
    """Manages Chrome WebDriver lifecycle and utility operations."""

    def __init__(self, headless: bool = None):
        """
        Initialize the browser driver.

        Args:
            headless: Run browser in headless mode. Defaults to Config.HEADLESS.
        """
        self.driver = None
        self.headless = headless if headless is not None else Config.HEADLESS

    def start(self) -> webdriver.Chrome:
        """
        Start Chrome browser with configured options.

        Returns:
            Chrome WebDriver instance.
        """
        chrome_options = Options()

        if self.headless:
            chrome_options.add_argument("--headless=new")

        # Common stability options
        chrome_options.add_argument("--no-sandbox")
        chrome_options.add_argument("--disable-dev-shm-usage")
        chrome_options.add_argument("--disable-gpu")
        chrome_options.add_argument("--window-size=1920,1080")
        chrome_options.add_argument("--disable-extensions")
        chrome_options.add_argument("--disable-notifications")
        chrome_options.add_argument("--disable-popup-blocking")

        # Suppress automation detection
        chrome_options.add_argument("--disable-blink-features=AutomationControlled")
        chrome_options.add_experimental_option("excludeSwitches", ["enable-automation"])
        chrome_options.add_experimental_option("useAutomationExtension", False)

        # Initialize ChromeDriver using webdriver-manager (auto-downloads matching version)
        service = Service(ChromeDriverManager().install())
        self.driver = webdriver.Chrome(service=service, options=chrome_options)

        # Set timeouts
        self.driver.implicitly_wait(Config.IMPLICIT_WAIT)
        self.driver.set_page_load_timeout(Config.PAGE_LOAD_TIMEOUT)

        # Maximize window
        if not self.headless:
            self.driver.maximize_window()

        print(f"[✓] Chrome browser started successfully (headless={self.headless})")
        return self.driver

    def take_screenshot(self, name: str, status: str = "info") -> str:
        """
        Take a screenshot and save it to the screenshots directory.

        Args:
            name: Descriptive name for the screenshot.
            status: Status label - 'pass', 'fail', or 'info'.

        Returns:
            Path to the saved screenshot file.
        """
        if not self.driver:
            print("[✗] Cannot take screenshot - driver not initialized")
            return ""

        # Create screenshots directory if it doesn't exist
        os.makedirs(Config.SCREENSHOTS_DIR, exist_ok=True)

        # Generate filename with timestamp
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"{status.upper()}_{name}_{timestamp}.png"
        filepath = os.path.join(Config.SCREENSHOTS_DIR, filename)

        try:
            self.driver.save_screenshot(filepath)
            print(f"[📸] Screenshot saved: {filepath}")
            return filepath
        except Exception as e:
            print(f"[✗] Failed to save screenshot: {e}")
            return ""

    def quit(self):
        """Safely close the browser and clean up."""
        if self.driver:
            try:
                self.driver.quit()
                print("[✓] Browser closed successfully")
            except Exception as e:
                print(f"[!] Error closing browser: {e}")
            finally:
                self.driver = None
