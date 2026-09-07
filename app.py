"""
GitHub README Renderer with Integrated AI Search Engine
Flask application supporting HTTPS with GPT + DeepSeek search
"""

from flask import Flask, render_template, request, jsonify
from search_routes import search_bp
from render_routes import render_bp
from middleware import (
    log_request_middleware,
    log_response_middleware,
    handle_app_error,
    handle_bad_request,
    handle_not_found,
    handle_internal_error
)
from errors import AppError
from config import config
import os
import logging
from datetime import datetime

# Configure logging
logging.basicConfig(
    level=getattr(logging, config.LOG_LEVEL),
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Create Flask app
app = Flask(__name__)
app.config["JSON_SORT_KEYS"] = False

# Register blueprints
app.register_blueprint(search_bp)
app.register_blueprint(render_bp)

# Register middleware
app.before_request(log_request_middleware)
app.after_request(log_response_middleware)

# Register error handlers
app.register_error_handler(AppError, handle_app_error)
app.register_error_handler(400, handle_bad_request)
app.register_error_handler(404, handle_not_found)
app.register_error_handler(500, handle_internal_error)


@app.route("/", methods=["GET"])
def index():
    """Main page - API information"""
    return jsonify({
        "name": "GitHub README Renderer with AI Search",
        "version": "2.0.0",
        "description": "Flask application to render GitHub README files as HTML with webhook support",
        "environment": config.FLASK_ENV,
        "features": [
            "Render GitHub README files as HTML",
            "AI-powered search with GPT",
            "AI-powered search with DeepSeek",
            "Hybrid search (both models)",
            "Webhook support",
            "Markdown rendering"
        ],
        "api_endpoints": {
            "health": {
                "path": "/health",
                "method": "GET",
                "description": "General health check"
            },
            "search": {
                "path": "/api/search/",
                "method": "POST",
                "description": "Search with AI"
            },
            "search_readme": {
                "path": "/api/search/readme",
                "method": "POST",
                "description": "Search within README content"
            },
            "search_health": {
                "path": "/api/search/health",
                "method": "GET",
                "description": "Search engine health check"
            },
            "search_models": {
                "path": "/api/search/models",
                "method": "GET",
                "description": "Get available AI models"
            },
            "render_markdown": {
                "path": "/api/render/markdown",
                "method": "POST",
                "description": "Render markdown to HTML"
            },
            "render_github": {
                "path": "/api/render/url",
                "method": "POST",
                "description": "Render GitHub README to HTML"
            },
            "render_health": {
                "path": "/api/render/health",
                "method": "GET",
                "description": "Renderer health check"
            }
        },
        "documentation": "https://github.com/palmas1503/github-readme-renderer",
        "repository": "palmas1503/github-readme-renderer",
        "timestamp": datetime.utcnow().isoformat(),
        "status": "running"
    })


@app.route("/health", methods=["GET"])
def health():
    """Main health check endpoint"""
    return jsonify({
        "status": "healthy",
        "service": "github-readme-renderer",
        "version": "2.0.0",
        "environment": config.FLASK_ENV,
        "timestamp": datetime.utcnow().isoformat(),
        "uptime": "running"
    }), 200


@app.route("/info", methods=["GET"])
def info():
    """Get application information"""
    return jsonify({
        "name": "GitHub README Renderer",
        "version": "2.0.0",
        "description": "Flask application to render GitHub README files as HTML with webhook support",
        "author": "palmas1503",
        "license": "MIT",
        "repository": "https://github.com/palmas1503/github-readme-renderer",
        "environment": config.FLASK_ENV,
        "port": config.PORT,
        "debug": config.FLASK_DEBUG,
        "ssl_enabled": config.USE_SSL,
        "timestamp": datetime.utcnow().isoformat()
    }), 200


@app.route("/status", methods=["GET"])
def status():
    """Get application status"""
    try:
        # Validate API keys
        gpt_configured = bool(config.OPENAI_API_KEY)
        deepseek_configured = bool(config.DEEPSEEK_API_KEY)
        
        return jsonify({
            "status": "operational",
            "services": {
                "search_engine": {
                    "status": "configured" if (gpt_configured or deepseek_configured) else "not configured",
                    "gpt": "available" if gpt_configured else "not configured",
                    "deepseek": "available" if deepseek_configured else "not configured"
                },
                "renderer": {
                    "status": "available"
                }
            },
            "timestamp": datetime.utcnow().isoformat()
        }), 200
    
    except Exception as e:
        logger.error(f"Status check error: {str(e)}")
        return jsonify({
            "status": "error",
            "message": "Unable to check application status",
            "error": str(e)
        }), 500


if __name__ == "__main__":
    try:
        # Validate configuration
        config.validate()
        
        # Log startup info
        logger.info("=" * 60)
        logger.info("GitHub README Renderer Starting")
        logger.info("=" * 60)
        logger.info(f"Environment: {config.FLASK_ENV}")
        logger.info(f"Debug: {config.FLASK_DEBUG}")
        logger.info(f"Port: {config.PORT}")
        logger.info(f"SSL: {'Enabled' if config.USE_SSL else 'Disabled'}")
        logger.info(f"OpenAI API: {'Configured' if config.OPENAI_API_KEY else 'Not configured'}")
        logger.info(f"DeepSeek API: {'Configured' if config.DEEPSEEK_API_KEY else 'Not configured'}")
        logger.info("=" * 60)
        
        # Determine SSL context
        ssl_context = None
        if config.USE_SSL:
            try:
                ssl_context = "adhoc"
                logger.warning("Using adhoc SSL - install pyopenssl for production use")
            except Exception as e:
                logger.warning(f"SSL configuration failed: {e}")
                ssl_context = None
        
        # Run Flask app
        app.run(
            host="0.0.0.0",
            port=config.PORT,
            debug=config.FLASK_DEBUG,
            ssl_context=ssl_context,
            use_reloader=config.FLASK_DEBUG
        )
    
    except Exception as e:
        logger.error(f"Failed to start application: {str(e)}")
        exit(1)
