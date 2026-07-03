"""
============================================================
  🔐 Tichi Login Automation - Main Runner
============================================================
Automates the login flow for:
  https://tichi-app-webapp-stage.web.app/

Usage:
  python run_login.py
  python run_login.py --headless
  python run_login.py --debug

Make sure to set your credentials in the .env file first!
============================================================
"""

import sys
import time
import argparse
from datetime import datetime

from config.settings import Config
from drivers.browser_driver import BrowserDriver
from pages.login_page import LoginPage


def print_banner():
    """Print a styled banner."""
    banner = """
╔══════════════════════════════════════════════╗
║       🔐 Tichi Login Automation             ║
║       ─────────────────────────              ║
║  Target: tichi-app-webapp-stage.web.app      ║
║  Engine: Selenium + ChromeDriver             ║
╚══════════════════════════════════════════════╝
    """
    print(banner)


def print_result(success: bool, duration: float):
    """Print the final result."""
    if success:
        print(f"""
╔══════════════════════════════════════════════╗
║  ✅  LOGIN SUCCESSFUL                        ║
║  ⏱   Duration: {duration:.2f}s{' ' * (30 - len(f'{duration:.2f}s'))}║
║  📸  Screenshots saved in: screenshots/      ║
╚══════════════════════════════════════════════╝
        """)
    else:
        print(f"""
╔══════════════════════════════════════════════╗
║  ❌  LOGIN FAILED                            ║
║  ⏱   Duration: {duration:.2f}s{' ' * (30 - len(f'{duration:.2f}s'))}║
║  📸  Check screenshots/ for failure details   ║
║  💡  Run with --debug to inspect the page     ║
╚══════════════════════════════════════════════╝
        """)


def run_login(headless: bool = False, debug: bool = False):
    """
    Execute the login automation.

    Args:
        headless: Run in headless mode (no visible browser).
        debug: Enable debug mode (prints page element info).

    Returns:
        True if login was successful, False otherwise.
    """
    print_banner()
    start_time = time.time()

    # Validate credentials
    if not Config.EMAIL or Config.EMAIL == "your_email@example.com":
        print("[✗] ERROR: Email not configured!")
        print("    → Edit the .env file and set TICHI_EMAIL=your_email@example.com")
        return False

    if not Config.PASSWORD or Config.PASSWORD == "your_password_here":
        print("[✗] ERROR: Password not configured!")
        print("    → Edit the .env file and set TICHI_PASSWORD=your_password")
        return False

    print(f"[i] Email: {Config.EMAIL}")
    print(f"[i] URL  : {Config.LOGIN_URL}")
    print(f"[i] Mode : {'Headless' if headless else 'Visible'}")
    print(f"[i] Time : {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("-" * 50)

    # Initialize browser
    browser = BrowserDriver(headless=headless)

    try:
        driver = browser.start()
        login_page = LoginPage(driver)

        # Step 1: Navigate to login page
        print("\n📌 Step 1: Navigate to login page")
        login_page.navigate_to_login()
        browser.take_screenshot("01_login_page_loaded", "info")

        # Debug: Print page info
        if debug:
            login_page.debug_page_info()

        # Step 2: Enter credentials
        print("\n📌 Step 2: Enter credentials")
        login_page.login(Config.EMAIL, Config.PASSWORD)
        browser.take_screenshot("02_credentials_entered", "info")

        # Step 3: Wait and verify login
        print("\n📌 Step 3: Verify login result")
        time.sleep(3)  # Allow time for the login request to process

        success = login_page.is_login_successful()

        if success:
            browser.take_screenshot("03_login_success", "pass")
            duration = time.time() - start_time
            print_result(True, duration)
            return True
        else:
            # Check for error message
            error_msg = login_page.get_error_message()
            if error_msg:
                print(f"[✗] Error message on page: {error_msg}")

            browser.take_screenshot("03_login_failed", "fail")

            if debug:
                login_page.debug_page_info()

            duration = time.time() - start_time
            print_result(False, duration)
            return False

    except Exception as e:
        print(f"\n[✗] UNEXPECTED ERROR: {e}")
        browser.take_screenshot("error_unexpected", "fail")

        if debug:
            import traceback
            traceback.print_exc()

        duration = time.time() - start_time
        print_result(False, duration)
        return False

    finally:
        # Always close the browser
        print("\n[→] Cleaning up...")
        browser.quit()


def main():
    """Parse command-line arguments and run the login automation."""
    parser = argparse.ArgumentParser(
        description="🔐 Tichi Login Automation",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python run_login.py                  # Run with visible browser
  python run_login.py --headless       # Run without opening browser
  python run_login.py --debug          # Run with debug output
  python run_login.py --headless --debug
        """,
    )
    parser.add_argument(
        "--headless",
        action="store_true",
        help="Run browser in headless mode (no visible window)",
    )
    parser.add_argument(
        "--debug",
        action="store_true",
        help="Enable debug mode (prints page element information)",
    )

    args = parser.parse_args()
    success = run_login(headless=args.headless, debug=args.debug)
    sys.exit(0 if success else 1)


if __name__ == "__main__":
    main()
