"""
============================================================
  🔍 Tichi Login Page Inspector
============================================================
Use this script to inspect the login page and discover
the correct element selectors.

This is useful when:
  - The login automation fails to find elements
  - The website has been updated and selectors need updating
  - You need to debug what's on the page

Usage:
  python inspect_page.py
============================================================
"""

import time
from drivers.browser_driver import BrowserDriver
from config.settings import Config
from selenium.webdriver.common.by import By


def inspect_login_page():
    """Open the login page and print detailed element information."""
    print("\n🔍 Tichi Login Page Inspector")
    print("=" * 60)
    print(f"URL: {Config.LOGIN_URL}")
    print("=" * 60)

    browser = BrowserDriver(headless=False)

    try:
        driver = browser.start()
        print(f"\n[→] Loading page: {Config.LOGIN_URL}")
        driver.get(Config.LOGIN_URL)

        # Wait for dynamic content
        print("[⏳] Waiting for page to fully render...")
        time.sleep(8)  # Extra time for Next.js hydration

        print(f"\n📋 Page Title: {driver.title}")
        print(f"📋 Current URL: {driver.current_url}")

        # ── Inspect all <input> elements ─────────────────────
        inputs = driver.find_elements(By.CSS_SELECTOR, "input")
        print(f"\n{'─' * 60}")
        print(f"  📝 INPUT ELEMENTS FOUND: {len(inputs)}")
        print(f"{'─' * 60}")
        for i, inp in enumerate(inputs):
            attrs = {}
            for attr in ["type", "name", "id", "placeholder", "class", "aria-label", "autocomplete"]:
                val = inp.get_attribute(attr)
                if val:
                    attrs[attr] = val
            visible = inp.is_displayed()
            print(f"  [{i}] visible={visible}")
            for k, v in attrs.items():
                print(f"       {k}: {v}")
            print()

        # ── Inspect all <button> elements ────────────────────
        buttons = driver.find_elements(By.CSS_SELECTOR, "button")
        print(f"{'─' * 60}")
        print(f"  🔘 BUTTON ELEMENTS FOUND: {len(buttons)}")
        print(f"{'─' * 60}")
        for i, btn in enumerate(buttons):
            text = btn.text.strip() or "(no text)"
            btn_type = btn.get_attribute("type") or ""
            btn_class = btn.get_attribute("class") or ""
            btn_id = btn.get_attribute("id") or ""
            visible = btn.is_displayed()
            print(f"  [{i}] text: '{text}'")
            print(f"       type: {btn_type}, id: {btn_id}")
            print(f"       class: {btn_class[:80]}...")
            print(f"       visible: {visible}")
            print()

        # ── Inspect all <a> link elements ────────────────────
        links = driver.find_elements(By.CSS_SELECTOR, "a")
        print(f"{'─' * 60}")
        print(f"  🔗 LINK ELEMENTS FOUND: {len(links)}")
        print(f"{'─' * 60}")
        for i, link in enumerate(links):
            text = link.text.strip() or "(no text)"
            href = link.get_attribute("href") or ""
            print(f"  [{i}] text: '{text}', href: {href}")
        print()

        # ── Inspect forms ────────────────────────────────────
        forms = driver.find_elements(By.CSS_SELECTOR, "form")
        print(f"{'─' * 60}")
        print(f"  📄 FORM ELEMENTS FOUND: {len(forms)}")
        print(f"{'─' * 60}")
        for i, form in enumerate(forms):
            action = form.get_attribute("action") or ""
            method = form.get_attribute("method") or ""
            form_id = form.get_attribute("id") or ""
            print(f"  [{i}] action: {action}, method: {method}, id: {form_id}")
        print()

        # Take a screenshot of the page
        browser.take_screenshot("inspect_login_page", "info")

        print("=" * 60)
        print("  ✅ Inspection complete!")
        print("  📸 Screenshot saved in screenshots/ folder")
        print("  💡 Update config/settings.py with the correct selectors")
        print("=" * 60)

        # Keep browser open for manual inspection
        print("\n[!] Browser will stay open for 30 seconds for manual inspection...")
        print("    Press Ctrl+C to close earlier.")

        try:
            time.sleep(30)
        except KeyboardInterrupt:
            print("\n[→] Closing...")

    except Exception as e:
        print(f"\n[✗] Error during inspection: {e}")
        import traceback
        traceback.print_exc()

    finally:
        browser.quit()


if __name__ == "__main__":
    inspect_login_page()
