from selenium import webdriver
from browser_utils import create_or_use_persistent_profile
from facebook_login import facebook_login
from visitgroup import visit_groups
import time

def main():
    driver = None
    try:
        print("Starting main application...")
        
        # Create or use a persistent profile
        chrome_options = create_or_use_persistent_profile()
        if not chrome_options:
            print("Failed to initialize Chrome options. Exiting.")
            return
        
        # Initialize the WebDriver
        driver = webdriver.Chrome(options=chrome_options)
        
        # First, log in to Facebook
        print("\n--- Starting Facebook Login ---")
        facebook_login(driver)
        
        # Then visit groups
        print("\n--- Starting Groups Navigation ---")
        visit_groups(driver)
        
        # Keep the browser open for a while
        print("\nAutomation complete. You can now close the browser or continue using it.")
        input("Press Enter to close the browser...")
        
    except Exception as e:
        print(f"An error occurred in main: {e}")
    finally:
        if driver:
            driver.quit()

if __name__ == "__main__":
    main()