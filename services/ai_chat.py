import os
from typing import Dict, Any
import requests
from models.database import Property, UserPreference, db

class AIChatService:
    def __init__(self):
        self.api_key = os.getenv('NEBIUS_API_KEY')
        self.api_url = 'https://api.studio.nebius.ai/v1/chat/completions'
        
    def get_context(self, user_id: int = None) -> Dict[str, Any]:
        """Gather context about the user and available properties"""
        context = {
            'available_properties': Property.query.filter_by(status='available').count(),
            'price_range': self._get_price_range()
        }
        
        if user_id:
            preferences = UserPreference.query.filter_by(user_id=user_id).first()
            if preferences:
                context['user_preferences'] = preferences.other_preferences
                
        return context
    
    def _get_price_range(self) -> Dict[str, float]:
        """Get the min and max property prices"""
        result = db.session.query(
            db.func.min(Property.price),
            db.func.max(Property.price)
        ).first()
        return {'min': result[0] or 0, 'max': result[1] or 0}
    
    def analyze_user_preferences(self, user_id: int) -> Dict[str, Any]:
        """Analyze user behavior and preferences to provide personalized recommendations"""
        preferences = UserPreference.query.filter_by(user_id=user_id).first()
        viewed_properties = Property.query.join(
            Property.views
        ).filter_by(user_id=user_id).all()
        
        analysis = {
            'preferred_price_range': self._get_user_price_range(viewed_properties),
            'preferred_locations': self._analyze_locations(viewed_properties),
            'property_types': self._analyze_property_types(viewed_properties),
            'saved_preferences': preferences.other_preferences if preferences else {},
            'interaction_history': len(viewed_properties)
        }
        
        return analysis
    
    def _get_user_price_range(self, viewed_properties: list) -> Dict[str, float]:
        """Analyze user's preferred price range based on viewed properties"""
        if not viewed_properties:
            return self._get_price_range()
            
        prices = [p.price for p in viewed_properties]
        return {
            'min': min(prices),
            'max': max(prices),
            'avg': sum(prices) / len(prices)
        }
    
    def _analyze_locations(self, viewed_properties: list) -> Dict[str, int]:
        """Analyze most viewed locations"""
        locations = {}
        for prop in viewed_properties:
            locations[prop.location] = locations.get(prop.location, 0) + 1
        return dict(sorted(locations.items(), key=lambda x: x[1], reverse=True)[:5])
    
    def _analyze_property_types(self, viewed_properties: list) -> Dict[str, int]:
        """Analyze preferred property types"""
        types = {}
        for prop in viewed_properties:
            types[prop.property_type] = types.get(prop.property_type, 0) + 1
        return dict(sorted(types.items(), key=lambda x: x[1], reverse=True))

    def get_response(self, message: str, user_id: int = None) -> str:
        """Get AI response for user message with enhanced context"""
        context = self.get_context(user_id)
        user_analysis = self.analyze_user_preferences(user_id) if user_id else {}
        
        system_prompt = f"""You are a helpful real estate assistant with access to the following information:
        Currently available properties: {context['available_properties']}
        Price range: ${context['price_range']['min']} - ${context['price_range']['max']}
        """
        
        if user_analysis:
            system_prompt += f"""
            User preferences:
            - Preferred price range: ${user_analysis['preferred_price_range']['min']} - ${user_analysis['preferred_price_range']['max']}
            - Favorite locations: {', '.join(user_analysis['preferred_locations'].keys())}
            - Preferred property types: {', '.join(user_analysis['property_types'].keys())}
            """
        
        try:
            response = requests.post(
                self.api_url,
                headers={
                    'Authorization': f'Bearer {self.api_key}',
                    'Content-Type': 'application/json'
                },
                json={
                    'model': 'meta-llama/Meta-Llama-3.1-70B-Instruct',
                    'messages': [
                        {
                            'role': 'system',
                            'content': system_prompt
                        },
                        {
                            'role': 'user',
                            'content': message
                        }
                    ],
                    'temperature': 0.7,
                    'max_tokens': 250,
                    'top_p': 1,
                    'frequency_penalty': 0.2,
                    'presence_penalty': 0.1
                }
            )
            
            if response.status_code == 200:
                return response.json()['choices'][0]['message']['content']
            else:
                return "I apologize, but I'm having trouble connecting to my AI services right now. Please try again later."
                
        except Exception as e:
            print(f"Error in AI chat service: {str(e)}")
            return "I apologize, but I'm experiencing technical difficulties. Please try again later."
