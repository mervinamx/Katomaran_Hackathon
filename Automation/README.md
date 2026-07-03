# 🔐 Tichi Login Automation

Automated login testing for the **Tichi web application** using **Selenium + Python**.

**Target:** https://tichi-app-webapp-stage.web.app/

---

## 📁 Project Structure

```
my project/
├── config/
│   ├── __init__.py
│   └── settings.py          # Configuration & selectors
├── drivers/
│   ├── __init__.py
│   └── browser_driver.py    # Chrome WebDriver management
├── pages/
│   ├── __init__.py
│   └── login_page.py        # Login Page Object Model
├── screenshots/              # Auto-generated screenshots (gitignored)
├── .env                      # Your credentials (gitignored)
├── .gitignore
├── inspect_page.py           # Page inspector/debugger
├── requirements.txt
├── run_login.py              # Main automation runner
└── README.md
```

---

## 🚀 Quick Start

### 1. Install Python Dependencies

```bash
pip install -r requirements.txt
```

### 2. Configure Credentials

Edit the `.env` file with your Tichi login credentials:

```env
TICHI_EMAIL=your_email@example.com
TICHI_PASSWORD=your_password_here
```

### 3. Run the Login Automation

```bash
# Run with visible browser (recommended first time)
python run_login.py

# Run in headless mode (no browser window)
python run_login.py --headless

# Run with debug output (shows page element details)
python run_login.py --debug

# Combine flags
python run_login.py --headless --debug
```

---

## 🔍 Debugging

If the automation fails to find elements on the page, use the **Page Inspector**:

```bash
python inspect_page.py
```

This will:
1. Open the Tichi login page in Chrome
2. Print all `<input>`, `<button>`, `<a>`, and `<form>` elements with their attributes
3. Take a screenshot
4. Keep the browser open for 30 seconds for manual inspection

Then update the selectors in `config/settings.py` based on what you find.

---

## 📸 Screenshots

Screenshots are automatically saved in the `screenshots/` folder:

| File Pattern | Description |
|---|---|
| `INFO_01_login_page_loaded_*.png` | Login page after loading |
| `INFO_02_credentials_entered_*.png` | After filling in credentials |
| `PASS_03_login_success_*.png` | Successful login |
| `FAIL_03_login_failed_*.png` | Failed login attempt |

---

## ⚙️ Configuration

All settings are in `config/settings.py` and can be overridden via the `.env` file:

| Setting | Default | Description |
|---|---|---|
| `TICHI_EMAIL` | - | Your login email |
| `TICHI_PASSWORD` | - | Your login password |
| `BASE_URL` | `https://tichi-app-webapp-stage.web.app/` | Target URL |
| `HEADLESS` | `false` | Run without browser UI |
| `IMPLICIT_WAIT` | `10` | Element wait timeout (seconds) |
| `PAGE_LOAD_TIMEOUT` | `30` | Page load timeout (seconds) |

---

## 🛠 Updating Selectors

The login page selectors are defined in `config/settings.py` under `Config.SELECTORS`. Each field has multiple fallback selectors that are tried in order:

```python
SELECTORS = {
    "email_input": [
        "input[type='email']",
        "input[name='email']",
        # ... add more selectors as needed
    ],
    # ...
}
```

If the Tichi website updates its UI, run `python inspect_page.py` and update these selectors.

---

## 📋 Requirements

- **Python** 3.8+
- **Google Chrome** browser installed
- ChromeDriver is auto-managed by `webdriver-manager`
