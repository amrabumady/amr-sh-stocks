# 🚀 Deployment Guide

This guide covers deploying the EGX Stock Predictor to various platforms.

## 📋 Table of Contents

1. [Local Deployment](#local-deployment)
2. [Streamlit Community Cloud](#streamlit-community-cloud)
3. [Heroku](#heroku)
4. [Docker](#docker)
5. [AWS/GCP/Azure](#cloud-platforms)

---

## 💻 Local Deployment

### Quick Start

```bash
# Clone repository
git clone https://github.com/yourusername/egx-stock-predictor.git
cd egx-stock-predictor

# Run setup script
./run.sh
```

### Manual Setup

```bash
# Create virtual environment
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Run application
streamlit run streamlit_app.py
```

The app will be available at `http://localhost:8501`

---

## ☁️ Streamlit Community Cloud

### Prerequisites

- GitHub account
- Streamlit Community Cloud account (free at [share.streamlit.io](https://share.streamlit.io))

### Steps

1. **Push to GitHub**

```bash
git init
git add .
git commit -m "Initial commit"
git branch -M main
git remote add origin https://github.com/yourusername/egx-stock-predictor.git
git push -u origin main
```

2. **Deploy to Streamlit Cloud**

- Go to [share.streamlit.io](https://share.streamlit.io)
- Click "New app"
- Select your GitHub repository
- Choose branch: `main`
- Main file path: `streamlit_app.py`
- Click "Deploy"

3. **Configuration** (if needed)

Create `.streamlit/config.toml`:

```toml
[theme]
primaryColor = "#1f77b4"
backgroundColor = "#ffffff"
secondaryBackgroundColor = "#f0f2f6"
textColor = "#262730"
font = "sans serif"

[server]
headless = true
port = 8501
enableCORS = false
```

Your app will be live at: `https://yourusername-egx-stock-predictor.streamlit.app`

---

## 🌐 Heroku

### Prerequisites

- Heroku account
- Heroku CLI installed

### Files Needed

1. **Procfile**

```
web: sh setup.sh && streamlit run streamlit_app.py
```

2. **setup.sh**

```bash
mkdir -p ~/.streamlit/

echo "\
[server]\n\
headless = true\n\
port = $PORT\n\
enableCORS = false\n\
\n\
" > ~/.streamlit/config.toml
```

### Deployment

```bash
# Login to Heroku
heroku login

# Create app
heroku create your-app-name

# Deploy
git push heroku main

# Open app
heroku open
```

---

## 🐳 Docker

### Create Dockerfile

```dockerfile
FROM python:3.9-slim

WORKDIR /app

# Install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application
COPY . .

# Expose port
EXPOSE 8501

# Run application
CMD ["streamlit", "run", "streamlit_app.py", "--server.port=8501", "--server.address=0.0.0.0"]
```

### Build and Run

```bash
# Build image
docker build -t egx-predictor .

# Run container
docker run -p 8501:8501 egx-predictor
```

### Docker Compose

Create `docker-compose.yml`:

```yaml
version: '3.8'

services:
  app:
    build: .
    ports:
      - "8501:8501"
    volumes:
      - ./data:/app/data
    environment:
      - STREAMLIT_SERVER_PORT=8501
```

Run with:
```bash
docker-compose up
```

---

## ☁️ Cloud Platforms

### AWS (EC2)

1. **Launch EC2 Instance**
   - Ubuntu 22.04 LTS
   - t2.medium or larger
   - Open port 8501 in security group

2. **Connect and Setup**

```bash
ssh -i your-key.pem ubuntu@your-ec2-ip

# Update system
sudo apt update && sudo apt upgrade -y

# Install Python
sudo apt install python3-pip python3-venv -y

# Clone repository
git clone https://github.com/yourusername/egx-stock-predictor.git
cd egx-stock-predictor

# Setup and run
./run.sh
```

3. **Keep Running** (using screen)

```bash
screen -S predictor
./run.sh
# Press Ctrl+A, then D to detach
```

### Google Cloud Platform (GCP)

Use Cloud Run for serverless deployment:

```bash
# Build and deploy
gcloud run deploy egx-predictor \
  --source . \
  --platform managed \
  --region us-central1 \
  --allow-unauthenticated
```

### Azure

Deploy using Azure Container Instances:

```bash
# Build and push to Azure Container Registry
az acr build --registry myregistry --image egx-predictor .

# Deploy
az container create \
  --resource-group myResourceGroup \
  --name egx-predictor \
  --image myregistry.azurecr.io/egx-predictor \
  --dns-name-label egx-predictor \
  --ports 8501
```

---

## 🔒 Security Considerations

### For Production Deployment:

1. **Environment Variables**
   - Store sensitive data in environment variables
   - Use `.streamlit/secrets.toml` for secrets (not committed to Git)

2. **Rate Limiting**
   - Implement rate limiting for API calls
   - Cache data appropriately

3. **Authentication**
   - Add user authentication if needed
   - Use Streamlit's native auth features

4. **HTTPS**
   - Ensure SSL/TLS is enabled
   - Use reverse proxy (nginx) if self-hosting

---

## 📊 Monitoring

### Streamlit Cloud
- Built-in analytics dashboard
- View logs in the Streamlit interface

### Self-Hosted
```bash
# View logs
streamlit run streamlit_app.py --server.enableCORS=false --logger.level=debug
```

---

## 🔄 Updates

### Streamlit Cloud
- Push changes to GitHub
- Auto-deploys on commit to main branch

### Heroku
```bash
git push heroku main
```

### Docker
```bash
docker build -t egx-predictor .
docker push your-registry/egx-predictor
```

---

## ⚠️ Troubleshooting

### Memory Issues
- Increase dyno size (Heroku)
- Use larger instance (AWS/GCP)
- Optimize data caching

### Slow Performance
- Enable Streamlit caching
- Reduce lookback days
- Limit concurrent users

### Dependencies
```bash
pip install --upgrade -r requirements.txt
```

---

## 📞 Support

For deployment issues:
- Check [Streamlit Docs](https://docs.streamlit.io)
- Open GitHub issue
- Contact via ClientN.com

---

**Happy Deploying! 🚀**
