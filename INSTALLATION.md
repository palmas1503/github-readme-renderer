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
venv\\Scripts\\activate
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

### 4. Configure Environment Variables

```bash
cp .env.example .env
nano .env  # or use your preferred editor
```

### 5. Run the Application

```bash
python app.py
```

The application will start at `http://localhost:5000`

## Docker Installation

### Using Docker Compose (Recommended)

```bash
docker-compose up -d
docker-compose logs -f readme-renderer
```

## Verification

```bash
# Test the application
curl http://localhost:5000/

# Health check
curl http://localhost:5000/health

# Render markdown
curl -X POST http://localhost:5000/api/render/markdown \
  -H "Content-Type: application/json" \
  -d '{"markdown": "# Hello World"}'

# Render GitHub README
curl -X POST http://localhost:5000/api/render/url \
  -H "Content-Type: application/json" \
  -d '{"url": "https://github.com/palmas1503/github-readme-renderer"}'
```
