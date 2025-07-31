# 🚀 Deployment Guide

This guide covers various deployment options for the Voice Sentiment Analyzer.

## 📋 Prerequisites

- Python 3.8 or higher
- Git
- Internet connection for downloading dependencies

## 🏠 Local Development

### Quick Start

```bash
git clone https://github.com/your-username/voice-sentiment-analyzer.git
cd voice-sentiment-analyzer
./run.sh
```

### Manual Setup

```bash
# Clone repository
git clone https://github.com/your-username/voice-sentiment-analyzer.git
cd voice-sentiment-analyzer

# Create virtual environment
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Download NLTK data
python3 -c "import nltk; nltk.download('punkt'); nltk.download('brown')"

# Run application
streamlit run app.py
```

## ☁️ Cloud Deployment

### Streamlit Cloud (Recommended)

1. **Fork the repository** to your GitHub account
2. **Sign up** for [Streamlit Cloud](https://streamlit.io/cloud)
3. **Connect your GitHub account**
4. **Deploy** by selecting your forked repository
5. **Configure** Python version to 3.8+ in advanced settings

**Deployment URL**: Your app will be available at `https://your-app-name.streamlit.app`

### Heroku

1. **Create Heroku account** and install Heroku CLI
2. **Create new app**:
   ```bash
   heroku create your-app-name
   ```
3. **Add Python buildpack**:
   ```bash
   heroku buildpacks:set heroku/python
   ```
4. **Deploy**:
   ```bash
   git push heroku main
   ```

### Railway

1. **Connect GitHub repository** to Railway
2. **Configure environment**:
   - Python version: 3.8+
   - Start command: `streamlit run app.py --server.port $PORT`
3. **Deploy** automatically on push

### Render

1. **Connect GitHub repository** to Render
2. **Configure service**:
   - Environment: Python 3
   - Build command: `pip install -r requirements.txt`
   - Start command: `streamlit run app.py --server.port $PORT --server.address 0.0.0.0`

## 🐳 Docker Deployment

### Build and Run Locally

```bash
# Build image
docker build -t voice-sentiment-analyzer .

# Run container
docker run -p 8501:8501 voice-sentiment-analyzer
```

### Docker Compose

```yaml
version: "3.8"
services:
  app:
    build: .
    ports:
      - "8501:8501"
    volumes:
      - ./data:/app/data
    environment:
      - STREAMLIT_SERVER_HEADLESS=true
```

### Deploy to Docker Hub

```bash
# Tag image
docker tag voice-sentiment-analyzer your-username/voice-sentiment-analyzer:latest

# Push to Docker Hub
docker push your-username/voice-sentiment-analyzer:latest
```

## 🔧 Environment Configuration

### Environment Variables

```bash
# Optional configurations
export STREAMLIT_SERVER_PORT=8501
export STREAMLIT_SERVER_ADDRESS=0.0.0.0
export STREAMLIT_SERVER_HEADLESS=true
```

### Streamlit Configuration

Create `.streamlit/config.toml`:

```toml
[server]
port = 8501
headless = true

[browser]
gatherUsageStats = false
```

## 📊 Production Considerations

### Performance Optimization

- Use caching for data loading (`@st.cache_data`)
- Optimize database queries
- Consider using Redis for session storage
- Implement connection pooling

### Security

- Enable HTTPS in production
- Implement rate limiting
- Add input validation
- Use environment variables for sensitive data

### Monitoring

- Set up application monitoring (e.g., Sentry)
- Configure logging
- Monitor resource usage
- Set up health checks

### Scaling

- Use load balancers for multiple instances
- Consider database scaling (PostgreSQL)
- Implement caching layers
- Use CDN for static assets

## 🔍 Troubleshooting

### Common Issues

**Port already in use**:

```bash
streamlit run app.py --server.port 8502
```

**NLTK data missing**:

```bash
python3 -c "import nltk; nltk.download('punkt'); nltk.download('brown')"
```

**Permission denied on run.sh**:

```bash
chmod +x run.sh
```

**Memory issues**:

- Increase container memory limits
- Optimize data processing
- Use data streaming for large datasets

### Logs and Debugging

```bash
# View Streamlit logs
streamlit run app.py --logger.level debug

# Docker logs
docker logs container-name

# Heroku logs
heroku logs --tail
```

## 📈 Monitoring and Analytics

### Application Metrics

- Response times
- Error rates
- User engagement
- Resource utilization

### Business Metrics

- Sentiment analysis accuracy
- User feedback volume
- Feature usage statistics
- Export frequency

## 🔄 CI/CD Pipeline

The repository includes GitHub Actions for:

- **Testing**: Automated testing on multiple Python versions
- **Linting**: Code quality checks
- **Security**: Vulnerability scanning
- **Deployment**: Automatic deployment on successful builds

### Manual Deployment Commands

```bash
# Run tests
python demo.py

# Check code quality
flake8 .
black --check .
isort --check-only .

# Security scan
safety check
bandit -r .
```

## 📞 Support

For deployment issues:

- Check the [troubleshooting section](#troubleshooting)
- Review [GitHub Issues](https://github.com/your-username/voice-sentiment-analyzer/issues)
- Contact support: [your-email@example.com](mailto:your-email@example.com)

---

**Happy Deploying!** 🚀
