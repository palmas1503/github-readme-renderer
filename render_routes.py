"""
Routes for rendering GitHub README files
"""

from flask import Blueprint, request, jsonify
import httpx
import markdown
import logging
import asyncio
from utils import validate_github_url, log_request, log_response
from errors import ValidationError, ProviderError, TimeoutError
from middleware import require_json

logger = logging.getLogger(__name__)

render_bp = Blueprint('render', __name__, url_prefix='/api/render')


async def fetch_readme_content(owner: str, repo: str) -> str:
    """Fetch README content from GitHub"""
    github_api_url = f"https://api.github.com/repos/{owner}/{repo}/readme"
    
    headers = {
        'Accept': 'application/vnd.github.v3.raw',
        'User-Agent': 'github-readme-renderer'
    }
    
    try:
        async with httpx.AsyncClient() as client:
            response = await client.get(github_api_url, headers=headers, timeout=10.0)
            
            if response.status_code == 200:
                return response.text
            elif response.status_code == 404:
                return None
            else:
                raise ProviderError('GitHub', response.status_code)
    
    except httpx.TimeoutException:
        raise TimeoutError('GitHub')
    except Exception as e:
        logger.error(f"Error fetching README: {str(e)}")
        raise


def render_markdown_to_html(markdown_content: str) -> str:
    """Convert Markdown to HTML"""
    try:
        extensions = ['markdown.extensions.extra', 'markdown.extensions.codehilite', 'markdown.extensions.toc']
        return markdown.markdown(markdown_content, extensions=extensions)
    except Exception as e:
        logger.error(f"Error rendering markdown: {str(e)}")
        raise


@render_bp.route('/url', methods=['POST'])
@require_json
def render_from_url():
    """Render README from GitHub URL"""
    try:
        data = request.get_json()
        
        if not data or 'url' not in data:
            raise ValidationError("Missing 'url' parameter")
        
        github_url = data.get('url').strip()
        
        if not validate_github_url(github_url):
            raise ValidationError("Invalid GitHub URL")
        
        # Parse GitHub URL
        parts = github_url.rstrip('/').split('/')
        if len(parts) < 5:
            raise ValidationError("Invalid GitHub URL format")
        
        owner = parts[-2]
        repo = parts[-1].replace('.git', '')
        
        # Fetch and render
        loop = asyncio.new_event_loop()
        try:
            readme_content = loop.run_until_complete(fetch_readme_content(owner, repo))
        finally:
            loop.close()
        
        if not readme_content:
            raise ValidationError(f"README not found in {owner}/{repo}")
        
        html_content = render_markdown_to_html(readme_content)
        
        response = {
            'status': 'success',
            'owner': owner,
            'repo': repo,
            'html': html_content,
            'markdown_length': len(readme_content)
        }
        
        return jsonify(response), 200
    
    except ValidationError as e:
        return jsonify({'status': 'error', 'message': e.message, 'error_code': e.error_code}), e.status_code
    except Exception as e:
        logger.error(f"Render error: {str(e)}")
        return jsonify({'status': 'error', 'message': str(e), 'error_code': 'RENDER_ERROR'}), 500


@render_bp.route('/markdown', methods=['POST'])
@require_json
def render_markdown():
    """Render Markdown content to HTML"""
    try:
        data = request.get_json()
        
        if not data or 'markdown' not in data:
            raise ValidationError("Missing 'markdown' parameter")
        
        markdown_content = data.get('markdown').strip()
        
        if not markdown_content:
            raise ValidationError("Markdown content is empty")
        
        html_content = render_markdown_to_html(markdown_content)
        
        return jsonify({'status': 'success', 'html': html_content, 'markdown_length': len(markdown_content)}), 200
    
    except ValidationError as e:
        return jsonify({'status': 'error', 'message': e.message, 'error_code': e.error_code}), e.status_code
    except Exception as e:
        logger.error(f"Markdown error: {str(e)}")
        return jsonify({'status': 'error', 'message': str(e), 'error_code': 'RENDER_ERROR'}), 500


@render_bp.route('/health', methods=['GET'])
def health():
    """Health check"""
    return jsonify({'status': 'ok', 'service': 'readme-renderer'}), 200
