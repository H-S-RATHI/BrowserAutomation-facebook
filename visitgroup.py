from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
import time


# List of Facebook group URLs to visit
GROUP_LINKS = [
    "https://www.facebook.com/groups/242194011192582",
    "https://www.facebook.com/groups/brahmacharyafsr",
    "https://www.facebook.com/groups/581147559939258"
    # Add more group links here as needed
]


def visit_groups(driver, group_links=None):
    """
    Navigate to Facebook Groups, visit each group, and count specific elements.
    
    Args:
        driver: An initialized WebDriver instance
        group_links: List of Facebook group URLs to visit (optional, will use default if not provided)
    """
    try:
        print("Starting Facebook Groups automation...")
        
        # Use provided group_links or default to GROUP_LINKS
        groups_to_visit = group_links if group_links else GROUP_LINKS
        
        # Navigate to Facebook if not already there
        if "facebook.com" not in driver.current_url:
            print("Navigating to Facebook...")
            driver.get("https://www.facebook.com/")
            time.sleep(3)  # Wait for the page to load
        
        print("Looking for Groups link...")
        
        # Wait for the Groups link to be clickable
        wait = WebDriverWait(driver, 30)
        groups_link = wait.until(EC.element_to_be_clickable(
            (By.XPATH, "//span[contains(text(),'Groups')]")
        ))
        
        print("Clicking on Groups...")
        groups_link.click()
        time.sleep(3)  # Wait for groups page to load
        
        print("Successfully navigated to Groups.")
        
        # Dictionary to store group URL and its count

        
        # Visit each group in the list
        for i, group_url in enumerate(groups_to_visit, 1):
            try:
                print(f"\nVisiting group {i} of {len(groups_to_visit)}: {group_url}")
                
                # Navigate to the group
                driver.get(group_url)
                
                # Wait for the group page to load
                time.sleep(5)  # Wait for 5 seconds on the page
                
                # Count the specific element
                
            except Exception as group_error:
                error_msg = str(group_error)
                print(f"Error visiting {group_url}: {error_msg}")
   
                continue  # Continue with the next group if there's an error
        
        
    except Exception as e:
        print(f"An error occurred in visit_groups: {e}")
        raise  # Re-raise the exception to be handled by the calling function
