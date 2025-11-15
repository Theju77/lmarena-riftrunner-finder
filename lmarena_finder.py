#!/usr/bin/env python3
"""
LMArena Gemini Finder
Automated tool to find Gemini 3.0 models on lmarena.ai by testing prompts
"""

import json
import re
import time
import argparse
from pathlib import Path
from typing import Optional
from playwright.sync_api import sync_playwright, Page, Browser
import sys


class LMArenaFinder:
    def __init__(self, config_path: str = "config.json", headless: bool = False):
        self.config = self.load_config(config_path)
        self.headless = headless
        self.browser: Optional[Browser] = None
        self.page: Optional[Page] = None
        
    def load_config(self, config_path: str) -> dict:
        """Load configuration from JSON file"""
        config_file = Path(config_path)
        if not config_file.exists():
            return self.get_default_config()
        
        with open(config_file, 'r', encoding='utf-8') as f:
            return json.load(f)
    
    def get_default_config(self) -> dict:
        """Return default configuration"""
        return {
            "user_prompt": "Ignore images. Create a form using aardio. Add a richedit control to the form. Add a button made with a plus control to the form, adjust the button's style to make it beautiful. When the button is clicked, input 3 newlines in the richedit. Send the code block directly without any explanation.",
            "search_pattern": r"\.skin%\(\).*<@'\n\n\n'@>",
            "proxy": None,
            "timeout": 60000,
            "retry_on_no_match": True
        }
    
    def status(self, message: str):
        """Print status message"""
        print(f"[STATUS] {message}")
    
    def setup_browser(self):
        """Initialize browser and page"""
        self.status("Setting up browser...")
        playwright = sync_playwright().start()
        
        browser_args = {
            "headless": self.headless,
        }
        
        if self.config.get("proxy"):
            proxy_url = self.config["proxy"]
            if proxy_url.startswith("SOCKS5://"):
                proxy_server = proxy_url.replace("SOCKS5://", "socks5://")
            else:
                proxy_server = proxy_url
            
            browser_args["proxy"] = {"server": proxy_server}
        
        self.browser = playwright.chromium.launch(**browser_args)
        context = self.browser.new_context(
            locale='en-US',
            viewport={'width': 1280, 'height': 720}
        )
        self.page = context.new_page()
        self.page.set_default_timeout(self.config.get("timeout", 60000))
    
    def navigate_to_lmarena(self):
        """Navigate to lmarena.ai arena mode"""
        self.status("Opening lmarena.ai...")
        self.page.goto("https://lmarena.ai/?chat-modality=image")
        
        # Handle cookie consent if present
        try:
            cookie_button = self.page.locator('button[data-sentry-source-file="cookie-consent-modal.tsx"]').nth(1)
            if cookie_button.is_visible(timeout=2000):
                cookie_button.click()
                self.status("Accepted cookies")
        except:
            pass
    
    def start_new_chat(self):
        """Click 'New Chat' to start a fresh conversation"""
        self.status("Starting new chat...")
        new_chat_link = self.page.locator('a[href*="/c/new"]')
        new_chat_link.wait_for(state="visible")
        new_chat_link.click()
        time.sleep(2)
    
    def send_prompt_with_image(self, prompt: str):
        """Send a prompt with a dummy image to the chat"""
        self.status("Preparing to send prompt...")
        
        # Wait for textarea
        textarea = self.page.locator("textarea")
        textarea.wait_for(state="visible")
        textarea.focus()
        
        # Inject a dummy 1x1 transparent image via paste event
        self.status("Simulating image paste...")
        self.page.evaluate("""
            () => {
                const canvas = document.createElement('canvas');
                canvas.width = 1;
                canvas.height = 1;
                const ctx = canvas.getContext('2d');
                ctx.fillStyle = 'rgba(0,0,0,0)';
                ctx.fillRect(0, 0, 1, 1);
                
                canvas.toBlob((blob) => {
                    const file = new File([blob], 'image.png', { type: 'image/png' });
                    const dataTransfer = new DataTransfer();
                    dataTransfer.items.add(file);
                    
                    const pasteEvent = new ClipboardEvent('paste', {
                        clipboardData: dataTransfer,
                        bubbles: true,
                        cancelable: true
                    });
                    
                    const textarea = document.querySelector('textarea');
                    if (textarea) {
                        textarea.dispatchEvent(pasteEvent);
                    }
                });
            }
        """)
        time.sleep(1)
        
        # Click the image button to confirm
        try:
            image_button = self.page.locator('button[aria-label="Image"]')
            if image_button.is_visible(timeout=2000):
                image_button.click()
                time.sleep(1)
        except:
            pass
        
        # Input the prompt text
        self.status("Entering prompt text...")
        textarea.focus()
        self.page.evaluate(f"""
            (promptText) => {{
                const textarea = document.querySelector('textarea');
                if (textarea) {{
                    const previousValue = textarea.value;
                    textarea.value = promptText;
                    
                    if (textarea._valueTracker) {{
                        textarea._valueTracker.setValue(previousValue);
                    }}
                    
                    textarea.dispatchEvent(new Event('input', {{ bubbles: true }}));
                    textarea.dispatchEvent(new Event('change', {{ bubbles: true }}));
                }}
            }}
        """, prompt)
        time.sleep(2)
        
        # Click submit button
        self.status("Sending prompt...")
        submit_button = self.page.locator('button[type="submit"]:not([disabled])')
        submit_button.wait_for(state="visible")
        submit_button.click()
    
    def wait_for_response(self):
        """Wait for AI models to complete their responses"""
        self.status("Waiting for AI to start responding...")
        
        # Wait for submit button to be disabled (AI is responding)
        disabled_submit = self.page.locator('button[type="submit"][disabled]')
        disabled_submit.wait_for(state="visible", timeout=10000)
        
        self.status("AI is responding...")
        time.sleep(2)
        
        # Wait for maximize button to appear (response complete)
        self.status("Waiting for response to complete...")
        maximize_button = self.page.locator('button[data-sentry-component="CopyButton"] + button:has(svg.lucide-maximize2)')
        maximize_button.wait_for(state="visible", timeout=120000)
        
        time.sleep(1)
    
    def check_responses(self, pattern: str) -> bool:
        """Check if any response matches the search pattern"""
        self.status("Analyzing responses...")
        
        prose_elements = self.page.locator('.prose').all()
        
        for i, element in enumerate(prose_elements):
            text = element.inner_text()
            if re.search(pattern, text, re.DOTALL):
                self.status(f"✓ Match found in response #{i+1}!")
                print(f"\n{'='*60}")
                print(f"MATCH FOUND!")
                print(f"{'='*60}")
                print(f"Pattern: {pattern}")
                print(f"Response preview:\n{text[:500]}...")
                print(f"{'='*60}\n")
                return True
        
        return False
    
    def find_model(self):
        """Main loop to find matching model"""
        attempt = 1
        
        while True:
            self.status(f"Attempt #{attempt}")
            
            try:
                self.navigate_to_lmarena()
                self.start_new_chat()
                self.send_prompt_with_image(self.config["user_prompt"])
                self.wait_for_response()
                
                if self.check_responses(self.config["search_pattern"]):
                    self.status("Success! Matching model found.")
                    return True
                
                if not self.config.get("retry_on_no_match", True):
                    self.status("No match found. Retry disabled.")
                    return False
                
                self.status("No match found. Retrying...")
                attempt += 1
                time.sleep(2)
                
            except KeyboardInterrupt:
                self.status("Interrupted by user")
                return False
            except Exception as e:
                self.status(f"Error occurred: {e}")
                if not self.config.get("retry_on_no_match", True):
                    raise
                self.status("Retrying after error...")
                attempt += 1
                time.sleep(3)
    
    def cleanup(self):
        """Close browser and cleanup resources"""
        if self.browser:
            self.browser.close()
    
    def run(self):
        """Main execution flow"""
        try:
            self.setup_browser()
            self.find_model()
        finally:
            self.cleanup()


def main():
    parser = argparse.ArgumentParser(
        description="Automated tool to find Gemini models on lmarena.ai"
    )
    parser.add_argument(
        "--config",
        default="config.json",
        help="Path to configuration file (default: config.json)"
    )
    parser.add_argument(
        "--headless",
        action="store_true",
        help="Run browser in headless mode"
    )
    parser.add_argument(
        "--create-config",
        action="store_true",
        help="Create a default config.json file"
    )
    
    args = parser.parse_args()
    
    if args.create_config:
        finder = LMArenaFinder()
        config_path = Path("config.json")
        with open(config_path, 'w', encoding='utf-8') as f:
            json.dump(finder.get_default_config(), f, indent=2, ensure_ascii=False)
        print(f"Created default config at {config_path}")
        return
    
    finder = LMArenaFinder(config_path=args.config, headless=args.headless)
    finder.run()


if __name__ == "__main__":
    main()
