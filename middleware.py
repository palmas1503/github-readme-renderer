"""
Flask middleware and request/response handlers
"""

from flask import request, jsonify, g
from functools import wraps
from datetime import datetime
import time
import logging
from errors import AppError

logger = logging.getLogger(__name__)


def log_request_middleware():
    """Log incoming requests"""
    g.start_time = time.time()
    logger.info(f"→ {request.method} {request.path}")


def log_response_middleware(response):
    """Log outgoing responses"""
    if hasattr(g, 'start_time'):
        duration = (time.time() - g.start_time) * 1000
        logger.info(f"← {response.status_code} (took {duration:.2f}ms)")
    return response


def handle_app_error(error):
    """Handle AppError exceptions"""
    if isinstance(error, AppError):
        response = {
            'status': 'error',
            'message': error.message,
            'error_code': error.error_code,
            'timestamp': datetime.utcnow().isoformat()
        }
        
        if hasattr(error, 'retry_after') and error.retry_after:
            response['retry_after'] = error.retry_after
        
        return jsonify(response), error.status_code
    
    raise error


def handle_bad_request(error):
    """Handle 400 Bad Request"""
    return jsonify({
        'status': 'error',
        'message': 'Bad request',
        'error_code': 'BAD_REQUEST',
        'timestamp': datetime.utcnow().isoformat()
    }), 400


def handle_not_found(error):
    """Handle 404 Not Found"""
    return jsonify({
        'status': 'error',
        'message': 'Endpoint not found',
        'error_code': 'NOT_FOUND',
        'timestamp': datetime.utcnow().isoformat()
    }), 404


def handle_internal_error(error):
    """Handle 500 Internal Server Error"""
    logger.error(f"Internal server error: {str(error)}", exc_info=True)
    return jsonify({
        'status': 'error',
        'message': 'Internal server error',
        'error_code': 'INTERNAL_ERROR',
        'timestamp': datetime.utcnow().isoformat()
    }), 500


def require_json(f):
    """Decorator to require JSON content type"""
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not request.is_json:
            return jsonify({
                'status': 'error',
                'message': 'Content-Type must be application/json',
                'error_code': 'INVALID_CONTENT_TYPE',
                'timestamp': datetime.utcnow().isoformat()
            }), 415
        return f(*args, **kwargs)
    return decorated_function
