from flask import jsonify
import logging
from werkzeug.exceptions import HTTPException

logger = logging.getLogger(__name__)

def handle_error(e):
    """Global error handler: always return JSON instead of HTML"""
    if isinstance(e, HTTPException):
        code = e.code
        message = e.description
        error_type = e.__class__.__name__
    else:
        code = 500
        message = str(e)
        error_type = e.__class__.__name__

    # Log error with traceback
    logger.error(f"Unexpected error: {message}", exc_info=True)

    return jsonify({
        "error": {
            "type": error_type,
            "message": message,
            "status_code": code
        }
    }), code
