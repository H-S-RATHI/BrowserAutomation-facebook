import time

def facebook_login(driver):
    """
    Handle Facebook login using the provided WebDriver instance.
    
    Args:
        driver: An initialized WebDriver instance
    """
    try:
        print("Starting Facebook login automation...")
        
        # Navigate to Facebook if not already there
        if "facebook.com" not in driver.current_url:
            print("Navigating to Facebook...")
            driver.get("https://www.facebook.com/")
        
        # Wait for user to log in manually
        print("\n" + "="*50)
        print("Please log in to Facebook in the browser window that just opened.")
        print("This script will wait for 3 seconds for you to complete the login.")
        print("="*50 + "\n")
        
        # Wait for 5 minutes to allow manual login
        time.sleep(3)  # 300 seconds = 5 minutes
        
        print("\nLogin wait period complete. Continuing with automation...")
        
    except Exception as e:
        print(f"An error occurred in facebook_login: {e}")
        raise  # Re-raise the exception to be handled by the calling function
