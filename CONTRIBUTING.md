# Contributing to Voice Sentiment Analyzer

Thank you for your interest in contributing to the Voice Sentiment Analyzer! This document provides guidelines for contributing to the project.

## Getting Started

1. **Fork the repository** on GitHub
2. **Clone your fork** locally:
   ```bash
   git clone https://github.com/your-username/voice-sentiment-analyzer.git
   cd voice-sentiment-analyzer
   ```
3. **Set up the development environment**:
   ```bash
   ./run.sh
   ```

## Development Setup

### Prerequisites

- Python 3.8 or higher
- Git

### Installation

1. Create a virtual environment:

   ```bash
   python3 -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

2. Install dependencies:

   ```bash
   pip install -r requirements.txt
   ```

3. Download NLTK data:
   ```bash
   python3 -c "import nltk; nltk.download('punkt'); nltk.download('brown')"
   ```

## Project Structure

```
voice-sentiment-analyzer/
├── app.py                 # Main Streamlit application
├── src/
│   ├── sentiment_analyzer.py  # Multi-model sentiment engine
│   ├── product_catalog.py     # Product management
│   ├── data_manager.py        # Database operations
│   └── audio_processor.py     # Speech-to-text processing
├── data/                  # Data storage directory
├── requirements.txt       # Python dependencies
├── run.sh                # Easy startup script
├── demo.py               # Command-line demo
└── setup.py              # Setup automation
```

## How to Contribute

### Reporting Issues

- Use the GitHub issue tracker
- Provide detailed information about the bug
- Include steps to reproduce the issue
- Mention your operating system and Python version

### Suggesting Features

- Open an issue with the "enhancement" label
- Describe the feature and its benefits
- Provide examples of how it would be used

### Code Contributions

1. **Create a new branch** for your feature:

   ```bash
   git checkout -b feature/your-feature-name
   ```

2. **Make your changes** following the coding standards below

3. **Test your changes**:

   ```bash
   python3 demo.py  # Test core functionality
   streamlit run app.py  # Test web interface
   ```

4. **Commit your changes**:

   ```bash
   git add .
   git commit -m "Add: brief description of your changes"
   ```

5. **Push to your fork**:

   ```bash
   git push origin feature/your-feature-name
   ```

6. **Create a Pull Request** on GitHub

## Coding Standards

### Python Style

- Follow PEP 8 guidelines
- Use meaningful variable and function names
- Add docstrings to all functions and classes
- Keep functions focused and small

### Code Organization

- Keep related functionality in appropriate modules
- Use type hints where possible
- Handle exceptions gracefully
- Add comments for complex logic

### Example Code Style

```python
def analyze_sentiment(self, text: str) -> dict:
    """
    Perform comprehensive sentiment analysis

    Args:
        text (str): Input text to analyze

    Returns:
        dict: Analysis results with scores and confidence
    """
    if not text or not text.strip():
        return self._empty_result()

    # Implementation here...
```

## Testing

### Running Tests

```bash
# Test core functionality
python3 demo.py

# Test web interface
streamlit run app.py
```

### Adding Tests

- Add test cases for new features
- Ensure existing functionality still works
- Test edge cases and error conditions

## Areas for Contribution

### High Priority

- [ ] Enhanced speech recognition accuracy
- [ ] Multi-language support
- [ ] Advanced ML models (transformer-based)
- [ ] Performance optimizations

### Medium Priority

- [ ] Additional visualization charts
- [ ] Export format options
- [ ] User authentication
- [ ] API endpoints

### Low Priority

- [ ] Mobile-responsive improvements
- [ ] Theme customization
- [ ] Advanced filtering options
- [ ] Batch processing features

## Documentation

- Update README.md for new features
- Add docstrings to new functions
- Update this CONTRIBUTING.md if needed
- Include examples in documentation

## Code Review Process

1. All contributions require a pull request
2. At least one maintainer review is required
3. All tests must pass
4. Code must follow the style guidelines
5. Documentation must be updated if needed

## Questions?

If you have questions about contributing, please:

- Check existing issues and discussions
- Open a new issue with the "question" label
- Reach out to the maintainers

Thank you for contributing to Voice Sentiment Analyzer! 🎤📊
