from flask import request, jsonify
from functools import wraps
import base64

def basic_auth_required(f):
    """Decorator to require Basic Authentication."""
    @wraps(f)
    def decorated_function(*args, **kwargs):
        auth = request.headers.get('Authorization')
        if not auth or not auth.startswith('Basic '):
            return jsonify({'message': 'Authentication required'}), 401

        # Decode Basic Auth
        try:
            encoded_credentials = auth.split(' ')[1]
            decoded_credentials = base64.b64decode(encoded_credentials).decode('utf-8')
            username, password = decoded_credentials.split(':')
        except Exception:
            return jsonify({'message': 'Invalid credentials format'}), 401

        return f(username, password, *args, **kwargs)
    return decorated_function
