# GitHub README Renderer - Installation Guide

Complete guide to install and run the GitHub README Renderer application.

## Prerequisites

- Python 3.8 or higher
- pip (Python package manager)
- git
- (Optional) Docker and Docker Compose

## Quick Start (Local Development)

### 1. Clone the Repository

```bash
git clone https://github.com/palmas1503/github-readme-renderer.git
cd github-readme-renderer
```

### 2. Create Virtual Environment

```bash
# Linux/macOS
python3 -m venv venv
source venv/bin/activate

# Windows
python -m venv venv
venv\Scripts\activate
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

### 4. Configure Environment Variables

```bash
# Copy example configuration
cp .env.example .env

# Edit .env file with your API keys
nano .env  # or use your preferred editor
```

**Required environment variables:**
```env
# At least one API key is required
OPENAI_API_KEY=sk-your-openai-key-here
DEEPSEEK_API_KEY=sk-your-deepseek-key-here

# Optional settings
FLASK_ENV=development
FLASK_DEBUG=True
PORT=5000
USE_SSL=False
```

### 5. Run the Application

```bash
# Development mode
python app.py

# With debug logging
FLASK_DEBUG=true python app.py

# With custom port
PORT=8000 python app.py
```

The application will start at `http://localhost:5000`

---

## Docker Installation

### Using Docker Compose (Recommended)

```bash
# 1. Clone the repository
git clone https://github.com/palmas1503/github-readme-renderer.git
cd github-readme-renderer

# 2. Create .env file
cp .env.example .env
# Edit .env with your API keys

# 3. Start with Docker Compose
docker-compose up -d

# 4. View logs
docker-compose logs -f readme-renderer

# 5. Stop the service
docker-compose down
```

### Using Docker Directly

```bash
# Build image
docker build -t github-readme-renderer .

# Run container
docker run -d \
  --name readme-renderer \
  -p 5000:5000 \
  -e OPENAI_API_KEY=sk-your-key \
  -e DEEPSEEK_API_KEY=sk-your-key \
  github-readme-renderer

# View logs
docker logs -f readme-renderer

# Stop container
docker stop readme-renderer
```

---

## Production Deployment

### Using Gunicorn

```bash
# Install production dependencies
pip install gunicorn

# Run with gunicorn
gunicorn --bind 0.0.0.0:5000 \
         --workers 4 \
         --worker-class sync \
         --timeout 60 \
         --access-logfile - \
         --error-logfile - \
         app:app
```

### With HTTPS/SSL

#### Generate Self-Signed Certificate

```bash
# Generate certificate valid for 365 days
openssl req -x509 -newkey rsa:4096 -nodes \
    -out cert.pem -keyout key.pem -days 365

# Run with gunicorn and SSL
gunicorn --certfile=cert.pem --keyfile=key.pem \
         --bind 0.0.0.0:443 \
         --workers 4 \
         app:app
```

#### Using Let's Encrypt

```bash
# Install certbot
sudo apt-get install certbot

# Get certificate
sudo certbot certonly --standalone -d your-domain.com

# Run with production certificate
gunicorn --certfile=/etc/letsencrypt/live/your-domain.com/fullchain.pem \
         --keyfile=/etc/letsencrypt/live/your-domain.com/privkey.pem \
         --bind 0.0.0.0:443 \
         --workers 4 \
         app:app
```

### Using Systemd Service

Create `/etc/systemd/system/readme-renderer.service`:

```ini
[Unit]
Description=GitHub README Renderer
After=network.target

[Service]
Type=notify
User=www-data
WorkingDirectory=/var/www/github-readme-renderer
Environment="PATH=/var/www/github-readme-renderer/venv/bin"
EnvironmentFile=/var/www/github-readme-renderer/.env
ExecStart=/var/www/github-readme-renderer/venv/bin/gunicorn \
    --bind 0.0.0.0:5000 \
    --workers 4 \
    --timeout 60 \
    app:app

[Install]
WantedBy=multi-user.target
```

Enable and start:

```bash
sudo systemctl daemon-reload
sudo systemctl enable readme-renderer
sudo systemctl start readme-renderer
sudo systemctl status readme-renderer
```

### Using Nginx Reverse Proxy

```nginx
server {
    listen 80;
    server_name your-domain.com;

    location / {
        proxy_pass http://localhost:5000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }
}
```

---

## Verification

### Check Installation

```bash
# Test the application
curl http://localhost:5000/

# Health check
curl http://localhost:5000/health

# Search engine status
curl http://localhost:5000/api/search/health

# Render health
curl http://localhost:5000/api/render/health
```

### API Testing

```bash
# Search with AI
curl -X POST http://localhost:5000/api/search/ \
  -H "Content-Type: application/json" \
  -d '{
    "query": "How to use Flask?",
    "provider": "hybrid"
  }'

# Render markdown
curl -X POST http://localhost:5000/api/render/markdown \
  -H "Content-Type: application/json" \
  -d '{
    "markdown": "# Hello World"
  }'

# Render GitHub README
curl -X POST http://localhost:5000/api/render/url \
  -H "Content-Type: application/json" \
  -d '{
    "url": "https://github.com/palmas1503/github-readme-renderer"
  }'
```

---

## Troubleshooting

### Import Errors

If you get "ModuleNotFoundError", ensure virtual environment is activated:

```bash
# Linux/macOS
source venv/bin/activate

# Windows
venv\Scripts\activate
```

### API Key Errors

Make sure your `.env` file has valid API keys:

```bash
# Verify .env exists
ls -la .env

# Check permissions
cat .env | grep API_KEY
```

### Port Already in Use

```bash
# Change port
PORT=8000 python app.py

# Or kill process using port 5000
lsof -i :5000
kill -9 <PID>
```

### SSL Certificate Issues

```bash
# Install pyopenssl for adhoc SSL
pip install pyopenssl

# Or use proper certificates with gunicorn
```

### Docker Issues

```bash
# Check container logs
docker-compose logs -f

# Rebuild image
docker-compose build --no-cache

# Reset everything
docker-compose down -v
docker-compose up -d
```

---

## Next Steps

1. **Configure API Keys**: Get keys from [OpenAI](https://platform.openai.com/) and [DeepSeek](https://www.deepseek.com/)
2. **Test Endpoints**: Use provided curl commands or Postman
3. **Deploy**: Choose production deployment method
4. **Monitor**: Set up logging and monitoring
5. **Secure**: Use HTTPS and strong authentication

See [README.md](README.md) for API documentation.
