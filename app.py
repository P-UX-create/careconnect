from flask import Flask,render_template, redirect, url_for
from flask_login import login_required

from config import Config
from models import db, login_manager

from models.user import User
from models.patient import Patient
from models.doctor import Doctor
from models.appointment import Appointment
from models.medical_record import MedicalRecord

from routes.auth import auth
from routes.patient import patient
from routes.doctor import doctor
from routes.appointment import appointment
from routes.report import report

app = Flask(__name__)

app.config.from_object(Config)

db.init_app(app)
login_manager.init_app(app)

app.register_blueprint(auth)
app.register_blueprint(patient)
app.register_blueprint(doctor)
app.register_blueprint(appointment)
app.register_blueprint(report)


with app.app_context():

        db.create_all()

        if User.query.filter_by(username="careconnect").first() is None:

            admin = User(
                fullname="System Administrator",
                username="careconnect",
                email="admin@careconnect.com",
                role="Administrator"
            )

            admin.set_password("careconnect123")

            db.session.add(admin)
            db.session.commit()

            print("Default admin account created.")



@app.route("/")
def home():
    return redirect(url_for("auth.login"))


@app.route("/dashboard")
@login_required
def dashboard():

    return render_template(
        "dashboard.html",
        patient_count=Patient.query.count(),
        doctor_count=Doctor.query.count(),
        appointment_count=Appointment.query.count()
    )


@app.errorhandler(404)
def page_not_found(error):

    return render_template("404.html"),404


@app.errorhandler(500)
def internal_server(error):

    return render_template("500.html"),500


if __name__ == "__main__":

    app.run(debug=True)