import cloudinary
import cloudinary.uploader
from flask_admin import Admin, AdminIndexView, expose
from flask_admin.contrib.sqla import ModelView
from flask_wtf.file import FileAllowed, FileField
from flask import redirect, url_for, request, flash, render_template
from flask_login import LoginManager, login_user, logout_user, login_required, current_user
from werkzeug.security import check_password_hash
from wtforms import StringField, TextAreaField
from wtforms.validators import DataRequired
from models import db, Event, User, Sponsor
from config import Config
import os

# Initialize Flask-Login
login_manager = LoginManager()
login_manager.login_view = "admin.admin_login"

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

class MyAdminIndexView(AdminIndexView):
    @expose("/")
    def index(self):
        if not current_user.is_authenticated:
            return redirect(url_for("admin.admin_login"))
        return super().index()

class SecureModelView(ModelView):
    def is_accessible(self):
        return current_user.is_authenticated

    def inaccessible_callback(self, name, **kwargs):
        return redirect(url_for("admin.admin_login"))

# Function to Upload Image to Cloudinary
def upload_image_to_cloudinary(file):
    """Uploads an image file to Cloudinary and returns the URL."""
    if not file or file.filename.strip() == "":  
        flash("No file selected for upload.", "warning")
        return None

    # Cloudinary configuration inside the function for security
    cloudinary.config(
        cloud_name=os.getenv("CLOUDINARY_CLOUD_NAME", Config.CLOUDINARY_CLOUD_NAME),
        api_key=os.getenv("CLOUDINARY_API_KEY", Config.CLOUDINARY_API_KEY),
        api_secret=os.getenv("CLOUDINARY_API_SECRET", Config.CLOUDINARY_API_SECRET),
        secure=True
    )

    try:
        upload_result = cloudinary.uploader.upload(file.stream)
        return upload_result.get("secure_url")
    except Exception as e:
        flash(f"Image upload failed: {str(e)}", "danger")
        print(f"Cloudinary Upload Error: {str(e)}")  # Debugging info in terminal
        return None

# Custom Form for EventAdmin
class EventForm(SecureModelView.form_base_class):
    title = StringField("Title", validators=[DataRequired()])
    date = StringField("Date", validators=[DataRequired()])
    time = StringField("Time", validators=[DataRequired()])
    venue = StringField("Venue", validators=[DataRequired()])
    registration_fees = StringField("Registration Fees")
    description = TextAreaField("Description", validators=[DataRequired()])
    image = FileField("Upload Image", validators=[FileAllowed(["jpg", "png", "jpeg"], "Images only!")])
    rules = TextAreaField("Rules")
    registration_link = StringField("Registration Link")
    team_size = StringField("Team Size")

# Event Admin - Upload Image to Cloudinary
class EventAdmin(SecureModelView):
    form = EventForm

    def on_model_change(self, form, model, is_created):
        if form.image.data:
            image_url = upload_image_to_cloudinary(form.image.data)
            if image_url:
                model.image = image_url  # Store Cloudinary URL in DB
            else:
                flash("Image upload failed!", "danger")

    form_columns = ["title", "date", "time", "venue", "registration_fees", "description", "image", "rules", "registration_link", "team_size"]

# Custom Form for SponsorAdmin
class SponsorForm(SecureModelView.form_base_class):
    name = StringField("Name", validators=[DataRequired()])
    logo = FileField("Upload Logo", validators=[FileAllowed(["jpg", "png", "jpeg"], "Images only!")])

# Sponsor Admin - Upload Logo to Cloudinary
class SponsorAdmin(SecureModelView):
    form = SponsorForm

    def on_model_change(self, form, model, is_created):
        if form.logo.data:
            logo_url = upload_image_to_cloudinary(form.logo.data)
            if logo_url:
                model.logo = logo_url  # Store Cloudinary URL in DB
            else:
                flash("Logo upload failed!", "danger")

    form_columns = ["name", "logo"]

# Initialize Flask-Admin
admin = Admin(index_view=MyAdminIndexView())

def setup_admin(app):
    admin.init_app(app)
    login_manager.init_app(app)
    
    admin.add_view(EventAdmin(Event, db.session))  
    admin.add_view(SponsorAdmin(Sponsor, db.session))  

    @app.route("/admin/login", methods=["GET", "POST"])
    def admin_login():
        if current_user.is_authenticated:
            return redirect(url_for("admin.index"))
        
        if request.method == "POST":
            username = request.form["username"]
            password = request.form["password"]
            user = User.query.filter_by(username=username).first()

            if user and check_password_hash(user.password, password):  # Fixed check
                login_user(user)
                return redirect(url_for("admin.index"))
            else:
                flash("Invalid username or password!", "danger")

        return render_template("admin_login.html")

    @app.route("/admin/logout")
    @login_required
    def admin_logout():
        logout_user()
        return redirect(url_for("admin_login"))
