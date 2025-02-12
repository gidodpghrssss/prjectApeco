from app import app, db
from models.database import User

def create_admin_user():
    with app.app_context():
        # Check if admin already exists
        admin = User.query.filter_by(email='admin@airealestate.com').first()
        if not admin:
            admin = User(
                email='admin@airealestate.com',
                name='Admin User',
                role='admin'
            )
            admin.set_password('admin123')  # Set a default password
            db.session.add(admin)
            db.session.commit()
            print("Admin user created successfully!")
        else:
            print("Admin user already exists!")

if __name__ == '__main__':
    create_admin_user()
