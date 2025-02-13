from flask import Flask
from models import db, User
from dotenv import load_dotenv
import os

# Load environment variables
load_dotenv()

# Create Flask app
app = Flask(__name__)

# Handle Render PostgreSQL database URL
database_url = os.getenv('DATABASE_URL')
if database_url and database_url.startswith("postgres://"):
    database_url = database_url.replace("postgres://", "postgresql://", 1)

app.config['SQLALCHEMY_DATABASE_URI'] = database_url or 'postgresql://postgres:postgres@localhost:5432/ai_real_estate'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Initialize extensions
db.init_app(app)

def init_db():
    with app.app_context():
        try:
            # Create all tables
            db.create_all()
            print("Database tables created successfully!")
            
            # Create admin user if it doesn't exist
            admin = User.query.filter_by(email='admin@airealestate.com').first()
            if not admin:
                admin = User(
                    email='admin@airealestate.com',
                    name='Admin User',
                    role='admin'
                )
                admin.set_password('admin123')  # Change this in production
                db.session.add(admin)
                db.session.commit()
                print("Admin user created successfully!")
            else:
                print("Admin user already exists.")
        except Exception as e:
            print(f"Error initializing database: {str(e)}")
            raise e

if __name__ == '__main__':
    init_db()
    print("Database initialization completed!")
