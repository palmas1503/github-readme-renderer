"""
GitHub README Renderer with Integrated AI Search Engine
Flask application supporting HTTPS with GPT + DeepSeek search
"""

from flask import Flask, render_template, request, jsonify
from search_routes import search_bp
import os
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = Flask(__name__)
app.config["JSON_SORT_KEYS"] = False

# Register search engine blueprint
app.register_blueprint(search_bp)


@app.route("/", methods=["GET"])
def index():
    """Main page"""
    return jsonify(
        {
            "name": "GitHub README Renderer with AI Search",
            "version": "1.0.0",
            "features": [
                "Render GitHub README files as HTML",
                "AI-powered search with GPT",
                "AI-powered search with DeepSeek",
                "Hybrid search (both models)",
                "Webhook support",
            ],
            "endpoints": {
                "health": "/api/search/health",
                "search": "/api/search/",
                "search_readme": "/api/search/readme",
                "models": "/api/search/models",
            },
            "documentation": "https://github.com/palmas1503/github-readme-renderer",
        }
    )


@app.route("/health", methods=["GET"])
def health():
    """Health check"""
    return jsonify({"status": "healthy", "service": "readme-renderer"}), 200


@app.errorhandler(404)
def not_found(error):
    """Handle 404 errors"""
    return jsonify({"error": "Endpoint not found"}), 404


@app.errorhandler(500)
def internal_error(error):
    """Handle 500 errors"""
    logger.error(f"Internal server error: {str(error)}")
    return jsonify({"error": "Internal server error"}), 500


if __name__ == "__main__":
    # For production, use with gunicorn and SSL certificates
    # gunicorn --certfile=cert.pem --keyfile=key.pem --bind 0.0.0.0:443 app:app
    
    debug = os.getenv("FLASK_DEBUG", "False").lower() == "true"
    port = int(os.getenv("PORT", 5000))
    
    app.run(
        host="0.0.0.0",
        port=port,
        debug=debug,
        ssl_context="adhoc" if os.getenv("USE_SSL") else None,
    )
