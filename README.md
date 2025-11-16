# LMArena Riftrunner Finder - AI Model Detection & Identification Tool

[![Python](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Selenium](https://img.shields.io/badge/selenium-automation-green.svg)](https://www.selenium.dev/)

**Automated AI Model Fingerprinting & Detection Tool** - Python-based web scraper to identify anonymous LLM models on [lmarena.ai](https://lmarena.ai) blind testing platform. Specifically designed to detect the **"riftrunner"** anonymous model through response pattern analysis.

If you’re looking for the anonymous LMArena checkpoint codenamed **"riftrunner"** – the model many in the community believe to be a **Gemini 3.0 Pro** release-candidate – this tool automates the process of finding it on lmarena.ai’s blind testing platform.

In this repository, any mentions of **"Gemini 3"** or **"Gemini 3 Pro"** are just shorthand for this anonymous LMArena model (`riftrunner`), not for any officially released Google Gemini 3 product. Some community posts also refer to it as **"Rift Runner"**, which this README treats as the same model.

🔍 **Keywords**: LMArena, AI model detection, Gemini 3.0 Pro RC finder, LLM fingerprinting, anonymous model identification, chatbot arena, AI benchmarking tool, model comparison automation, riftrunner, Rift Runner

The "riftrunner" model is widely speculated within the AI research community to be an unreleased Gemini 3.0 variant based on behavioral analysis and response patterns.

> **Acknowledgment:** This project is inspired by and based on the fingerprinting technique shared by [Jacen He](https://mp.weixin.qq.com/s?mid=2650934479&sn=fbba9e154fed1d2c128814d2ad546fb4&idx=1&__biz=MzA3Njc1MDU0OQ%3D%3D) from the aardio community. This Python implementation adapts their original approach using Selenium and Chrome automation.

## ⚠️ Important Disclaimer

> Terminology note: throughout this README, **"Gemini 3"** / **"Gemini 3 Pro"** always refer to the anonymous LMArena model codenamed `riftrunner`, as speculated by the community – not to any officially released Google product.

**Target Model Clarification:** This tool is designed to identify the anonymous model codenamed **"riftrunner"** on LMArena's blind testing platform. This model has been widely speculated to be an unreleased Gemini 3.0 variant within the AI community.

**This tool does NOT target:**
- Any officially released Google Gemini models (Gemini 1.0, Gemini 1.5, Gemini 2.0, etc.)
- Any publicly announced or documented Gemini 3.x series models
- Any production Google AI models

**Please note:** The connection between "riftrunner" and any specific Google model is based on community speculation and behavioral fingerprinting patterns. This tool is for research and educational purposes only. Users should make their own informed decisions about model identity based on response characteristics.

## 🎯 Purpose

This tool automates the process of finding the **"riftrunner"** anonymous model on LMArena's blind testing platform by:
- Submitting custom prompts with images
- Analyzing AI responses for specific fingerprint patterns
- Automatically retrying until a match is found
- Supporting proxy configurations for network access

## ✨ Features

- **Web Automation**: Uses undetected-chromedriver with real Chrome for reliable automation
- **Cloudflare Bypass**: Automatically bypasses bot detection and verification
- **Persistent Sessions**: Saves Chrome profile - faster on subsequent runs
- **Smart Pattern Matching**: Flexible regex that catches riftrunner's unique response patterns
- **Error Detection**: Automatically detects and retries generation errors
- **Model Identification**: Clearly shows which model (A or B) is riftrunner
- **Interactive Mode**: Browser stays open after finding model for testing
- **Auto-retry**: Continues testing until the target model is found
- **Proxy Support**: Compatible with SOCKS5 proxies for network routing
- **Configurable**: JSON-based configuration for prompts and patterns
- **Timestamped Logs**: All status messages include timestamps for debugging
- **Robust Text Extraction**: Uses textContent for reliable code capture

## 📋 Requirements

- Python 3.8+
- Google Chrome browser (installed on your system)
- macOS, Linux, or Windows
- Internet connection (proxy optional)

## 🚀 Quick Start

### 1. Clone the Repository

```bash
git clone https://github.com/aezizhu/lmarena-riftrunner-finder.git
cd lmarena-riftrunner-finder
```

### 2. Install Dependencies

```bash
# Install Python packages
pip install -r requirements.txt

# Note: Chrome browser must be installed on your system
# On macOS: brew install --cask google-chrome
# Or download from: https://www.google.com/chrome/
```

### 3. Configuration

The `config.json` file contains a **fixed prompt and search pattern** specifically designed to identify the "riftrunner" model. These values are tuned to find specific fingerprint characteristics in model responses and **should not be modified**.

**Optional Configuration:**
You can adjust these settings in `config.json` if needed:

- `proxy`: Proxy URL (e.g., `"socks5://127.0.0.1:1080"`) or `null` for direct connection
- `timeout`: Maximum wait time in milliseconds (default: 60000)
- `retry_on_no_match`: Continue retrying until match found (default: true)

**Note:** The `user_prompt` and `search_pattern` fields use a specialized fingerprinting technique to reliably identify target models. Changing these values will prevent the tool from working correctly.

### 4. Run

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
lmarena-riftrunner-finder/
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
- **Browser**: Uses your installed Google Chrome browser
- **Session State**: Each retry starts a fresh chat session

## 🐛 Troubleshooting

**Browser doesn't open:**
- Ensure Google Chrome is installed on your system
- Check that ChromeDriver can be downloaded (webdriver-manager handles this automatically)

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

## 🙏 Acknowledgments

This project was inspired by and developed based on techniques described in [this article](https://mp.weixin.qq.com/s?mid=2650934479&sn=fbba9e154fed1d2c128814d2ad546fb4&idx=1&__biz=MzA3Njc1MDU0OQ%3D%3D). Special thanks to the original author for sharing the aardio implementation and the clever fingerprinting technique.

## 📄 License

MIT License - see LICENSE file for details

## 🤝 Contributing

Contributions welcome! Feel free to:
- Report bugs
- Suggest features
- Submit pull requests

---

## 🔍 Related Topics & Use Cases

**AI Model Research:**
- LLM benchmarking and evaluation
- Anonymous model identification on chatbot arena platforms
- AI model fingerprinting techniques
- Gemini model detection and analysis

**Automation & Scraping:**
- Selenium web automation for AI platforms
- Browser automation with Chrome/ChromeDriver
- Cloudflare bypass techniques
- Pattern matching and response analysis

**Research Applications:**
- Comparative LLM analysis
- Model behavior profiling
- AI capability testing
- Blind testing automation

## 🏷️ Tags

`lmarena` `ai-model-detection` `gemini-finder` `llm-fingerprinting` `chatbot-arena` `selenium-automation` `web-scraping` `ai-research` `model-identification` `python-automation` `gemini-3` `riftrunner` `ai-benchmarking` `model-testing` `chrome-automation`

---

**Note**: This tool is for educational and research purposes. Respect lmarena.ai's terms of service and rate limits.
