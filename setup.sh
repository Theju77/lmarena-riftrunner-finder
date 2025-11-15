#!/bin/bash
# Setup script for LMArena Gemini Finder

echo "🚀 Setting up LMArena Gemini Finder..."

# Check if Python 3 is installed
if ! command -v python3 &> /dev/null; then
    echo "❌ Python 3 is not installed. Please install Python 3.8 or higher."
    exit 1
fi

echo "✓ Python 3 found: $(python3 --version)"

# Create virtual environment if it doesn't exist
if [ ! -d "venv" ]; then
    echo "📦 Creating virtual environment..."
    python3 -m venv venv
fi

# Activate virtual environment
echo "🔌 Activating virtual environment..."
source venv/bin/activate

# Upgrade pip
echo "⬆️  Upgrading pip..."
pip install --upgrade pip

# Install requirements
echo "📥 Installing Python dependencies..."
pip install -r requirements.txt

# Install Playwright browsers
echo "🌐 Installing Playwright browsers (Chromium)..."
python -m playwright install chromium

# Make the main script executable
chmod +x lmarena_finder.py

echo ""
echo "✅ Setup complete!"
echo ""
echo "To get started:"
echo "  1. Activate the virtual environment: source venv/bin/activate"
echo "  2. Edit config.json to customize your search"
echo "  3. Run the tool: python lmarena_finder.py"
echo ""
echo "For more information, see README.md"
