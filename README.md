# 🎤 Voice Sentiment Analyzer

[![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)](https://www.python.org/downloads/)
[![Streamlit](https://img.shields.io/badge/Streamlit-1.28+-red.svg)](https://streamlit.io/)
[![License](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)
[![PRs Welcome](https://img.shields.io/badge/PRs-welcome-brightgreen.svg)](CONTRIBUTING.md)

A comprehensive web-based application for analyzing customer sentiment from both voice recordings and text input for e-commerce product feedback. Built with advanced NLP models and real-time analytics.

![Voice Sentiment Analyzer Demo](https://via.placeholder.com/800x400/007bff/ffffff?text=Voice+Sentiment+Analyzer+Demo)

## 🌟 Key Features

- 🎤 **Multi-Modal Input**: Support for both voice recordings and text feedback
- 🧠 **Advanced Sentiment Analysis**: Hybrid analysis using TextBlob, VADER, and custom keyword models
- ⚡ **Real-Time Processing**: Instant sentiment analysis with confidence scores
- 📊 **Interactive Dashboard**: Real-time analytics and visualization
- 🛍️ **Product Catalog**: Browse and select products for feedback
- 💾 **Data Management**: Export capabilities and data persistence
- 🔒 **Privacy-First**: No permanent audio storage, local data processing

## Quick Start

### Option 1: Using the startup script (Recommended)

```bash
./run.sh
```

### Option 2: Manual setup

1. **Create Virtual Environment**

   ```bash
   python3 -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

2. **Install Dependencies**

   ```bash
   pip install -r requirements.txt
   ```

3. **Download NLTK Data**

   ```bash
   python3 -c "import nltk; nltk.download('punkt'); nltk.download('brown')"
   ```

4. **Run the Application**

   ```bash
   streamlit run app.py
   ```

5. **Access the Application**
   Open your browser and navigate to `http://localhost:8501`

### Option 3: Try the demo first

```bash
source venv/bin/activate
python3 demo.py
```

## Usage

### Collecting Feedback

1. Navigate to "Feedback Collection"
2. Select a product from the catalog
3. Choose input method (Voice or Text)
4. Provide your feedback
5. View instant sentiment analysis results

### Analytics Dashboard

- View sentiment trends over time
- Analyze sentiment distribution
- Compare product performance
- Export data for further analysis

### Product Catalog

- Browse available products
- Search and filter by category
- View product details

## Technical Architecture

### Core Components

- **Sentiment Analyzer**: Multi-model sentiment analysis engine
- **Product Catalog**: Product management system
- **Data Manager**: SQLite database with JSON backup
- **Audio Processor**: Speech-to-text conversion

### Technology Stack

- **Frontend**: Streamlit
- **Backend**: Python 3.8+
- **Database**: SQLite with JSON fallback
- **Speech Processing**: Google Speech Recognition
- **Sentiment Analysis**: TextBlob, VADER, Custom Keywords
- **Visualization**: Plotly

## Configuration

The application uses default configurations that work out of the box. Data is stored in the `data/` directory:

- `data/feedback.db` - SQLite database
- `data/feedback_backup.json` - JSON backup
- `data/products.json` - Product catalog

## Performance

- **Text Analysis**: < 3 seconds
- **Voice Processing**: < 10 seconds
- **Dashboard Load**: < 3 seconds
- **Concurrent Users**: 50+ supported

## Security & Privacy

- No permanent storage of audio files
- Data encryption at rest for SQLite database
- Browser-based microphone access
- Compliance with basic data privacy requirements

## 🚀 Deployment

### Local Development

```bash
git clone https://github.com/your-username/voice-sentiment-analyzer.git
cd voice-sentiment-analyzer
./run.sh
```

### Streamlit Cloud

1. Fork this repository
2. Connect your GitHub account to [Streamlit Cloud](https://streamlit.io/cloud)
3. Deploy directly from your repository
4. Set Python version to 3.8+ in advanced settings

### Docker (Coming Soon)

```bash
docker build -t voice-sentiment-analyzer .
docker run -p 8501:8501 voice-sentiment-analyzer
```

### Heroku

1. Create a new Heroku app
2. Connect to your GitHub repository
3. Add Python buildpack
4. Deploy from main branch

## 📊 Demo Data

The application comes with sample data to demonstrate functionality:

- 10 sample products across 5 categories
- Pre-configured sentiment analysis models
- Sample feedback entries for testing

## 🤝 Contributing

We welcome contributions! Please see our [Contributing Guidelines](CONTRIBUTING.md) for details.

### Quick Contribution Steps

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## 📈 Roadmap

### Phase 1 (Current)

- ✅ Multi-modal sentiment analysis
- ✅ Real-time dashboard
- ✅ Product catalog management
- ✅ Data export capabilities

### Phase 2 (Next)

- [ ] Multi-language support
- [ ] Advanced ML models (BERT, RoBERTa)
- [ ] API endpoints
- [ ] User authentication

### Phase 3 (Future)

- [ ] Mobile application
- [ ] Enterprise features
- [ ] Advanced analytics
- [ ] Third-party integrations

## 🏆 Acknowledgments

- Built with [Streamlit](https://streamlit.io/) for the web interface
- Sentiment analysis powered by [TextBlob](https://textblob.readthedocs.io/) and [VADER](https://github.com/cjhutto/vaderSentiment)
- Speech recognition using [SpeechRecognition](https://pypi.org/project/SpeechRecognition/)
- Visualizations created with [Plotly](https://plotly.com/)

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🆘 Support

- 📖 [Documentation](README.md)
- 🐛 [Report Issues](https://github.com/your-username/voice-sentiment-analyzer/issues)
- 💬 [Discussions](https://github.com/your-username/voice-sentiment-analyzer/discussions)
- 📧 Contact: [your-email@example.com](mailto:your-email@example.com)

---

⭐ **Star this repository if you find it helpful!** ⭐
