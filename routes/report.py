from flask import Blueprint, render_template
from flask_login import login_required

from models.patient import Patient
from models.doctor import Doctor
from models.appointment import Appointment

report = Blueprint("report", __name__)


@report.route("/reports")
@login_required
def reports():

    total_patients = Patient.query.count()

    total_doctors = Doctor.query.count()

    total_appointments = Appointment.query.count()

    return render_template(

        "reports.html",

        patients=total_patients,

        doctors=total_doctors,

        appointments=total_appointments

    )