from flask import Blueprint, render_template, current_app
from models import Event, Sponsor
import os

app_routes = Blueprint('app_routes', __name__)

@app_routes.route('/')
def home():
    sponsors = Sponsor.query.all()  # Fetch all sponsor logos
    return render_template('index.html', sponsors=sponsors)

@app_routes.route('/events')
def events():
    all_events = Event.query.all()  # Fetch all events
    return render_template('events.html', events=all_events)

@app_routes.route('/event/<int:event_id>')
def event_detail(event_id):
    event = Event.query.get_or_404(event_id)
    return render_template('event_detail.html', event=event)

@app_routes.route('/about')
def about():
    return render_template('about.html')

@app_routes.route('/gallery')
def gallery():
    image_folder = os.path.join(current_app.static_folder, 'images')
    
    # Check if the folder exists to avoid errors
    if os.path.exists(image_folder):
        images = [f for f in os.listdir(image_folder) if f.lower().endswith(('png', 'jpg', 'jpeg', 'gif'))]
    else:
        images = []
    
    return render_template('gallery.html', images=images)

@app_routes.route('/team')
def team():
    return render_template('team.html')
