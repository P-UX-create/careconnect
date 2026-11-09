from flask import Flask, render_template, redirect, url_for
from flask_login import login_required, current_user

from config import Config
from models import db, login_manager

from models.user import User
from models.patient import Patient
from models.doctor import Doctor
from models.availability import DoctorAvailability
from models.appointment import Appointment
from models.medical_record import MedicalRecord

from routes.auth import auth
from routes.patient import patient
from routes.doctor import doctor

app = Flask(__name__)

app.config.from_object(Config)

db.init_app(app)
login_manager.init_app(app)

app.register_blueprint(auth)
app.register_blueprint(patient)
app.register_blueprint(doctor)


# Create all tables (SQLite file is made automatically on first run).
with app.app_context():
    db.create_all()


@app.route("/")
def home():
    return render_template("index.html")


@app.route("/dashboard")
@login_required
def dashboard():
    """Send each user to the dashboard for their own role."""

    if current_user.role == "Doctor":
        return redirect(url_for("doctor.dashboard"))

    return redirect(url_for("patient.dashboard"))


@app.context_processor
def inject_globals():
    return {"db_name": db.engine.dialect.name.replace("postgresql", "PostgreSQL").replace("sqlite", "SQLite")}


@app.errorhandler(404)
def page_not_found(error):

    return render_template("404.html"), 404


@app.errorhandler(500)
def internal_server(error):

    db.session.rollback()

    return render_template("500.html"), 500


if __name__ == "__main__":

    app.run(debug=True)
