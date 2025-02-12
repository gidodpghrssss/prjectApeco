from flask import Blueprint, render_template, jsonify, request
from models.database import Property, BlogPost
from services.ai_chat import AIChatService
from services.property_search import PropertySearchService

main_bp = Blueprint('main', __name__)
ai_chat = AIChatService()
property_search = PropertySearchService()

@main_bp.route('/')
def home():
    latest_properties = Property.query.order_by(Property.created_at.desc()).limit(6).all()
    latest_posts = BlogPost.query.order_by(BlogPost.created_at.desc()).limit(3).all()
    return render_template('home.html', properties=latest_properties, posts=latest_posts)

@main_bp.route('/search')
def search():
    return render_template('search.html')

@main_bp.route('/blog')
def blog():
    posts = BlogPost.query.order_by(BlogPost.created_at.desc()).all()
    return render_template('blog.html', posts=posts)

@main_bp.route('/blog/<int:post_id>')
def blog_post(post_id):
    post = BlogPost.query.get_or_404(post_id)
    
    # Get previous and next posts
    prev_post = BlogPost.query.filter(BlogPost.id < post_id).order_by(BlogPost.id.desc()).first()
    next_post = BlogPost.query.filter(BlogPost.id > post_id).order_by(BlogPost.id.asc()).first()
    
    return render_template('blog_post.html', post=post, prev_post=prev_post, next_post=next_post)

@main_bp.route('/property/<int:property_id>')
def property_detail(property_id):
    property = Property.query.get_or_404(property_id)
    return render_template('property_detail.html', property=property)

@main_bp.route('/api/search', methods=['POST'])
def property_search_api():
    query = request.json.get('query', '')
    results = property_search.search(query)
    return jsonify(results)
