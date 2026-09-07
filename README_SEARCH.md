# AI Search Engine Documentation

Integrated GPT + DeepSeek search engine for GitHub README Renderer.

## Features

- **Dual AI Models**: Use GPT, DeepSeek, or both simultaneously
- **Hybrid Search**: Get results from multiple models for comprehensive answers
- **README Context**: Search within specific README content
- **HTTPS Ready**: Full SSL/TLS support for secure connections
- **RESTful API**: Easy integration with any application
- **Async Support**: High-performance asynchronous operations

## Installation

### Prerequisites
- Python 3.8+
- OpenAI API key (for GPT)
- DeepSeek API key

### Setup

1. **Install dependencies:**
```bash
pip install -r requirements.txt
```

2. **Configure environment variables:**
```bash
cp .env.example .env
```

Edit `.env` with your API keys:
```
OPENAI_API_KEY=sk-your-openai-key
DEEPSEEK_API_KEY=sk-your-deepseek-key
```

3. **Run the application:**
```bash
# Development
python app.py

# Production with HTTPS
gunicorn --certfile=cert.pem --keyfile=key.pem --bind 0.0.0.0:443 app:app
```

## API Endpoints

### 1. General Search
**POST** `/api/search/`

Search using any AI provider.

**Request:**
```json
{
  "query": "How to use Flask?",
  "provider": "hybrid",
  "context": "optional context",
  "temperature": 0.7
}
```

**Parameters:**
- `query` (required): Your search query
- `provider` (optional): `gpt`, `deepseek`, or `hybrid` (default: `hybrid`)
- `context` (optional): Additional context for better results
- `temperature` (optional): Model creativity (0-1, default: 0.7)

**Response:**
```json
{
  "provider": "hybrid",
  "query": "How to use Flask?",
  "results": {
    "gpt": {
      "provider": "gpt",
      "model": "gpt-3.5-turbo",
      "result": "Flask is a lightweight...",
      "status": "success"
    },
    "deepseek": {
      "provider": "deepseek",
      "model": "deepseek-chat",
      "result": "Flask is a popular...",
      "status": "success"
    }
  },
  "status": "success"
}
```

### 2. README Search
**POST** `/api/search/readme`

Search within specific README content.

**Request:**
```json
{
  "query": "What dependencies does this project need?",
  "readme_content": "# Project\n\n## Requirements\n...",
  "provider": "gpt"
}
```

**Parameters:**
- `query` (required): Your search query
- `readme_content` (required): Full README content to search within
- `provider` (optional): `gpt`, `deepseek`, or `hybrid` (default: `hybrid`)

**Response:**
```json
{
  "provider": "gpt",
  "model": "gpt-3.5-turbo",
  "result": "Based on the README, this project requires...",
  "status": "success"
}
```

### 3. Health Check
**GET** `/api/search/health`

Check if the search service is running.

**Response:**
```json
{
  "status": "ok",
  "service": "ai-search-engine"
}
```

### 4. Available Models
**GET** `/api/search/models`

Get information about available models.

**Response:**
```json
{
  "providers": ["gpt", "deepseek", "hybrid"],
  "gpt_model": "gpt-3.5-turbo",
  "deepseek_model": "deepseek-chat",
  "docs": "https://github.com/palmas1503/github-readme-renderer"
}
```

## Usage Examples

### Python
```python
import requests
import json

# Search using both models
response = requests.post(
    "https://your-domain.com/api/search/",
    json={
        "query": "What is this project about?",
        "provider": "hybrid",
        "temperature": 0.7
    }
)

results = response.json()
print(results)
```

### cURL
```bash
curl -X POST https://your-domain.com/api/search/ \
  -H "Content-Type: application/json" \
  -d '{
    "query": "What is this project about?",
    "provider": "hybrid"
  }'
```

### JavaScript/Node.js
```javascript
const response = await fetch('https://your-domain.com/api/search/', {
  method: 'POST',
  headers: {
    'Content-Type': 'application/json'
  },
  body: JSON.stringify({
    query: 'What is this project about?',
    provider: 'hybrid'
  })
});

const results = await response.json();
console.log(results);
```

## HTTPS Configuration

### Development (Self-signed certificate)
```bash
# Generate self-signed certificate
openssl req -x509 -newkey rsa:4096 -nodes -out cert.pem -keyout key.pem -days 365

# Run with HTTPS
gunicorn --certfile=cert.pem --keyfile=key.pem --bind 0.0.0.0:443 app:app
```

### Production (Let's Encrypt)
```bash
# Install certbot
sudo apt-get install certbot python3-certbot-nginx

# Get certificate
sudo certbot certonly --standalone -d your-domain.com

# Run with production certificate
gunicorn --certfile=/etc/letsencrypt/live/your-domain.com/fullchain.pem \
         --keyfile=/etc/letsencrypt/live/your-domain.com/privkey.pem \
         --bind 0.0.0.0:443 app:app
```

### Environment Variable
```bash
USE_SSL=True python app.py
```

## API Costs

Be aware of API usage costs:
- **GPT**: Usage rates depend on model (3.5-turbo: ~$0.002 per 1K tokens)
- **DeepSeek**: Generally lower cost than GPT
- **Hybrid**: Costs sum for both models

Monitor your API usage in:
- OpenAI Dashboard: https://platform.openai.com/account/usage
- DeepSeek Console: https://www.deepseek.com/console

## Error Handling

### Missing API Keys
```json
{
  "error": "GPT API key not configured",
  "status": "failed"
}
```

**Solution**: Add keys to `.env` file

### Invalid Provider
```json
{
  "error": "Invalid provider: invalid_name",
  "status": "failed"
}
```

**Solution**: Use one of: `gpt`, `deepseek`, `hybrid`

### API Rate Limits
```json
{
  "error": "Rate limit exceeded",
  "status": "failed"
}
```

**Solution**: Implement request throttling or upgrade API plan

## Performance Tips

1. **Use specific providers**: Don't always use hybrid if you don't need both results
2. **Optimize context**: Provide only relevant context to reduce token usage
3. **Cache results**: Store frequently searched queries
4. **Lower temperature**: Use 0.1-0.3 for factual queries, 0.7-1.0 for creative ones
5. **Monitor usage**: Track API calls and costs regularly

## Troubleshooting

### Connection Timeout
- Check internet connection
- Verify API endpoints are accessible
- Increase timeout value in code

### CORS Issues
- Add CORS middleware to Flask:
```python
from flask_cors import CORS
CORS(app)
```

### SSL Certificate Errors
- Verify certificate path in gunicorn command
- Check certificate expiration date
- Use valid domain name

## Contributing

Found a bug or have a suggestion? Create an issue on GitHub:
https://github.com/palmas1503/github-readme-renderer

## License

MIT License - see LICENSE file for details
