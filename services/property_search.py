from typing import List, Dict, Any
from sqlalchemy import or_
from models.database import Property, PropertyImage

class PropertySearchService:
    def search(self, filters: Dict[str, Any]) -> List[Property]:
        """
        Search properties based on filters
        """
        query = Property.query
        
        # Apply status filter
        if filters.get('status'):
            query = query.filter(Property.status == filters['status'])
            
        # Apply text search
        if filters.get('query'):
            search_term = f"%{filters['query']}%"
            query = query.filter(or_(
                Property.title.ilike(search_term),
                Property.description.ilike(search_term),
                Property.property_type.ilike(search_term),
                Property.city.ilike(search_term),
                Property.state.ilike(search_term),
                Property.address.ilike(search_term)
            ))
        
        # Apply filters
        if filters.get('min_price'):
            query = query.filter(Property.price >= filters['min_price'])
        
        if filters.get('max_price'):
            query = query.filter(Property.price <= filters['max_price'])
            
        if filters.get('property_type'):
            query = query.filter(Property.property_type == filters['property_type'])
            
        if filters.get('min_square_meters'):
            query = query.filter(Property.square_meters >= filters['min_square_meters'])
            
        if filters.get('max_square_meters'):
            query = query.filter(Property.square_meters <= filters['max_square_meters'])
            
        if filters.get('bedrooms'):
            query = query.filter(Property.bedrooms >= filters['bedrooms'])
            
        if filters.get('bathrooms'):
            query = query.filter(Property.bathrooms >= filters['bathrooms'])
            
        if filters.get('location'):
            location_term = f"%{filters['location']}%"
            query = query.filter(or_(
                Property.city.ilike(location_term),
                Property.state.ilike(location_term),
                Property.address.ilike(location_term)
            ))
        
        # Order by relevance and price
        if filters.get('sort_by') == 'price_asc':
            query = query.order_by(Property.price.asc())
        elif filters.get('sort_by') == 'price_desc':
            query = query.order_by(Property.price.desc())
        else:
            query = query.order_by(Property.created_at.desc())
        
        # Execute query
        return query.all()
    
    def get_recommended_properties(self, user_preferences: Dict[str, Any]) -> List[Dict[str, Any]]:
        """
        Get recommended properties based on user preferences
        """
        query = Property.query.filter_by(status='available')
        
        if user_preferences.get('preferred_locations'):
            locations = user_preferences['preferred_locations']
            query = query.filter(or_(
                *[Property.city.ilike(f"%{loc}%") for loc in locations]
            ))
        
        if user_preferences.get('min_price'):
            query = query.filter(Property.price >= user_preferences['min_price'])
            
        if user_preferences.get('max_price'):
            query = query.filter(Property.price <= user_preferences['max_price'])
        
        # Add more preference-based filters
        
        # Order by relevance
        query = query.order_by(Property.created_at.desc())
        
        properties = query.limit(10).all()
        return [prop.to_dict() for prop in properties]
