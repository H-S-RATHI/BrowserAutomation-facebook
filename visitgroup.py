from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import TimeoutException, NoSuchElementException, ElementClickInterceptedException
import time
import os
import json
import base64
import random
from selenium.webdriver.common.action_chains import ActionChains
from datetime import datetime


# List of Facebook group URLs to visit
GROUP_LINKS = [
    "https://www.facebook.com/groups/242194011192582",
    "https://www.facebook.com/groups/brahmacharyafsr",
    "https://www.facebook.com/groups/581147559939258"
    # Add more group links here as needed
]


def get_latest_post():
    """Get the latest post from the posts directory"""
    posts_dir = os.path.join(os.path.dirname(__file__), 'posts')
    if not os.path.exists(posts_dir):
        print("No posts directory found!")
        return None
    
    # Get all JSON files in posts directory
    post_files = [f for f in os.listdir(posts_dir) if f.endswith('.json')]
    if not post_files:
        print("No post files found!")
        return None
    
    # Sort by creation time (newest first)
    post_files.sort(key=lambda x: os.path.getmtime(os.path.join(posts_dir, x)), reverse=True)
    latest_post = post_files[0]
    
    # Load the post data
    with open(os.path.join(posts_dir, latest_post), 'r', encoding='utf-8') as f:
        post_data = json.load(f)
    
    print(f"Loaded post: {latest_post}")
    return post_data

def post_to_group(driver, post_data):
    """Post content to the current group"""
    try:
        wait = WebDriverWait(driver, 20)
        
        # Click on the main post box to open the post form
        post_box = wait.until(EC.element_to_be_clickable(
            (By.CLASS_NAME, "x6s0dn4.x78zum5.x1l90r2v.x1pi30zi.x1swvt13.xz9dl7a")
        ))
        post_box.click()
        print("Clicked on post box")
        time.sleep(random.uniform(3, 7))  # Wait for post form to appear
        
        # Find the description input field and type the post content
        try:
            # Use the working XPath selector
            try:
                desc_input = wait.until(EC.presence_of_element_located(
                    (By.XPATH, "//div[@role='dialog']//div[@role='textbox' and @contenteditable='true']")
                ))
                print("Found description field")
            except Exception as e:
                print(f"Could not find description field: {str(e)}")
                driver.save_screenshot("debug_description_field.png")
                print("Screenshot saved as debug_description_field.png")
                return False
            
            # Clean and prepare the description text (only BMP characters)
            cleaned_description = ''.join(
                char for char in post_data['description'] 
                if ord(char) <= 0xFFFF  # Only include BMP characters
            )
            
            try:
                # Focus and clear the field
                desc_input.click()
                time.sleep(random.uniform(1, 7))
                desc_input.clear()
                time.sleep(random.uniform(1, 7))
                
                # Type character by character with small delay
                for char in cleaned_description:
                    desc_input.send_keys(char)
                    time.sleep(0.03)  # Slightly faster typing speed
                
                print("Description entered successfully")
                
            except Exception as e:
                print(f"Failed to enter description: {str(e)}")
                return False
            
            print("Typed description using JavaScript")
            time.sleep(random.uniform(2, 7))
            
            # Handle photos by pasting them directly into the post
            photos_to_process = []
            
            # Check for photos in both formats
            if 'photos_data' in post_data and post_data['photos_data']:
                print(f"Found {len(post_data['photos_data'])} embedded photos to process")
                # Create temporary files from embedded photos
                import tempfile
                temp_dir = os.path.join(tempfile.gettempdir(), 'fb_temp_photos')
                os.makedirs(temp_dir, exist_ok=True)
                
                for i, photo_data in enumerate(post_data['photos_data']):
                    try:
                        file_path = os.path.join(temp_dir, f"temp_photo_{i}.jpg")
                        with open(file_path, 'wb') as f:
                            f.write(base64.b64decode(photo_data['data']))
                        photos_to_process.append(file_path)
                    except Exception as e:
                        print(f"Error processing embedded photo: {str(e)}")
        
            
            if photos_to_process:
                print(f"Total photos to process: {len(photos_to_process)}")
                try:
                    # Click to focus the post box again
                    print("Focusing post box...")
                    desc_input.click()
                    time.sleep(random.uniform(1, 7))
                    
                    # Import required modules
                    from selenium.webdriver.common.keys import Keys
                    
                    # Press Enter to create a new line before pasting photos
                    print("Adding new line for photos...")
                    desc_input.send_keys(Keys.ENTER)
                    time.sleep(random.uniform(1, 7))
                    
                    # Paste each photo
                    for i, photo_path in enumerate(photos_to_process, 1):
                        try:
                            print(f"\nProcessing photo {i}/{len(post_data['photos'])}: {photo_path}")
                            
                            if not os.path.exists(photo_path):
                                print(f"Photo not found: {photo_path}")
                                continue
                                
                            print("Opening image...")
                            from PIL import Image
                            from io import BytesIO
                            
                            # Load and prepare image
                            image = Image.open(photo_path)
                            print(f"Image format: {image.format}, size: {image.size}")
                            
                            # Convert to RGB if needed
                            if image.mode != 'RGB':
                                print(f"Converting image from {image.mode} to RGB...")
                                image = image.convert('RGB')
                            
                            # Save to BMP in memory
                            output = BytesIO()
                            image.save(output, format='BMP')
                            data = output.getvalue()[14:]  # Remove BMP header
                            output.close()
                            
                            print("Copying to clipboard...")
                            import win32clipboard
                            win32clipboard.OpenClipboard()
                            win32clipboard.EmptyClipboard()
                            win32clipboard.SetClipboardData(win32clipboard.CF_DIB, data)
                            win32clipboard.CloseClipboard()
                            
                            print("Pasting image...")
                            desc_input.send_keys(Keys.CONTROL + 'v')
                            print(f"Pasted photo: {os.path.basename(photo_path)}")
                            
                            # Add space between photos (except after last photo)
                            if i < len(post_data['photos']):
                                desc_input.send_keys(Keys.ENTER)
                            
                            time.sleep(random.uniform(2, 7))  # Wait for image to process
                            
                        except Exception as img_error:
                            print(f"Error pasting photo {photo_path}: {str(img_error)}")
                            import traceback
                            traceback.print_exc()
                    
                except Exception as e:
                    print(f"Error in photo handling: {str(e)}")
                    import traceback
                    traceback.print_exc()
                    driver.save_screenshot("photo_paste_error.png")
                    return False
            else:
                print("No photos to paste")
            
        except Exception as e:
            print(f"Error with description field: {str(e)}")
            # Take a screenshot to help debug
            driver.save_screenshot("description_error.png")
            print("Screenshot saved as description_error.png")
            return False
        
        # Click the post button
        try:
            post_btn = wait.until(EC.element_to_be_clickable(
                (By.XPATH, "//div[@role='button' and contains(., 'Post')]")
            ))
            post_btn.click()
            print("Clicked post button")
            time.sleep(random.uniform(5, 11))  # Wait for post to complete
            return True
            
        except Exception as e:
            print(f"Could not find post button: {str(e)}")
            return False
        
    except Exception as e:
        print(f"Error posting to group: {str(e)}")
        return False

def visit_groups(driver, group_links=None):
    """
    Navigate to Facebook Groups and post content to each group
    
    Args:
        driver: An initialized WebDriver instance
        group_links: List of Facebook group URLs to visit (optional, will use default if not provided)
    """
    try:
        print("Starting Facebook Groups automation...")
        
        # Load the post to share
        post_data = get_latest_post()
        if not post_data:
            print("No post data found to share!")
            return
            
        print(f"Will post: {post_data['description'][:50]}...")
        if post_data.get('photos'):
            print(f"With {len(post_data['photos'])} photos")
        
        # Use provided group_links or default to GROUP_LINKS
        groups_to_visit = group_links if group_links else GROUP_LINKS
        
        # Navigate to Facebook if not already there
        if "facebook.com" not in driver.current_url:
            print("Navigating to Facebook...")
            driver.get("https://www.facebook.com/")
            time.sleep(5)  # Wait for the page to load
        
        print("Looking for Groups link...")
        
        # Dictionary to store group URL and its count

        
        # Visit each group in the list
        for i, group_url in enumerate(groups_to_visit, 1):
            try:
                print(f"\n--- Processing group {i} of {len(groups_to_visit)} ---")
                print(f"URL: {group_url}")
                
                # Navigate to the group
                driver.get(group_url)
                
                # Human-like behavior after page load
                print("Simulating human-like behavior...")
                
                # Random wait to mimic human reading/processing time
                time.sleep(random.uniform(3, 11))
                
                # Random scrolling behavior
                scroll_actions = [
                    lambda: driver.execute_script("window.scrollBy(0, 500);"),
                    lambda: driver.execute_script("window.scrollBy(0, 800);"),
                    lambda: driver.execute_script("window.scrollBy(0, 300);"),
                    lambda: driver.execute_script("window.scrollBy(0, 1000);"),
                ]
                
                # Perform 2-4 random scrolls
                for _ in range(random.randint(2, 7)):
                    random.choice(scroll_actions)()
                    time.sleep(random.uniform(1, 11))  # Random pause between scrolls
                    
                
                
                # Scroll back to top
                driver.execute_script("window.scrollTo(0, 200);")
                time.sleep(random.uniform(1, 11))
                
                # Check if we're in the group (not redirected to login or error page)
                if "groups/join" in driver.current_url or "login" in driver.current_url:
                    print("Not a member of this group or login required. Skipping...")
                    continue
                
                # Try to post to the group
                print("Attempting to post...")
                if post_to_group(driver, post_data):
                    print(f"Successfully posted to group {i}")
                else:
                    print(f"Failed to post to group {i}")
                
                # Random delay between posts (30-90 seconds) to avoid detection
                delay = random.uniform(30, 90)
                print(f"Waiting for {delay} seconds before next post...")
                time.sleep(delay)
                
            except Exception as group_error:
                error_msg = str(group_error)
                print(f"Error processing group {group_url}: {error_msg}")
                
                # Take a screenshot on error
                try:
                    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                    screenshot_path = f"error_group_{i}_{timestamp}.png"
                    driver.save_screenshot(screenshot_path)
                    print(f"Screenshot saved as {screenshot_path}")
                except:
                    print("Could not save screenshot")
                
                # Random delay before next attempt
                time.sleep(random.uniform(10, 30))
                continue  # Continue with the next group if there's an error
        
        
    except Exception as e:
        print(f"An error occurred in visit_groups: {e}")
        raise  # Re-raise the exception to be handled by the calling function
