"""
Flask routes for integrated AI search engine
"""

from flask import Blueprint, request, jsonify
from search_engine import search_sync
import logging

logger = logging.getLogger(__name__)

search_bp = Blueprint("search", __name__, url_prefix="/api/search")


@search_bp.route("/", methods=["POST"])
def search():
    """
    Main search endpoint
    
    POST body:
    {
        "query": "your search query",
        "provider": "gpt|deepseek|hybrid",
        "context": "optional context",
        "temperature": 0.7
    }
    """
    try:
        data = request.get_json()

        if not data or "query" not in data:
            return jsonify({"error": "Missing 'query' parameter"}), 400

        query = data.get("query")
        provider = data.get("provider", "hybrid")
        context = data.get("context")
        temperature = data.get("temperature", 0.7)

        if provider not in ["gpt", "deepseek", "hybrid"]:
            return jsonify({"error": f"Invalid provider: {provider}"}), 400

        result = search_sync(query, provider, context, temperature)

        return jsonify(result), 200

    except Exception as e:
        logger.error(f"Search endpoint error: {str(e)}")
        return jsonify({"error": str(e)}), 500


@search_bp.route("/readme", methods=["POST"])
def search_readme():
    """
    Search within README content
    
    POST body:
    {
        "query": "your search query",
        "readme_content": "full readme content",
        "provider": "gpt|deepseek|hybrid"
    }
    """
    try:
        data = request.get_json()

        if not data or "query" not in data or "readme_content" not in data:
            return (
                jsonify({"error": "Missing 'query' or 'readme_content' parameter"}),
                400,
            )

        query = data.get("query")
        readme_content = data.get("readme_content")
        provider = data.get("provider", "hybrid")
        temperature = data.get("temperature", 0.7)

        result = search_sync(query, provider, readme_content, temperature)

        return jsonify(result), 200

    except Exception as e:
        logger.error(f"README search error: {str(e)}")
        return jsonify({"error": str(e)}), 500


@search_bp.route("/health", methods=["GET"])
def health():
    """Health check endpoint"""
    return jsonify({"status": "ok", "service": "ai-search-engine"}), 200


@search_bp.route("/models", methods=["GET"])
def models():
    """Get available models"""
    return (
        jsonify(
            {
                "providers": ["gpt", "deepseek", "hybrid"],
                "gpt_model": "gpt-3.5-turbo",
                "deepseek_model": "deepseek-chat",
                "docs": "https://github.com/palmas1503/github-readme-renderer",
            }
        ),
        200,
    )
