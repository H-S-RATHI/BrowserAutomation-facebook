from selenium.webdriver.chrome.options import Options
import os

def create_or_use_persistent_profile():
    try:
        # Path for our persistent automation profile
        automation_profile_dir = os.path.join(os.path.expanduser("~"), "ChromeAutomationProfile")
        
        # Create the profile directory if it doesn't exist
        if not os.path.exists(automation_profile_dir):
            os.makedirs(automation_profile_dir)
            print(f"Created new persistent profile at: {automation_profile_dir}")
        else:
            print(f"Using existing profile at: {automation_profile_dir}")
        
        # Setup Chrome options
        chrome_options = Options()
        
        # Use our persistent profile
        chrome_options.add_argument(f"--user-data-dir={automation_profile_dir}")
        
        # Enable password saving and autofill
        chrome_options.add_argument("--password-store=basic")
        chrome_options.add_experimental_option("prefs", {
            "credentials_enable_service": True,
            "profile.password_manager_enabled": True,
            "autofill.profile_enabled": True,
            "autofill.enabled": True
        })
        
        # Disable automation flags to make it appear more like a regular browser
        chrome_options.add_argument("--disable-blink-features=AutomationControlled")
        chrome_options.add_experimental_option("excludeSwitches", ["enable-automation"])
        chrome_options.add_experimental_option('useAutomationExtension', False)
        
        return chrome_options
    except Exception as e:
        print(f"Error setting up Chrome options: {e}")
        return None
