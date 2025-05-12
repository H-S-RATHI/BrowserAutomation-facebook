# Facebook Automation Tool

A Python-based automation tool for managing Facebook posts, including creation, enhancement with AI, and automated posting to groups and profiles.

## Features

- **Post Creation**: Create and manage Facebook posts with text and images
- **AI Enhancement**: Improve post content using Google's Gemini AI
- **Automated Posting**: Schedule and automate posts to Facebook groups and profiles
- **Persistent Profile**: Maintains browser session for seamless automation
- **User-Friendly GUI**: Intuitive interface for post creation and management

## Prerequisites

- Python 3.7+
- Chrome browser installed
- Facebook account credentials
- Google Gemini API key (for AI enhancement)

## Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/H-S-RATHI/facebook-automation-tool.git
   cd facebook-automation-tool
   ```

2. Install the required packages:
   ```bash
   pip install -r requirements.txt
   ```

3. Configure your Gemini API key:
   - Get an API key from [Google AI Studio](https://aistudio.google.com/app/apikey)
   - Update the `GEMINI_API_KEY` in `gemini_config.py`

## Usage

### Running the Application

1. Start the post creator GUI:
   ```bash
   python post_creator_gui.py
   ```

2. To run the automation (login and post to groups):
   ```bash
   python main.py
   ```

### Creating Posts

1. Launch the Post Creator GUI
2. Enter your post content in the text area
3. Add images using the "Add Photos" button
4. Optionally enhance your post using the AI enhancement feature
5. Save the post to the posts directory

### Automated Posting

1. Update the `GROUP_LINKS` list in `visitgroup.py` with your target Facebook groups
2. Run `main.py` to start the automation
3. The script will:
   - Log in to Facebook (if not already logged in)
   - Visit each group in the list
   - Post your saved content
   - Move posted content to the 'already_posted' directory

## File Structure

```
facebook-automation-tool/
├── browser_utils.py     # Browser configuration and utilities
├── facebook_login.py    # Facebook login automation
├── gemini_config.py     # Gemini AI configuration
├── gemini_utils.py      # Gemini AI integration
├── main.py              # Main automation script
├── post_creator_gui.py  # Post creation interface
├── requirements.txt     # Python dependencies
└── visitgroup.py        # Group visiting and posting logic
```

## Configuration

- `gemini_config.py`: Configure your Gemini API key and model settings
- `visitgroup.py`: Update `GROUP_LINKS` with your target Facebook groups
- `browser_utils.py`: Modify browser settings and profile configuration

## Security Notes

- Never commit your Facebook credentials or API keys to version control
- The tool uses a persistent Chrome profile to maintain login state
- Be aware of Facebook's terms of service regarding automation

## Troubleshooting

- If login fails, check your internet connection and Facebook credentials
- For API key issues, verify your Gemini API key is correctly set
- Ensure all required Python packages are installed

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

---

*Disclaimer: This tool is for educational purposes only. Use it responsibly and in compliance with Facebook's Terms of Service.*
