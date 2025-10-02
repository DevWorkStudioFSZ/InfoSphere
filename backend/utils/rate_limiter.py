from flask_limiter import Limiter
from flask_limiter.util import get_remote_address

# Global limiter instance
limiter = Limiter(
    key_func=get_remote_address,
    default_limits=["100 per hour"]  # Default if route doesn’t override
)
