from flask import Blueprint, render_template, jsonify, request, current_app
from flask_login import login_required, current_user
from models.database import db, Property, User, BlogPost, Inquiry
from services.admin_ai_assistant import AdminAIAssistant
from datetime import datetime, timedelta

admin_bp = Blueprint('admin', __name__)
ai_assistant = AdminAIAssistant()

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
    properties = Property.query.order_by(Property.created_at.desc()).all()
    return render_template('admin/properties.html', properties=properties)

@admin_bp.route('/blog')
@login_required
def blog():
    posts = BlogPost.query.order_by(BlogPost.created_at.desc()).all()
    return render_template('admin/blog.html', posts=posts)

@admin_bp.route('/inquiries')
@login_required
def inquiries():
    inquiries = Inquiry.query.order_by(Inquiry.created_at.desc()).all()
    return render_template('admin/inquiries.html', inquiries=inquiries)

@admin_bp.route('/inquiries/<int:id>')
@login_required
def get_inquiry(id):
    inquiry = Inquiry.query.get_or_404(id)
    property = Property.query.get(inquiry.property_id)
    return jsonify({
        'status': 'success',
        'inquiry': {
            'id': inquiry.id,
            'property_id': inquiry.property_id,
            'property_title': property.title if property else 'Unknown Property',
            'user_email': inquiry.user_email,
            'message': inquiry.message,
            'status': inquiry.status,
            'created_at': inquiry.created_at.strftime('%Y-%m-%d %H:%M')
        }
    })

@admin_bp.route('/inquiries/<int:id>/resolve', methods=['POST'])
@login_required
def resolve_inquiry(id):
    inquiry = Inquiry.query.get_or_404(id)
    inquiry.status = 'resolved'
    db.session.commit()
    return jsonify({'status': 'success'})

@admin_bp.route('/inquiries/<int:id>', methods=['DELETE'])
@login_required
def delete_inquiry(id):
    inquiry = Inquiry.query.get_or_404(id)
    db.session.delete(inquiry)
    db.session.commit()
    return jsonify({'status': 'success'})

@admin_bp.route('/settings')
@login_required
def settings():
    return render_template('admin/settings.html')

@admin_bp.route('/recent-activity')
@login_required
def recent_activity():
    try:
        # Get recent properties
        recent_properties = Property.query.order_by(Property.created_at.desc()).limit(5).all()
        property_activities = [{
            'type': 'property',
            'title': p.title,
            'action': 'added',
            'date': p.created_at.strftime("%Y-%m-%d %H:%M") if p.created_at else datetime.now().strftime("%Y-%m-%d %H:%M")
        } for p in recent_properties]

        # Get recent inquiries
        recent_inquiries = Inquiry.query.order_by(Inquiry.created_at.desc()).limit(5).all()
        inquiry_activities = [{
            'type': 'inquiry',
            'title': f'Inquiry for property #{i.property_id}',
            'action': 'received',
            'date': i.created_at.strftime("%Y-%m-%d %H:%M") if i.created_at else datetime.now().strftime("%Y-%m-%d %H:%M")
        } for i in recent_inquiries]

        # Get recent blog posts
        recent_posts = BlogPost.query.order_by(BlogPost.created_at.desc()).limit(5).all()
        post_activities = [{
            'type': 'blog',
            'title': p.title,
            'action': 'published',
            'date': p.created_at.strftime("%Y-%m-%d %H:%M") if p.created_at else datetime.now().strftime("%Y-%m-%d %H:%M")
        } for p in recent_posts]

        # Combine all activities
        activities = property_activities + inquiry_activities + post_activities
        
        # Sort by date
        activities.sort(key=lambda x: datetime.strptime(x["date"], "%Y-%m-%d %H:%M"), reverse=True)
        
        return jsonify(activities[:10])  # Return only last 10 activities
    except Exception as e:
        current_app.logger.error(f"Error in recent_activity: {str(e)}")
        return jsonify({"error": str(e)}), 500

@admin_bp.route('/ai-assistant', methods=['POST'])
@login_required
def ai_assistant_command():
    data = request.get_json()
    command = data.get('command')
    
    if not command:
        return jsonify({"status": "error", "message": "No command provided"})
        
    result = ai_assistant.process_command(command)
    return jsonify(result)
