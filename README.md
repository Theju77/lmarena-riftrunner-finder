# LMArena Gemini Finder

Automated Python tool to identify Gemini 3.0 models on [lmarena.ai](https://lmarena.ai) by testing specific prompts and analyzing responses.

## 🎯 Purpose

This tool automates the process of finding specific AI models (particularly Gemini 3.0) on LMArena's blind testing platform by:
- Submitting custom prompts with images
- Analyzing AI responses for specific patterns
- Automatically retrying until a match is found
- Supporting proxy configurations for network access

## ✨ Features

- **Web Automation**: Uses Playwright to automate browser interactions
- **Pattern Matching**: Regex-based response analysis to identify target models
- **Auto-retry**: Continues testing until the target model is found
- **Proxy Support**: Compatible with SOCKS5 proxies for network routing
- **Configurable**: JSON-based configuration for prompts and patterns
- **Headless Mode**: Can run without visible browser window
- **Status Updates**: Real-time progress reporting

## 📋 Requirements

- Python 3.8+
- macOS, Linux, or Windows
- Internet connection (proxy optional)

## 🚀 Quick Start

### 1. Install Dependencies

```bash
# Install Python packages
pip install -r requirements.txt

# Install Playwright browsers
python -m playwright install chromium
```

### 2. Configure

Edit `config.json` to customize your search:

```json
{
  "user_prompt": "Your custom prompt here",
  "search_pattern": "regex pattern to match",
  "proxy": null,
  "timeout": 60000,
  "retry_on_no_match": true
}
```

**Configuration Options:**
- `user_prompt`: The prompt to send to AI models
- `search_pattern`: Regex pattern to identify target model responses
- `proxy`: Proxy URL (e.g., `"socks5://127.0.0.1:1080"`) or `null`
- `timeout`: Maximum wait time in milliseconds (default: 60000)
- `retry_on_no_match`: Continue retrying if no match found (default: true)

### 3. Run

```bash
# Run with visible browser
python lmarena_finder.py

# Run in headless mode
python lmarena_finder.py --headless

# Use custom config file
python lmarena_finder.py --config my_config.json

# Generate default config file
python lmarena_finder.py --create-config
```

## 📖 How It Works

1. **Initialize**: Opens a browser and navigates to lmarena.ai
2. **Setup Chat**: Starts a new chat session in arena mode
3. **Send Prompt**: Submits your custom prompt with a dummy image
4. **Wait for Response**: Monitors the page until AI models complete their responses
5. **Analyze**: Checks responses against your search pattern using regex
6. **Match or Retry**: If found, reports success; otherwise, starts over

## 🔧 Advanced Usage

### Proxy Configuration

To use a SOCKS5 proxy (e.g., for network routing):

```json
{
  "proxy": "socks5://127.0.0.1:1080"
}
```

The tool automatically detects and converts `SOCKS5://` format to `socks5://`.

### Custom Patterns

The search pattern uses Python regex. Escape special characters:

```json
{
  "search_pattern": "\\.skin%\\(\\).*<@'\\n\\n\\n'@>"
}
```

### Timeout Adjustment

For slower connections or complex prompts:

```json
{
  "timeout": 120000
}
```

## 🛠️ Development

### Project Structure

```
lmarena-gemini-finder/
├── lmarena_finder.py   # Main application
├── config.json         # Configuration file
├── requirements.txt    # Python dependencies
├── README.md          # Documentation
└── setup.sh           # Setup script
```

### Key Components

- `LMArenaFinder`: Main class orchestrating the automation
- `setup_browser()`: Initializes Playwright browser with config
- `send_prompt_with_image()`: Injects dummy image and sends prompt
- `check_responses()`: Pattern matching against AI responses
- `find_model()`: Main retry loop

## ⚠️ Notes

- **Rate Limiting**: Be mindful of lmarena.ai's usage policies
- **Network**: Ensure stable internet connection for best results
- **Browser**: Chromium is used by default (installed via Playwright)
- **Session State**: Each retry starts a fresh chat session

## 🐛 Troubleshooting

**Browser doesn't open:**
```bash
python -m playwright install chromium
```

**Timeout errors:**
- Increase `timeout` in config.json
- Check internet connection
- Try without proxy

**No matches found:**
- Verify your search pattern is correct
- Check that the prompt generates expected responses
- Review lmarena.ai's current model availability

## 📝 Example Output

```
[STATUS] Setting up browser...
[STATUS] Opening lmarena.ai...
[STATUS] Starting new chat...
[STATUS] Preparing to send prompt...
[STATUS] Simulating image paste...
[STATUS] Entering prompt text...
[STATUS] Sending prompt...
[STATUS] Waiting for AI to start responding...
[STATUS] AI is responding...
[STATUS] Waiting for response to complete...
[STATUS] Analyzing responses...
[STATUS] ✓ Match found in response #2!

============================================================
MATCH FOUND!
============================================================
Pattern: \.skin%\(\).*<@'\n\n\n'@>
Response preview:
[Response content...]
============================================================

[STATUS] Success! Matching model found.
```

## 📄 License

MIT License - see LICENSE file for details

## 🤝 Contributing

Contributions welcome! Feel free to:
- Report bugs
- Suggest features
- Submit pull requests

---

**Note**: This tool is for educational and research purposes. Respect lmarena.ai's terms of service and rate limits.
