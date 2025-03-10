from flask import Flask, render_template, send_from_directory, make_response
from config import Config
from models import db
from flask_migrate import Migrate
from routes import app_routes
from admin import setup_admin

app = Flask(__name__)
app.config.from_object(Config)

# Initialize Database
db.init_app(app)
migrate = Migrate(app, db)

# Register routes
app.register_blueprint(app_routes)

@app.route("/gallery")
def gallery():
    return render_template("gallery.html")


# Serve static files with cache control
@app.route('/static/<path:filename>')
def cached_static(filename):
    response = make_response(send_from_directory('static', filename))
    response.headers['Cache-Control'] = 'public, max-age=31536000'  # Cache for 1 year
    return response

# Setup Admin Panel
setup_admin(app)

if __name__ == '__main__':
    app.run(debug=True)
