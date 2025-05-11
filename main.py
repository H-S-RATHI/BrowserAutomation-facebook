from selenium import webdriver
from browser_utils import create_or_use_persistent_profile
from facebook_login import main as facebook_login

def main():
    print("Starting main application...")
    
    # Create or use a persistent profile
    chrome_options = create_or_use_persistent_profile()
    
    # Run the Facebook login automation
    if chrome_options:
        facebook_login()
    else:
        print("Failed to initialize Chrome options. Exiting.")

if __name__ == "__main__":
    main()