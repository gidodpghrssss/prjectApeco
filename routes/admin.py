from flask import Blueprint, render_template, jsonify, request, current_app, url_for
from flask_login import login_required, current_user
from datetime import datetime
from models.database import db, Property, User, BlogPost, Inquiry

admin_bp = Blueprint('admin', __name__)

@admin_bp.route('/dashboard')
@login_required
def dashboard():
    if current_user.role != 'admin':
        return render_template('errors/403.html'), 403
        
    stats = {
        'total_properties': Property.query.count(),
        'active_listings': Property.query.filter_by(status='available').count(),
        'total_users': User.query.count(),
        'new_inquiries': Inquiry.query.filter_by(status='new').count()
    }
    return render_template('admin/dashboard.html', stats=stats)

@admin_bp.route('/properties')
@login_required
def properties():
    if current_user.role != 'admin':
        return render_template('errors/403.html'), 403
    properties = Property.query.order_by(Property.created_at.desc()).all()
    return render_template('admin/properties.html', properties=properties)

@admin_bp.route('/properties/<int:id>')
@login_required
def get_property(id):
    if current_user.role != 'admin':
        return jsonify({'status': 'error', 'message': 'Unauthorized'}), 403
    property = Property.query.get_or_404(id)
    return jsonify({
        'status': 'success',
        'property': property.to_dict()
    })

@admin_bp.route('/properties', methods=['POST'])
@login_required
def create_property():
    if current_user.role != 'admin':
        return jsonify({'status': 'error', 'message': 'Unauthorized'}), 403
    data = request.get_json()
    property = Property(
        title=data['title'],
        description=data['description'],
        price=float(data['price']),
        location=data['location'],
        status=data['status']
    )
    db.session.add(property)
    db.session.commit()
    return jsonify({'status': 'success'})

@admin_bp.route('/properties/<int:id>', methods=['PUT'])
@login_required
def update_property(id):
    if current_user.role != 'admin':
        return jsonify({'status': 'error', 'message': 'Unauthorized'}), 403
    property = Property.query.get_or_404(id)
    data = request.get_json()
    property.title = data['title']
    property.description = data['description']
    property.price = float(data['price'])
    property.location = data['location']
    property.status = data['status']
    db.session.commit()
    return jsonify({'status': 'success'})

@admin_bp.route('/properties/<int:id>', methods=['DELETE'])
@login_required
def delete_property(id):
    if current_user.role != 'admin':
        return jsonify({'status': 'error', 'message': 'Unauthorized'}), 403
    property = Property.query.get_or_404(id)
    db.session.delete(property)
    db.session.commit()
    return jsonify({'status': 'success'})

@admin_bp.route('/blog')
@login_required
def blog():
    if current_user.role != 'admin':
        return render_template('errors/403.html'), 403
    posts = BlogPost.query.order_by(BlogPost.created_at.desc()).all()
    return render_template('admin/blog.html', posts=posts)

@admin_bp.route('/inquiries')
@login_required
def inquiries():
    if current_user.role != 'admin':
        return render_template('errors/403.html'), 403
    inquiries = Inquiry.query.order_by(Inquiry.created_at.desc()).all()
    return render_template('admin/inquiries.html', inquiries=inquiries)

@admin_bp.route('/settings')
@login_required
def settings():
    if current_user.role != 'admin':
        return render_template('errors/403.html'), 403
    return render_template('admin/settings.html')

@admin_bp.route('/recent-activity')
@login_required
def recent_activity():
    if current_user.role != 'admin':
        return jsonify({'status': 'error', 'message': 'Unauthorized'}), 403
        
    try:
        # Get recent properties
        recent_properties = Property.query.order_by(Property.created_at.desc()).limit(5).all()
        property_activities = [{
            'type': 'property',
            'title': p.title,
            'action': 'added',
            'date': p.created_at.strftime("%Y-%m-%d %H:%M") if p.created_at else datetime.now().strftime("%Y-%m-%d %H:%M"),
            'url': url_for('main.property_detail', id=p.id)
        } for p in recent_properties]

        # Get recent inquiries
        recent_inquiries = Inquiry.query.order_by(Inquiry.created_at.desc()).limit(5).all()
        inquiry_activities = [{
            'type': 'inquiry',
            'title': f'New inquiry from {i.email}',
            'action': 'received',
            'date': i.created_at.strftime("%Y-%m-%d %H:%M") if i.created_at else datetime.now().strftime("%Y-%m-%d %H:%M"),
            'url': url_for('admin.inquiries')
        } for i in recent_inquiries]

        # Get recent blog posts
        recent_posts = BlogPost.query.order_by(BlogPost.created_at.desc()).limit(5).all()
        post_activities = [{
            'type': 'blog',
            'title': p.title,
            'action': 'published',
            'date': p.created_at.strftime("%Y-%m-%d %H:%M") if p.created_at else datetime.now().strftime("%Y-%m-%d %H:%M"),
            'url': url_for('main.blog_post', id=p.id)
        } for p in recent_posts]

        # Combine all activities
        activities = property_activities + inquiry_activities + post_activities
        
        # If no activities, add a default message
        if not activities:
            activities = [{
                'type': 'info',
                'title': 'Welcome to your dashboard!',
                'action': 'system',
                'date': datetime.now().strftime("%Y-%m-%d %H:%M"),
                'url': url_for('admin.dashboard')
            }]
        
        # Sort by date
        activities.sort(key=lambda x: datetime.strptime(x["date"], "%Y-%m-%d %H:%M"), reverse=True)
        
        return jsonify(activities[:10])  # Return only last 10 activities
    except Exception as e:
        current_app.logger.error(f"Error in recent_activity: {str(e)}")
        return jsonify([{
            'type': 'error',
            'title': 'Error loading activities',
            'action': 'error',
            'date': datetime.now().strftime("%Y-%m-%d %H:%M"),
            'url': '#'
        }])
