#!/usr/bin/env python3
"""
Setup script for Voice Sentiment Analyzer
"""

import subprocess
import sys
import os
from pathlib import Path


def install_requirements():
    """Install required packages"""
    print("Installing required packages...")
    try:
        subprocess.check_call(
            [sys.executable, "-m", "pip", "install", "-r", "requirements.txt"]
        )
        print("✅ Requirements installed successfully!")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ Error installing requirements: {e}")
        return False


def setup_directories():
    """Create necessary directories"""
    print("Setting up directories...")
    directories = ["data"]

    for directory in directories:
        Path(directory).mkdir(parents=True, exist_ok=True)
        print(f"✅ Created directory: {directory}")


def download_nltk_data():
    """Download required NLTK data for TextBlob"""
    print("Downloading NLTK data for TextBlob...")
    try:
        import nltk

        nltk.download("punkt", quiet=True)
        nltk.download("brown", quiet=True)
        print("✅ NLTK data downloaded successfully!")
        return True
    except Exception as e:
        print(f"⚠️  Warning: Could not download NLTK data: {e}")
        print("TextBlob may not work properly without this data.")
        return False


def test_imports():
    """Test if all required modules can be imported"""
    print("Testing imports...")

    required_modules = [
        "streamlit",
        "pandas",
        "plotly",
        "textblob",
        "vaderSentiment",
        "speech_recognition",
        "numpy",
    ]

    failed_imports = []

    for module in required_modules:
        try:
            __import__(module)
            print(f"✅ {module}")
        except ImportError as e:
            print(f"❌ {module}: {e}")
            failed_imports.append(module)

    return len(failed_imports) == 0


def main():
    """Main setup function"""
    print("🎤 Voice Sentiment Analyzer Setup")
    print("=" * 40)

    # Setup directories
    setup_directories()

    # Install requirements
    if not install_requirements():
        print("Setup failed. Please check the error messages above.")
        return False

    # Download NLTK data
    download_nltk_data()

    # Test imports
    if not test_imports():
        print("Some modules failed to import. Please check the installation.")
        return False

    print("\n🎉 Setup completed successfully!")
    print("\nTo run the application:")
    print("  streamlit run app.py")
    print("\nThen open your browser to: http://localhost:8501")

    return True


if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
