import time
import random
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException

def is_logged_in(driver):
    """Check if user is already logged in to Facebook"""
    try:
        # Check for elements that indicate user is logged in
        logged_in_indicators = [
            (By.CSS_SELECTOR, "div[role='navigation']"),
            (By.CSS_SELECTOR, "div[aria-label='Facebook']"),
            (By.CSS_SELECTOR, "a[aria-label='Profile']")
        ]
        
        for by, selector in logged_in_indicators:
            try:
                WebDriverWait(driver, 5).until(EC.presence_of_element_located((by, selector)))
                return True
            except (TimeoutException, NoSuchElementException):
                continue
        return False
    except Exception as e:
        print(f"Error checking login status: {e}")
        return False

def human_like_behavior(driver):
    """Simulate human-like behavior after login"""
    try:
        # Random scroll
        scroll_actions = [
            lambda: driver.execute_script("window.scrollBy(0, 500);"),
            lambda: driver.execute_script("window.scrollBy(0, 300);"),
            lambda: driver.execute_script("window.scrollBy(0, 700);"),
            lambda: driver.execute_script("window.scrollBy(0, 1000);"),
            lambda: driver.execute_script("window.scrollBy(0, 1500);"),

        ]
        
        # Random wait times between actions
        wait_times = [3,4,5,6,7,8,9,10,11,12,13,14,15]
        
        # Perform some random actions
        for _ in range(random.randint(2,4)):
            # Random scroll
            random.choice(scroll_actions)()
            time.sleep(random.choice(wait_times))
            
            # Occasionally interact with page elements
            if random.random() > 0.7:  # 30% chance to interact
                try:
                    # Try to find and click on home button or other common elements
                    elements = driver.find_elements(By.CSS_SELECTOR, "a[aria-label='Home']")
                    if elements:
                        random.choice(elements).click()
                        time.sleep(random.choice(wait_times))
                except:
                    pass
        
        # Scroll back to top
        driver.execute_script("window.scrollTo(0, 0);")
        time.sleep(random.choice(wait_times))
        
    except Exception as e:
        print(f"Error in human-like behavior simulation: {e}")

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
        
        # Check if already logged in
        if is_logged_in(driver):
            print("Already logged in to Facebook.")
            human_like_behavior(driver)
            return True
        
        # If not logged in, wait for manual login
        print("\n" + "="*50)
        print("Please log in to Facebook in the browser window that just opened.")
        print("This script will wait for 5 minutes for you to complete the login.")
        print("="*50 + "\n")
        
        # Wait for up to 5 minutes for login to complete
        login_timeout = 300  # 5 minutes in seconds
        start_time = time.time()
        logged_in = False
        
        while time.time() - start_time < login_timeout:
            if is_logged_in(driver):
                logged_in = True
                break
            time.sleep(random.randint(3,11))  # Check every 5 seconds
        
        if not logged_in:
            print("\nLogin timeout reached. Please make sure you're logged in.")
            return False
            
        print("\nSuccessfully logged in to Facebook!")
        
        # Simulate human-like behavior after login
        print("Simulating human-like behavior...")
        human_like_behavior(driver)
        
        return True
        
    except Exception as e:
        print(f"An error occurred in facebook_login: {e}")
        return False
