from flask import Flask, jsonify
from flask_cors import CORS
from dotenv import load_dotenv
import os

# Load environment variables
load_dotenv()

# Import routes
from routes.candidates import candidates_bp
from routes.search import search_bp

from services.database import Database

# Create Flask app
app = Flask(__name__)

# Enable CORS for frontend
CORS(app, resources={
    r"/api/*": {
        "origins": ["http://localhost:3000", "http://localhost:5173"],
        "methods": ["GET", "POST", "PUT", "DELETE"],
        "allow_headers": ["Content-Type"]
    }
})

# Initialize database
db = Database()
db.init_schema()

# Register blueprints
app.register_blueprint(candidates_bp)
app.register_blueprint(search_bp)


@app.route('/')
def index():
    """API health check."""
    return jsonify({
        'name': 'Grok Talent Engineer API',
        'version': '1.0.0',
        'status': 'running',
        'endpoints': {
            'candidates': '/api/candidates',
            'search': '/api/search',
            'health': '/health'
        }
    })


@app.route('/health')
def health():
    """Health check endpoint."""
    return jsonify({
        'status': 'healthy',
        'grok_api_configured': bool(os.getenv('XAI_API_KEY')),
        'supabase_configured': bool(os.getenv('SUPABASE_URL') and os.getenv('SUPABASE_KEY'))
    })


@app.errorhandler(404)
def not_found(error):
    """Handle 404 errors."""
    return jsonify({'error': 'Endpoint not found'}), 404


@app.errorhandler(500)
def internal_error(error):
    """Handle 500 errors."""
    return jsonify({'error': 'Internal server error'}), 500


if __name__ == '__main__':
    port = int(os.getenv('PORT', 5000))
    debug = os.getenv('FLASK_ENV') == 'development'

    print(f"""
    TPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPW
    Q   Grok Talent Engineer API                 Q
    Q   Running on http://localhost:{port}        Q
    Q   Debug mode: {debug}                       Q
    ZPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPP]
    """)

    app.run(host='0.0.0.0', port=port, debug=debug)
