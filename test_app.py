import unittest
from app import app, db
from models.database import User, Property, BlogPost, PropertyImage, UserPreference
from services.ai_chat import AIChatService
import os
from dotenv import load_dotenv

load_dotenv()

class TestAIRealEstate(unittest.TestCase):
    def setUp(self):
        app.config['TESTING'] = True
        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
        self.client = app.test_client()
        self.app_context = app.app_context()
        self.app_context.push()
        db.create_all()

    def tearDown(self):
        db.session.remove()
        db.drop_all()
        self.app_context.pop()

    def test_database_models(self):
        # Test user creation
        user = User(
            email='test@example.com',
            name='Test User',
            role='user'
        )
        user.set_password('password123')
        db.session.add(user)
        db.session.commit()
        self.assertIsNotNone(User.query.filter_by(email='test@example.com').first())

        # Test property creation
        property = Property(
            title='Test Property',
            description='A test property',
            price=500000,
            property_type='House',
            status='available',
            city='Test City'
        )
        db.session.add(property)
        db.session.commit()
        self.assertIsNotNone(Property.query.filter_by(title='Test Property').first())

    def test_auth_routes(self):
        # Test registration
        response = self.client.post('/auth/register', data={
            'email': 'test@example.com',
            'password': 'password123',
            'first_name': 'Test',
            'last_name': 'User'
        }, follow_redirects=True)
        self.assertEqual(response.status_code, 200)
        user = User.query.filter_by(email='test@example.com').first()
        self.assertIsNotNone(user)
        self.assertEqual(user.name, 'Test User')

        # Test login
        response = self.client.post('/auth/login', data={
            'email': 'test@example.com',
            'password': 'password123'
        }, follow_redirects=True)
        self.assertEqual(response.status_code, 200)

    def test_ai_chat_service(self):
        if not os.getenv('NEBIUS_API_KEY'):
            self.skipTest("Nebius API key not found in environment")
            
        chat_service = AIChatService()
        
        # Test context gathering
        context = chat_service.get_context()
        self.assertIn('available_properties', context)
        self.assertIn('price_range', context)

        # Test AI response
        response = chat_service.get_response("What properties are available?")
        self.assertIsInstance(response, str)
        self.assertNotEqual(response, "")

    def test_property_search(self):
        # Create test user
        user = User(
            email='test@example.com',
            name='Test User',
            role='user'
        )
        user.set_password('password123')
        db.session.add(user)
        
        # Create test properties
        properties = [
            Property(
                title=f'Test Property {i}',
                description=f'Test description {i}',
                price=500000 + i * 100000,
                property_type='House',
                status='available',
                city='Test City'
            ) for i in range(3)
        ]
        db.session.add_all(properties)
        db.session.commit()

        # Test property search
        response = self.client.get('/api/properties/search?query=Test')
        self.assertEqual(response.status_code, 200)
        data = response.get_json()
        self.assertGreater(len(data['properties']), 0)

if __name__ == '__main__':
    unittest.main()
