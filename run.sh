#!/bin/bash

# Voice Sentiment Analyzer Startup Script

echo "🎤 Starting Voice Sentiment Analyzer..."

# Check if virtual environment exists
if [ ! -d "venv" ]; then
    echo "Virtual environment not found. Creating one..."
    python3 -m venv venv
    
    echo "Installing dependencies..."
    source venv/bin/activate
    pip install -r requirements.txt
    
    echo "Downloading NLTK data..."
    python3 -c "import nltk; nltk.download('punkt', quiet=True); nltk.download('brown', quiet=True)"
fi

# Activate virtual environment
source venv/bin/activate

# Check if all dependencies are installed
echo "Checking dependencies..."
python3 -c "
try:
    from src.sentiment_analyzer import SentimentAnalyzer
    from src.product_catalog import ProductCatalog
    from src.data_manager import DataManager
    from src.audio_processor import AudioProcessor
    print('✅ All dependencies are ready!')
except ImportError as e:
    print(f'❌ Missing dependency: {e}')
    print('Please run: pip install -r requirements.txt')
    exit(1)
"

if [ $? -eq 0 ]; then
    echo "🚀 Starting Streamlit application..."
    echo "Open your browser to: http://localhost:8501"
    echo "Press Ctrl+C to stop the application"
    echo ""
    streamlit run app.py
else
    echo "❌ Failed to start application. Please check the error messages above."
fi