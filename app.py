from flask import Flask, render_template, jsonify, request
from flask_login import LoginManager
from dotenv import load_dotenv
from models import db, User, Property, BlogPost
import os
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Load environment variables
load_dotenv()

app = Flask(__name__)
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY', 'your-secret-key')

# Handle Render PostgreSQL database URL
database_url = os.getenv('DATABASE_URL')
logger.info(f"Initial DATABASE_URL: {database_url}")

if not database_url:
    logger.error("No DATABASE_URL environment variable found!")
    database_url = 'postgresql://postgres:postgres@localhost:5432/ai_real_estate'

app.config['SQLALCHEMY_DATABASE_URI'] = database_url
logger.info(f"Final SQLALCHEMY_DATABASE_URI: {app.config['SQLALCHEMY_DATABASE_URI']}")
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Initialize extensions
try:
    db.init_app(app)
    with app.app_context():
        # Test the database connection
        db.engine.connect()
        logger.info("Successfully connected to the database")
        
        # Create tables
        db.create_all()
        logger.info("Database tables created successfully")

        # Create admin user if it doesn't exist
        admin = User.query.filter_by(email='admin@airealestate.com').first()
        if not admin:
            admin = User(
                email='admin@airealestate.com',
                name='Admin User',
                role='admin'
            )
            admin.set_password('admin123')  # You should change this password
            db.session.add(admin)
            db.session.commit()
            logger.info("Admin user created successfully")
        else:
            logger.info("Admin user already exists")

except Exception as e:
    logger.error(f"Error initializing database: {str(e)}")
    raise

login_manager = LoginManager(app)
login_manager.login_view = 'auth.login'

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

# Register blueprints
from routes.main import main_bp
from routes.auth import auth_bp
from routes.admin import admin_bp
from routes.api import api_bp

app.register_blueprint(main_bp)
app.register_blueprint(auth_bp, url_prefix='/auth')
app.register_blueprint(admin_bp, url_prefix='/admin')
app.register_blueprint(api_bp, url_prefix='/api')

@app.errorhandler(404)
def not_found_error(error):
    return render_template('404.html'), 404

@app.errorhandler(500)
def internal_error(error):
    db.session.rollback()
    return render_template('500.html'), 500

if __name__ == '__main__':
    app.run(debug=True)
