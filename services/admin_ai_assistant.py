from models.database import db, Property, User, BlogPost, Inquiry
from sqlalchemy import text
import re
from datetime import datetime, timedelta

class AdminAIAssistant:
    def __init__(self):
        self.commands = {
            r'show all properties(?: in (?P<location>\w+))?': self.show_properties,
            r'update (?P<field>\w+) of property (?:ID )?(?P<id>\d+) to (?P<value>.+)': self.update_property,
            r'delete (?:all )?(?P<type>\w+)(?: older than (?P<age>\d+) (?P<unit>\w+))?': self.delete_items,
            r'generate (?:a )?report of (?P<report_type>.+)': self.generate_report,
            r'create (?:new )?property(?: with )?(?P<details>.+)?': self.create_property,
            r'show (?:all )?users': self.show_users,
            r'show (?:all )?inquiries': self.show_inquiries,
        }

    def process_command(self, command):
        """Process natural language command and execute corresponding database operation"""
        try:
            for pattern, handler in self.commands.items():
                match = re.match(pattern, command.lower())
                if match:
                    return handler(**match.groupdict())
            return {"status": "error", "message": "Command not recognized. Please try a different command."}
        except Exception as e:
            return {"status": "error", "message": f"Error executing command: {str(e)}"}

    def show_properties(self, location=None):
        """Show properties, optionally filtered by location"""
        query = Property.query
        if location:
            query = query.filter(Property.location.ilike(f'%{location}%'))
        
        properties = query.all()
        return {
            "status": "success",
            "data": [
                {
                    "id": p.id,
                    "title": p.title,
                    "price": p.price,
                    "location": p.location,
                    "status": p.status
                } for p in properties
            ]
        }

    def create_property(self, details=None):
        """Create a new property with optional details"""
        try:
            property_data = {
                'title': 'New Property',
                'description': 'Property description',
                'price': 0,
                'location': 'Unknown',
                'status': 'available'
            }

            if details:
                pairs = [pair.strip() for pair in details.split(',')]
                for pair in pairs:
                    if ':' in pair:
                        key, value = pair.split(':', 1)
                        key = key.strip().lower()
                        value = value.strip()
                        if key == 'price':
                            value = float(value.replace('$', '').replace(',', ''))
                        if key in property_data:
                            property_data[key] = value

            new_property = Property(**property_data)
            db.session.add(new_property)
            db.session.commit()

            return {
                "status": "success",
                "message": f"Created new property: {new_property.title}",
                "data": {
                    "id": new_property.id,
                    "title": new_property.title,
                    "price": new_property.price,
                    "location": new_property.location,
                    "status": new_property.status
                }
            }
        except Exception as e:
            db.session.rollback()
            return {"status": "error", "message": f"Error creating property: {str(e)}"}

    def update_property(self, field, id, value):
        """Update a specific field of a property"""
        property = Property.query.get(id)
        if not property:
            return {"status": "error", "message": f"Property with ID {id} not found"}
        
        try:
            if field == 'price':
                value = float(value.replace('$', '').replace(',', ''))
            setattr(property, field, value)
            db.session.commit()
            return {"status": "success", "message": f"Updated {field} of property {id}"}
        except Exception as e:
            db.session.rollback()
            return {"status": "error", "message": str(e)}

    def delete_items(self, type, age=None, unit=None):
        """Delete items of specified type with optional age filter"""
        try:
            if type == 'properties':
                query = Property.query
            elif type == 'inquiries':
                query = Inquiry.query
            elif type == 'listings':
                query = Property.query.filter_by(status='inactive')
            else:
                return {"status": "error", "message": f"Unknown type: {type}"}

            if age and unit:
                if unit in ['days', 'months', 'years']:
                    delta = {
                        'days': timedelta(days=int(age)),
                        'months': timedelta(days=int(age) * 30),
                        'years': timedelta(days=int(age) * 365)
                    }
                    cutoff_date = datetime.now() - delta[unit]
                    query = query.filter(Property.created_at < cutoff_date)

            items = query.all()
            count = len(items)
            for item in items:
                db.session.delete(item)
            db.session.commit()
            
            return {"status": "success", "message": f"Deleted {count} {type}"}
        except Exception as e:
            db.session.rollback()
            return {"status": "error", "message": str(e)}

    def generate_report(self, report_type):
        """Generate various types of reports"""
        try:
            if 'sales' in report_type:
                match = re.search(r'Q(\d) (\d{4})', report_type)
                if match:
                    quarter = int(match.group(1))
                    year = int(match.group(2))
                    start_date = datetime(year, (quarter - 1) * 3 + 1, 1)
                    end_date = datetime(year, quarter * 3 + 1, 1) - timedelta(days=1)
                    
                    sales = Property.query.filter(
                        Property.status == 'sold',
                        Property.updated_at.between(start_date, end_date)
                    ).all()
                    
                    total_sales = len(sales)
                    total_value = sum(p.price for p in sales)
                    
                    return {
                        "status": "success",
                        "data": {
                            "period": f"Q{quarter} {year}",
                            "total_sales": total_sales,
                            "total_value": f"${total_value:,.2f}",
                            "average_price": f"${(total_value/total_sales if total_sales else 0):,.2f}"
                        }
                    }
            return {"status": "error", "message": "Report type not supported"}
        except Exception as e:
            return {"status": "error", "message": str(e)}

    def show_users(self):
        """Show all users"""
        users = User.query.all()
        return {
            "status": "success",
            "data": [
                {
                    "id": u.id,
                    "name": u.name,
                    "email": u.email,
                    "role": u.role
                } for u in users
            ]
        }

    def show_inquiries(self):
        """Show all inquiries"""
        inquiries = Inquiry.query.all()
        return {
            "status": "success",
            "data": [
                {
                    "id": i.id,
                    "property_id": i.property_id,
                    "user_email": i.user_email,
                    "status": i.status,
                    "created_at": i.created_at.strftime("%Y-%m-%d %H:%M:%S")
                } for i in inquiries
            ]
        }
