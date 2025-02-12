from flask import Blueprint, jsonify, request
from models import Property, BlogPost
from services.ai_chat import AIChatService
from services.property_search import PropertySearchService

api_bp = Blueprint('api', __name__)
ai_chat = AIChatService()
property_search = PropertySearchService()

@api_bp.route('/chat', methods=['POST'])
def chat():
    message = request.json.get('message')
    if not message:
        return jsonify({'error': 'No message provided'}), 400
    
    try:
        response = ai_chat.get_response(message)
        return jsonify({'response': response})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@api_bp.route('/properties/search', methods=['GET', 'POST'])
def search_properties():
    if request.method == 'POST':
        filters = request.json
        if not filters:
            return jsonify({'error': 'No filters provided'}), 400
    else:
        # Handle GET request
        filters = {
            'query': request.args.get('query', ''),
            'property_type': request.args.get('type'),
            'min_price': request.args.get('min_price', type=float),
            'max_price': request.args.get('max_price', type=float),
            'location': request.args.get('location'),
            'status': request.args.get('status', 'available')
        }
        # Remove None values
        filters = {k: v for k, v in filters.items() if v is not None}
    
    try:
        results = property_search.search(filters)
        return jsonify({
            'properties': [prop.to_dict() for prop in results],
            'total': len(results)
        })
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@api_bp.route('/properties/<int:property_id>')
def get_property(property_id):
    property = Property.query.get_or_404(property_id)
    return jsonify(property.to_dict())

@api_bp.route('/blog/posts')
def get_blog_posts():
    page = request.args.get('page', 1, type=int)
    per_page = request.args.get('per_page', 10, type=int)
    
    posts = BlogPost.query.filter_by(status='published')\
        .order_by(BlogPost.published_at.desc())\
        .paginate(page=page, per_page=per_page, error_out=False)
    
    return jsonify({
        'posts': [post.to_dict() for post in posts.items],
        'total': posts.total,
        'pages': posts.pages,
        'current_page': posts.page
    })
