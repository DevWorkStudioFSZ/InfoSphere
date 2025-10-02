# # from flask import Flask, request, jsonify
# # from flask_cors import CORS
# # from dotenv import load_dotenv
# # import os
# # from utils.error_handler import handle_error
# # from utils.rate_limiter import limiter
# # from routes.search import router as search_bp
# # from routes.export import export_bp
# # import logging

# # # Load environment variables
# # load_dotenv()

# # # Setup logging
# # logging.basicConfig(level=logging.INFO)
# # logger = logging.getLogger(__name__)

# # def create_app():
# #     app = Flask(__name__)
    
# #     # Configuration
# #     app.config['SECRET_KEY'] = os.getenv('SECRET_KEY', 'dev-secret-key-infosphere')
# #     app.config['MONGODB_URI'] = os.getenv('MONGODB_URI')
    
# #     # Enable CORS for frontend communication
# #     #CORS(app, origins=['http://localhost:3000', 'http://localhost:5173'])
# #     # in app.py
# #     CORS(app, origins=[    'http://localhost:3000', 'http://localhost:3001',    'http://127.0.0.1:3000', 'http://127.0.0.1:3001'])

# #     # Initialize rate limiter
# #     limiter.init_app(app)
    
# #     # Register blueprints
# #     app.register_blueprint(search_bp, url_prefix='/api')
# #     app.register_blueprint(export_bp, url_prefix='/api')
    
# #     # Global error handler
# #     @app.errorhandler(Exception)
# #     def handle_exception(e):
# #         return handle_error(e)
    
# #     # Health check endpoint
# #     @app.route('/health')
# #     def health_check():
# #         return jsonify({
# #             'status': 'healthy', 
# #             'service': 'Infosphere Data Extractor API',
# #             'version': '1.0.0'
# #         })
    
# #     @app.route('/')
# #     def home():
# #         return jsonify({
# #             'message': 'Infosphere API is running!',
# #             'endpoints': {
# #                 'health': '/health',
# #                 'search': '/api/search'
# #             }
# #         })

# #     @app.route('/docs')
# #     def docs():
# #         return jsonify({
# #             "service": "Infosphere Data Extractor API",
# #             "version": "1.0.0",
# #             "endpoints": {
# #                 "home": {
# #                     "path": "/",
# #                     "method": "GET",
# #                     "description": "Welcome route with basic info"
# #                 },
# #                 "health": {
# #                     "path": "/health",
# #                     "method": "GET",
# #                     "description": "Check if API is healthy"
# #                 },
# #                 "search": {
# #                     "path": "/api/search",
# #                     "method": "POST",
# #                     "description": "Search for places by city and category",
# #                     "body_example": {
# #                         "city": "Lahore",
# #                         "category": "libraries",
# #                         "filters": {
# #                             "min_rating": 4,
# #                             "open_now": True,
# #                             "has_phone": False,
# #                             "has_website": False
# #                         }
# #                     }
# #                 }
# #             }
# #         })

# #     return app

# # if __name__ == '__main__':
# #     app = create_app()
# #     logger.info("Starting Infosphere API...")
# #     app.run(host='0.0.0.0', port=5000, debug=True)

# # app.py





# # import os
# # from flask import Flask
# # from flask_cors import CORS
# # from dotenv import load_dotenv

# # # Local imports
# # from utils.error_handler import handle_error
# # from utils.rate_limiter import limiter
# # from routes.search import router as search_bp
# # from routes.export import export_bp

# # load_dotenv()  # load .env file

# # def create_app():
# #     app = Flask(__name__)

# #     # Enable CORS
# #     CORS(app)

# #     # Initialize rate limiter
# #     limiter.init_app(app)

# #     # Register blueprints
# #     app.register_blueprint(search_bp, url_prefix="/api")
# #     app.register_blueprint(export_bp, url_prefix="/api")

# #     # Register error handler
# #     app.register_error_handler(Exception, handle_error)

# #     return app

# # app = create_app()

# # if __name__ == "__main__":
# #     port = int(os.getenv("PORT", 5000))
# #     app.run(host="0.0.0.0", port=port, debug=True)

# # app.py
# # app.py
# # import os
# # from flask import Flask
# # from flask_cors import CORS
# # from dotenv import load_dotenv

# # # Local imports (keep same as your project)
# # from utils.error_handler import handle_error
# # from utils.rate_limiter import limiter
# # from routes.search import router as search_bp
# # from routes.export import export_bp



# # load_dotenv()  # load .env

# # def create_app():
# #     app = Flask(__name__)

# #     # Enable CORS for your frontend origins (call AFTER app is created)
# #     # You can list exact origins for safety:
# #     CORS(app, resources={r"/api/*": {"origins": ["http://localhost:3000", "http://127.0.0.1:3000"]}})

# #     # Initialize rate limiter
# #     limiter.init_app(app)

# #     # Register blueprints
# #     app.register_blueprint(search_bp, url_prefix="/api")
# #     app.register_blueprint(export_bp, url_prefix="/api")

# #     # Register error handler
# #     app.register_error_handler(Exception, handle_error)

# #     # root + health endpoints (optional but useful)
# #     @app.route("/")
# #     def home():
# #         return {
# #             "message": "Infosphere API is running 🚀",
# #             "endpoints": {
# #                 "health": "/health",
# #                 "search": "/api/search"
# #             }
# #         }

# #     @app.route("/health")
# #     def health_check():
# #         return {"status": "healthy", "service": "Infosphere API", "version": "1.0.0"}

# #     return app

# # app = create_app()

# # if __name__ == "__main__":
# #     port = int(os.getenv("PORT", 5000))
# #     app.run(host="0.0.0.0", port=port, debug=True)


# import os
# from flask import Flask
# from flask_cors import CORS
# from dotenv import load_dotenv

# # Local imports (keep same as your project)
# from utils.error_handler import handle_error
# from utils.rate_limiter import limiter
# from routes.export import export_bp  # ✅ make sure this exists
# from routes.search import search_bp



# load_dotenv()  # load .env


# def create_app():
#     app = Flask(__name__)

#     # Enable CORS for your frontend origins
#     CORS(app, resources={r"/api/*": {"origins": ["http://localhost:3000", "http://127.0.0.1:3000"]}})

#     # Initialize rate limiter
#     limiter.init_app(app)

#     # Register blueprints
#     app.register_blueprint(search_bp, url_prefix="/api")
#     app.register_blueprint(export_bp, url_prefix="/api")  # ✅ export routes

#     # Register error handler
#     app.register_error_handler(Exception, handle_error)

#     # Root + health endpoints
#     @app.route("/")
#     def home():
#         return {
#             "message": "Infosphere API is running 🚀",
#             "endpoints": {
#                 "health": "/health",
#                 "search": "/api/search",
#                 "export_csv": "/api/export/csv",   # ✅ new info
#                 "export_pdf": "/api/export/pdf"    # ✅ new info
#             }
#         }

#     @app.route("/health")
#     def health_check():
#         return {"status": "healthy", "service": "Infosphere API", "version": "1.0.0"}

#     return app


# app = create_app()

# if __name__ == "__main__":
#     port = int(os.getenv("PORT", 5000))
#     app.run(host="0.0.0.0", port=port, debug=True)


from flask import Flask
from flask_cors import CORS
import logging

# Import blueprints
from routes.search import search_bp  # ✅ fixed import

app = Flask(__name__)
CORS(app)

# Register blueprints
app.register_blueprint(search_bp, url_prefix="/api")

# Logging setup
logging.basicConfig(level=logging.INFO)


@app.route("/")
def home():
    return {"message": "Backend is running 🚀"}


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
