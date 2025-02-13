from flask import Blueprint, render_template, request, flash, redirect, url_for, jsonify
from flask_login import login_required, current_user
from models.database import db, BlogPost, Property, User, Inquiry
from services.blog_generator import BlogGeneratorService
from services.deal_maker import DealMakerService
from services.admin_ai_assistant import AdminAIAssistant
import os
from datetime import datetime, timedelta
import schedule
import threading
import time

admin_bp = Blueprint('admin', __name__, url_prefix='/admin')
blog_generator = BlogGeneratorService()
deal_maker = DealMakerService()
ai_assistant = AdminAIAssistant()

def check_admin():
    return current_user.is_authenticated and current_user.role == 'admin'

@admin_bp.before_request
def before_request():
    if not check_admin():
        flash('Access denied. Admin privileges required.', 'error')
        return redirect(url_for('main.home'))

@admin_bp.route('/dashboard')
@login_required
def dashboard():
    stats = {
        'total_properties': Property.query.count(),
        'active_listings': Property.query.filter_by(status='available').count(),
        'total_users': User.query.count(),
        'new_inquiries': Inquiry.query.filter_by(status='new').count(),
        'blog_posts': BlogPost.query.count()
    }
    return render_template('admin/dashboard.html', stats=stats)

@admin_bp.route('/settings', methods=['GET', 'POST'])
@login_required
def settings():
    if request.method == 'POST':
        # Update API settings
        api_key = request.form.get('nebius_api_key')
        if api_key and api_key != '•' * 20:  # Only update if changed
            os.environ['NEBIUS_API_KEY'] = api_key
            
        # Update blog settings
        posts_per_day = request.form.get('posts_per_day', type=int)
        days_interval = request.form.get('days_interval', type=int)
        
        if posts_per_day and days_interval:
            update_blog_schedule(posts_per_day, days_interval)
            
        flash('Settings updated successfully!', 'success')
        return redirect(url_for('admin.settings'))
        
    return render_template('admin/settings.html',
                         nebius_api_key=bool(os.getenv('NEBIUS_API_KEY')),
                         posts_per_day=2,
                         days_interval=1,
                         blog_categories=get_blog_categories())

@admin_bp.route('/blog')
@login_required
def blog():
    posts = BlogPost.query.order_by(BlogPost.created_at.desc()).all()
    return render_template('admin/blog.html', posts=posts)

@admin_bp.route('/blog/generate', methods=['POST'])
@login_required
def generate_blog():
    try:
        num_posts = int(request.form.get('num_posts', 1))
        posts = blog_generator.generate_blog_posts(num_posts)
        return jsonify({
            'status': 'success',
            'message': f'Generated {len(posts)} blog posts successfully',
            'posts': [{'id': p.id, 'title': p.title} for p in posts]
        })
    except Exception as e:
        return jsonify({
            'status': 'error',
            'message': str(e)
        }), 500

@admin_bp.route('/blog/edit/<int:post_id>', methods=['GET', 'POST'])
@login_required
def edit_blog_post(post_id):
    post = BlogPost.query.get_or_404(post_id)
    if request.method == 'POST':
        post.title = request.form['title']
        post.content = request.form['content']
        post.summary = request.form['summary']
        db.session.commit()
        flash('Blog post updated successfully!', 'success')
        return redirect(url_for('admin.blog'))
    return render_template('admin/edit_blog.html', post=post)

@admin_bp.route('/properties')
@login_required
def properties():
    properties = Property.query.order_by(Property.created_at.desc()).all()
    return render_template('admin/properties.html', properties=properties)

@admin_bp.route('/property/create', methods=['GET', 'POST'])
@login_required
def create_property():
    if request.method == 'POST':
        try:
            property_data = {
                'title': request.form['title'],
                'property_type': request.form['property_type'],
                'price': float(request.form['price']),
                'address': request.form['address'],
                'city': request.form['city'],
                'state': request.form['state'],
                'zip_code': request.form['zip_code'],
                'country': request.form['country'],
                'square_meters': float(request.form['square_meters']),
                'bedrooms': int(request.form.get('bedrooms', 0)),
                'bathrooms': float(request.form.get('bathrooms', 0)),
                'year_built': int(request.form.get('year_built', 0)),
                'features': request.form.getlist('features[]'),
                'images': process_images(request.files.getlist('images'))
            }
            
            property_listing = deal_maker.create_deal(property_data)
            flash('Property created successfully!', 'success')
            return redirect(url_for('admin.properties'))
            
        except Exception as e:
            flash(f'Error creating property: {str(e)}', 'error')
            
    return render_template('admin/create_property.html')

@admin_bp.route('/ai-assistant', methods=['POST'])
@login_required
def ai_assistant_command():
    if not check_admin():
        return jsonify({"status": "error", "message": "Admin access required"}), 403
    
    command = request.json.get('command')
    if not command:
        return jsonify({"status": "error", "message": "No command provided"}), 400
    
    result = ai_assistant.process_command(command)
    return jsonify(result)

@admin_bp.route('/recent-activity')
@login_required
def recent_activity():
    if not check_admin():
        return jsonify([]), 403
    
    # Get recent activities from various sources
    recent_properties = Property.query.order_by(Property.created_at.desc()).limit(5).all()
    recent_inquiries = Inquiry.query.order_by(Inquiry.created_at.desc()).limit(5).all()
    recent_users = User.query.order_by(User.created_at.desc()).limit(5).all()
    
    activities = []
    
    for prop in recent_properties:
        activities.append({
            "date": prop.created_at.strftime("%Y-%m-%d %H:%M"),
            "type": "Property",
            "description": f"New property listed: {prop.title}",
            "status": prop.status,
            "status_class": "success" if prop.status == "available" else "secondary"
        })
    
    for inquiry in recent_inquiries:
        activities.append({
            "date": inquiry.created_at.strftime("%Y-%m-%d %H:%M"),
            "type": "Inquiry",
            "description": f"New inquiry from {inquiry.user_email}",
            "status": inquiry.status,
            "status_class": "warning" if inquiry.status == "new" else "info"
        })
    
    for user in recent_users:
        activities.append({
            "date": user.created_at.strftime("%Y-%m-d %H:%M"),
            "type": "User",
            "description": f"New user registered: {user.email}",
            "status": "active",
            "status_class": "primary"
        })
    
    # Sort by date
    activities.sort(key=lambda x: datetime.strptime(x["date"], "%Y-%m-%d %H:%M"), reverse=True)
    return jsonify(activities[:10])  # Return most recent 10 activities

def get_blog_categories():
    return [
        {'id': 1, 'name': 'Market Trends', 'enabled': True},
        {'id': 2, 'name': 'Investment Tips', 'enabled': True},
        {'id': 3, 'name': 'Property Management', 'enabled': True},
        {'id': 4, 'name': 'Real Estate Technology', 'enabled': True},
        {'id': 5, 'name': 'Home Improvement', 'enabled': True},
        {'id': 6, 'name': 'Legal & Regulations', 'enabled': True}
    ]

def update_blog_schedule(posts_per_day, days_interval):
    schedule.clear()
    
    def generate_posts():
        blog_generator.generate_blog_posts(posts_per_day)
    
    # Schedule post generation
    schedule.every(days_interval).days.do(generate_posts)
    
    # Start the scheduler in a background thread if not already running
    if not hasattr(update_blog_schedule, 'scheduler_thread'):
        def run_scheduler():
            while True:
                schedule.run_pending()
                time.sleep(60)
        
        update_blog_schedule.scheduler_thread = threading.Thread(target=run_scheduler)
        update_blog_schedule.scheduler_thread.daemon = True
        update_blog_schedule.scheduler_thread.start()

def process_images(images):
    """Process and store uploaded images"""
    image_data = []
    for image in images:
        if image and allowed_file(image.filename):
            filename = secure_filename(image.filename)
            filepath = os.path.join('static', 'uploads', 'properties', filename)
            image.save(filepath)
            image_data.append({
                'url': url_for('static', filename=f'uploads/properties/{filename}'),
                'is_primary': len(image_data) == 0  # First image is primary
            })
    return image_data

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in {'png', 'jpg', 'jpeg', 'gif'}
