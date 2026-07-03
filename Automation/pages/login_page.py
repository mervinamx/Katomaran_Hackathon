"""
============================================
  Tichi Login Automation - Login Page Object
============================================
Page Object Model for the Tichi login page.
Encapsulates all interactions with the login page.
"""

import time
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import (
    TimeoutException,
    NoSuchElementException,
    ElementNotInteractableException,
)

from config.settings import Config


class LoginPage:
    """Page Object for the Tichi login page."""

    def __init__(self, driver):
        """
        Initialize LoginPage with a WebDriver instance.

        Args:
            driver: Selenium WebDriver instance.
        """
        self.driver = driver
        self.wait = WebDriverWait(driver, Config.IMPLICIT_WAIT)
        self.long_wait = WebDriverWait(driver, Config.PAGE_LOAD_TIMEOUT)

    # ── Navigation ───────────────────────────────────────────

    def navigate_to_login(self):
        """Open the Tichi login page and wait for it to fully load."""
        print(f"[→] Navigating to: {Config.LOGIN_URL}")
        self.driver.get(Config.LOGIN_URL)

        # Wait for the Next.js app to finish loading (spinner disappears)
        self._wait_for_page_load()
        print("[✓] Login page loaded successfully")

    def _wait_for_page_load(self):
        """
        Wait for the dynamic Next.js page to finish rendering.
        The page initially shows a loading spinner, then renders the login form.
        """
        try:
            # First, wait for the loading spinner to disappear
            print("[⏳] Waiting for page to finish loading...")

            # Wait for document ready state
            self.long_wait.until(
                lambda d: d.execute_script("return document.readyState") == "complete"
            )

            # Wait a bit for React/Next.js hydration
            time.sleep(3)

            # Try to wait until at least one input field is present
            self.long_wait.until(
                EC.presence_of_element_located((By.CSS_SELECTOR, "input"))
            )

            print("[✓] Page fully loaded and interactive")

        except TimeoutException:
            print("[!] Page load timed out - attempting to continue anyway")

    # ── Element Finders (Multi-Selector Strategy) ────────────

    def _find_element_by_selectors(self, selector_list: list, description: str):
        """
        Try multiple selectors to find an element. Returns the first match.

        Args:
            selector_list: List of CSS selectors and/or XPath expressions.
            description: Human-readable description for logging.

        Returns:
            WebElement if found.

        Raises:
            NoSuchElementException: If no selector matches.
        """
        for selector in selector_list:
            try:
                if selector.startswith("//"):
                    # XPath selector
                    element = self.wait.until(
                        EC.presence_of_element_located((By.XPATH, selector))
                    )
                elif ":has-text(" in selector:
                    # Custom text-based selector - convert to XPath
                    text = selector.split(":has-text('")[1].rstrip("')")
                    tag = selector.split(":has-text(")[0] or "*"
                    xpath = f"//{tag}[contains(text(),'{text}')]"
                    element = self.wait.until(
                        EC.presence_of_element_located((By.XPATH, xpath))
                    )
                else:
                    # CSS selector
                    element = self.wait.until(
                        EC.presence_of_element_located((By.CSS_SELECTOR, selector))
                    )

                print(f"  [✓] Found {description} using: {selector}")
                return element

            except (TimeoutException, NoSuchElementException):
                continue

        raise NoSuchElementException(
            f"Could not find {description} with any of the configured selectors.\n"
            f"Tried: {selector_list}\n"
            f"TIP: Open the login page in Chrome DevTools and inspect the elements "
            f"to find the correct selectors, then update config/settings.py"
        )

    def _find_email_input(self):
        """Find the email input field."""
        return self._find_element_by_selectors(
            Config.SELECTORS["email_input"], "email input"
        )

    def _find_password_input(self):
        """Find the password input field."""
        return self._find_element_by_selectors(
            Config.SELECTORS["password_input"], "password input"
        )

    def _find_login_button(self):
        """Find the login/sign-in button."""
        return self._find_element_by_selectors(
            Config.SELECTORS["login_button"], "login button"
        )

    # ── Actions ──────────────────────────────────────────────

    def enter_email(self, email: str):
        """
        Type the email address into the email field.

        Args:
            email: Email address to enter.
        """
        print(f"[→] Entering email: {email}")
        email_input = self._find_email_input()
        email_input.clear()
        email_input.send_keys(email)
        print("[✓] Email entered")

    def enter_password(self, password: str):
        """
        Type the password into the password field.

        Args:
            password: Password to enter.
        """
        print("[→] Entering password: ********")
        password_input = self._find_password_input()
        password_input.clear()
        password_input.send_keys(password)
        print("[✓] Password entered")

    def click_login(self):
        """Click the login button."""
        print("[→] Clicking login button...")
        login_btn = self._find_login_button()

        # Scroll to element if needed
        self.driver.execute_script(
            "arguments[0].scrollIntoView({block: 'center'});", login_btn
        )
        time.sleep(0.5)

        try:
            login_btn.click()
        except ElementNotInteractableException:
            # Fallback: click via JavaScript
            self.driver.execute_script("arguments[0].click();", login_btn)

        print("[✓] Login button clicked")

    def login(self, email: str, password: str):
        """
        Perform the complete login flow: enter email, password, and click login.

        Args:
            email: Email address.
            password: Password.
        """
        self.enter_email(email)
        time.sleep(0.5)
        self.enter_password(password)
        time.sleep(0.5)
        self.click_login()

    # ── Verification ─────────────────────────────────────────

    def is_login_successful(self, timeout: int = 15) -> bool:
        """
        Check if login was successful by looking for post-login indicators.

        Args:
            timeout: Maximum seconds to wait for login to complete.

        Returns:
            True if login appears successful, False otherwise.
        """
        print(f"[⏳] Waiting up to {timeout}s for login to complete...")
        wait = WebDriverWait(self.driver, timeout)

        try:
            # Wait for URL to change (away from login page)
            time.sleep(3)  # Allow time for redirect

            current_url = self.driver.current_url
            if current_url != Config.LOGIN_URL and "/login" not in current_url.lower():
                print(f"[✓] URL changed to: {current_url}")
                return True

            # Check for post-login elements
            for selector in Config.SELECTORS["post_login_indicators"]:
                try:
                    if selector.startswith("//"):
                        wait.until(
                            EC.presence_of_element_located((By.XPATH, selector))
                        )
                    else:
                        wait.until(
                            EC.presence_of_element_located(
                                (By.CSS_SELECTOR, selector)
                            )
                        )
                    print(f"[✓] Post-login element found: {selector}")
                    return True
                except TimeoutException:
                    continue

            return False

        except Exception as e:
            print(f"[!] Error checking login status: {e}")
            return False

    def get_error_message(self) -> str:
        """
        Try to extract any visible error message from the page.

        Returns:
            Error message text, or empty string if none found.
        """
        for selector in Config.SELECTORS["error_indicators"]:
            try:
                if selector.startswith("//"):
                    element = self.driver.find_element(By.XPATH, selector)
                else:
                    element = self.driver.find_element(By.CSS_SELECTOR, selector)

                text = element.text.strip()
                if text:
                    return text
            except (NoSuchElementException, Exception):
                continue

        return ""

    def get_page_title(self) -> str:
        """Get the current page title."""
        return self.driver.title

    def get_current_url(self) -> str:
        """Get the current page URL."""
        return self.driver.current_url

    def debug_page_info(self):
        """Print debug information about the current page state."""
        print("\n" + "=" * 50)
        print("  DEBUG: Current Page Info")
        print("=" * 50)
        print(f"  Title : {self.get_page_title()}")
        print(f"  URL   : {self.get_current_url()}")

        # List all input fields on the page
        inputs = self.driver.find_elements(By.CSS_SELECTOR, "input")
        print(f"  Inputs found: {len(inputs)}")
        for i, inp in enumerate(inputs):
            inp_type = inp.get_attribute("type") or "text"
            inp_name = inp.get_attribute("name") or ""
            inp_id = inp.get_attribute("id") or ""
            inp_placeholder = inp.get_attribute("placeholder") or ""
            print(
                f"    [{i}] type={inp_type}, name={inp_name}, "
                f"id={inp_id}, placeholder={inp_placeholder}"
            )

        # List all buttons
        buttons = self.driver.find_elements(By.CSS_SELECTOR, "button")
        print(f"  Buttons found: {len(buttons)}")
        for i, btn in enumerate(buttons):
            btn_text = btn.text.strip() or "(no text)"
            btn_type = btn.get_attribute("type") or ""
            print(f"    [{i}] text='{btn_text}', type={btn_type}")

        print("=" * 50 + "\n")
