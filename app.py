import cloudinary
from flask import Flask, render_template
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

# Setup Admin Panel
setup_admin(app)

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=10000)
