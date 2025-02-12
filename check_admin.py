from app import app, db
from models.database import User
from werkzeug.security import generate_password_hash

def check_and_reset_admin():
    with app.app_context():
        # Get admin user
        admin = User.query.filter_by(email='admin@airealestate.com').first()
        if admin:
            # Reset password
            admin.password_hash = generate_password_hash('admin123')
            db.session.commit()
            print(f"Admin details:")
            print(f"Email: {admin.email}")
            print(f"Name: {admin.name}")
            print(f"Role: {admin.role}")
            print("Password has been reset to: admin123")
        else:
            print("No admin user found!")

if __name__ == '__main__':
    check_and_reset_admin()
