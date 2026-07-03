"""
============================================
  Tichi Login Automation - Configuration
============================================
Central configuration for the automation project.
Loads settings from .env file and provides defaults.
"""

import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()


class Config:
    """Application configuration loaded from environment variables."""

    # ── Credentials ──────────────────────────────────────────
    EMAIL = os.getenv("TICHI_EMAIL", "")
    PASSWORD = os.getenv("TICHI_PASSWORD", "")

    # ── URLs ─────────────────────────────────────────────────
    BASE_URL = os.getenv("BASE_URL", "https://tichi-app-webapp-stage.web.app/")
    LOGIN_URL = BASE_URL  # Login page is the landing page

    # ── Browser Settings ─────────────────────────────────────
    HEADLESS = os.getenv("HEADLESS", "false").lower() == "true"
    IMPLICIT_WAIT = int(os.getenv("IMPLICIT_WAIT", "10"))
    PAGE_LOAD_TIMEOUT = int(os.getenv("PAGE_LOAD_TIMEOUT", "30"))

    # ── Paths ────────────────────────────────────────────────
    PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    SCREENSHOTS_DIR = os.path.join(PROJECT_ROOT, "screenshots")

    # ── Selectors (CSS / XPath) for Login Page ───────────────
    # These selectors target common patterns in Next.js / React login forms.
    # Update these if the Tichi app uses different element identifiers.
    SELECTORS = {
        # Email input field - tries multiple common selectors
        "email_input": [
            "input[type='email']",
            "input[name='email']",
            "input[placeholder*='email' i]",
            "input[placeholder*='Email' i]",
            "input[id*='email' i]",
            "#email",
        ],
        # Password input field
        "password_input": [
            "input[type='password']",
            "input[name='password']",
            "input[placeholder*='password' i]",
            "input[placeholder*='Password' i]",
            "input[id*='password' i]",
            "#password",
        ],
        # Login / Sign-in button
        "login_button": [
            "button[type='submit']",
            "button:has-text('Log in')",
            "button:has-text('Login')",
            "button:has-text('Sign in')",
            "button:has-text('Sign In')",
            "//button[contains(text(),'Log in')]",
            "//button[contains(text(),'Login')]",
            "//button[contains(text(),'Sign in')]",
            "//button[contains(text(),'Sign In')]",
            "//button[contains(text(),'LOG IN')]",
        ],
        # Post-login indicators (elements that appear after successful login)
        "post_login_indicators": [
            "//a[contains(text(),'Dashboard')]",
            "//span[contains(text(),'Dashboard')]",
            "[class*='dashboard']",
            "[class*='home']",
            "[data-testid='user-avatar']",
            "[class*='sidebar']",
            "[class*='nav']",
        ],
        # Error message indicators
        "error_indicators": [
            "[class*='error']",
            "[class*='alert']",
            "[role='alert']",
            ".toast-error",
            "[class*='invalid']",
        ],
    }
