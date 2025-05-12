import time
import random
import os
import json
import base64
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import TimeoutException, NoSuchElementException, ElementClickInterceptedException

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
        driver.execute_script("window.scrollTo(0, 20);")
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
            # Post to main profile after successful login
            post_to_profile(driver)
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

def post_to_profile(driver):
    """
    Post content to the user's main profile
    
    Args:
        driver: An initialized WebDriver instance
    """
    try:
        print("\nPreparing to post to main profile...")
        wait = WebDriverWait(driver, 20)
        
        # Get the latest post data
        post_data = get_latest_post()
        if not post_data:
            print("No post data found to share on profile!")
            return False
            
        print(f"Will post to profile: {post_data['description'][:50]}...")

        # Click on the post box
        post_box = wait.until(EC.element_to_be_clickable(
            (By.XPATH,
             "//div[@role='button' and contains(., \"What's on your mind\")]"
            )
        ))

        post_box.click()
        print("Clicked on post box")
        time.sleep(random.uniform(2, 5))
        
        # Find the post input field
        try:
            post_input = wait.until(EC.presence_of_element_located(
                (By.XPATH, "//div[@role='dialog']//div[@role='textbox' and @contenteditable='true']")
            ))
            
            # Clean and prepare the description text
            cleaned_description = ''.join(
                char for char in post_data['description'] 
                if ord(char) <= 0xFFFF  # Only include BMP characters
            )
            
            # Type the post content
            post_input.click()
            time.sleep(random.uniform(1, 3))
            post_input.clear()
            time.sleep(random.uniform(1, 3))
            
            # Type character by character with small delay
            for char in cleaned_description:
                post_input.send_keys(char)
                time.sleep(0.03)  # Slightly faster typing speed
            
            print("Description entered successfully")
            time.sleep(random.uniform(2, 5))
            
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
                    post_input.click()
                    time.sleep(random.uniform(1, 7))
                    
                    # Import required modules
                    from selenium.webdriver.common.keys import Keys
                    
                    # Press Enter to create a new line before pasting photos
                    print("Adding new line for photos...")
                    post_input.send_keys(Keys.ENTER)
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
                            post_input.send_keys(Keys.CONTROL + 'v')
                            print(f"Pasted photo: {os.path.basename(photo_path)}")
                            
                            # Add space between photos (except after last photo)
                            if i < len(post_data['photos']):
                                post_input.send_keys(Keys.ENTER)
                            
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
            
            # Click post button
            post_btn = wait.until(EC.element_to_be_clickable(
                (By.XPATH, "//div[@role='button']//span[text()='Post']")
            ))
            post_btn.click()
            print("Post published successfully!")
            time.sleep(random.uniform(5, 10))
            
            return True
            
        except Exception as e:
            print(f"Error while creating post: {str(e)}")
            return False
            
    except Exception as e:
        print(f"Error in post_to_profile: {str(e)}")
        return False
