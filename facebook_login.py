from selenium import webdriver
from browser_utils import create_or_use_persistent_profile
import time

def main():
    driver = None
    try:
        print("Starting Facebook login automation...")
        
        # Get Chrome options with persistent profile from browser_utils.py
        chrome_options = create_or_use_persistent_profile()
        if not chrome_options:
            print("Failed to initialize Chrome options. Exiting.")
            return
            
        # Initialize the WebDriver
        driver = webdriver.Chrome(options=chrome_options)
        
        # Navigate to Facebook
        print("Opening Facebook...")
        driver.get("https://www.facebook.com/")
        
        # Wait for user to log in manually
        print("\n" + "="*50)
        print("Please log in to Facebook in the browser window that just opened.")
        print("This script will wait for 5 minutes for you to complete the login.")
        print("="*50 + "\n")
        
        # Wait for 5 minutes to allow manual login
        time.sleep(300)  # 300 seconds = 5 minutes
        
        print("\nLogin wait period complete. You can now close the browser or continue using it.")
        
        # Keep the browser open until user presses Enter
        input("Press Enter to close the browser...")
        
    except Exception as e:
        print(f"An error occurred: {e}")
    finally:
        if driver:
            driver.quit()

if __name__ == "__main__":
    main()
