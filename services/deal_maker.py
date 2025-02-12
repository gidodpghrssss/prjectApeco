import os
from typing import Dict, List, Any
import requests
from models.database import Property, PropertyImage, PropertyDocument, db

class DealMakerService:
    def __init__(self):
        self.api_key = os.getenv('NEBIUS_AI_KEY')
        self.api_url = os.getenv('NEBIUS_AI_URL')
    
    def create_deal(self, data: Dict[str, Any]) -> Property:
        """Create a new property deal with AI-enhanced description and analysis"""
        try:
            # Generate AI-enhanced description
            enhanced_description = self._generate_description(data)
            
            # Extract and analyze features
            features = self._analyze_features(data)
            
            # Create property listing
            property_listing = Property(
                title=data['title'],
                property_type=data['property_type'],
                status='available',
                price=data['price'],
                address=data['address'],
                city=data['city'],
                state=data['state'],
                zip_code=data['zip_code'],
                country=data['country'],
                square_meters=data['square_meters'],
                bedrooms=data.get('bedrooms'),
                bathrooms=data.get('bathrooms'),
                year_built=data.get('year_built'),
                description=enhanced_description,
                features=features,
                tax_rate=data.get('tax_rate'),
                maintenance_cost=data.get('maintenance_cost'),
                rental_value=self._estimate_rental_value(data)
            )
            
            db.session.add(property_listing)
            
            # Process and add images
            if 'images' in data:
                for img_data in data['images']:
                    image = PropertyImage(
                        property=property_listing,
                        url=img_data['url'],
                        is_primary=img_data.get('is_primary', False)
                    )
                    db.session.add(image)
            
            # Process and add documents
            if 'documents' in data:
                for doc_data in data['documents']:
                    document = PropertyDocument(
                        property=property_listing,
                        name=doc_data['name'],
                        document_type=doc_data['type'],
                        url=doc_data['url']
                    )
                    db.session.add(document)
            
            db.session.commit()
            return property_listing
            
        except Exception as e:
            db.session.rollback()
            raise Exception(f"Error creating deal: {str(e)}")
    
    def _generate_description(self, data: Dict[str, Any]) -> str:
        """Generate an AI-enhanced property description"""
        try:
            prompt = f"""Create an engaging and honest property description for:
            - {data['property_type']} in {data['city']}, {data['state']}
            - {data['square_meters']} square meters
            - {data.get('bedrooms', 0)} bedrooms, {data.get('bathrooms', 0)} bathrooms
            - Built in {data.get('year_built', 'N/A')}
            - Key features: {', '.join(data.get('features', []))}
            """
            
            response = requests.post(
                self.api_url,
                headers={'Authorization': f'Bearer {self.api_key}'},
                json={
                    'messages': [
                        {
                            'role': 'system',
                            'content': 'You are a professional real estate copywriter.'
                        },
                        {
                            'role': 'user',
                            'content': prompt
                        }
                    ]
                }
            )
            
            if response.status_code == 200:
                return response.json()['choices'][0]['message']['content']
            return ""
            
        except Exception as e:
            print(f"Error generating description: {str(e)}")
            return ""
    
    def _analyze_features(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """Analyze and structure property features"""
        features = {
            'basic': {
                'bedrooms': data.get('bedrooms'),
                'bathrooms': data.get('bathrooms'),
                'square_meters': data['square_meters']
            },
            'amenities': data.get('amenities', []),
            'construction': {
                'year_built': data.get('year_built'),
                'construction_type': data.get('construction_type'),
                'roof_type': data.get('roof_type')
            },
            'utilities': data.get('utilities', []),
            'outdoor': data.get('outdoor_features', []),
            'security': data.get('security_features', [])
        }
        
        return features
    
    def _estimate_rental_value(self, data: Dict[str, Any]) -> float:
        """Estimate the rental value based on property data and market analysis"""
        # Implement rental value estimation logic here
        # For now, return a simple calculation
        base_value = data['price'] * 0.005  # 0.5% of property value
        
        # Adjust based on property type and location
        if data['property_type'].lower() == 'apartment':
            base_value *= 1.1
        elif data['property_type'].lower() == 'house':
            base_value *= 0.9
        
        return round(base_value, 2)
    
    def analyze_market_value(self, property_id: int) -> Dict[str, Any]:
        """Analyze the market value and potential of a property"""
        property_listing = Property.query.get(property_id)
        if not property_listing:
            raise ValueError("Property not found")
        
        # Implement market analysis logic here
        analysis = {
            'estimated_value': property_listing.price,
            'market_trend': 'stable',
            'investment_potential': 'high',
            'comparable_properties': []
        }
        
        return analysis
