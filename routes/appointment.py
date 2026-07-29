from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_required
from datetime import datetime

from models import db
from models.patient import Patient
from models.doctor import Doctor
from models.appointment import Appointment

appointment = Blueprint("appointment", __name__)


@appointment.route("/appointments")
@login_required
def appointments():

    appointments = Appointment.query.all()

    patients = Patient.query.all()

    doctors = Doctor.query.all()

    return render_template(
        "appointments.html",
        appointments=appointments,
        patients=patients,
        doctors=doctors
    )


@appointment.route("/book_appointment", methods=["POST"])
@login_required
def book_appointment():

    appointment_date = datetime.strptime(
        request.form["appointment_date"],
        "%Y-%m-%d"
    ).date()

    appointment_time = datetime.strptime(
        request.form["appointment_time"],
        "%H:%M"
    ).time()

    new_appointment = Appointment(

        patient_id=int(request.form["patient_id"]),
        doctor_id=int(request.form["doctor_id"]),
        appointment_date=appointment_date,
        appointment_time=appointment_time,
        reason=request.form["reason"],
        status="Scheduled"

    )

    db.session.add(new_appointment)
    db.session.commit()

    flash("Appointment booked successfully!")

    return redirect(url_for("appointment.appointments"))


@appointment.route("/complete/<int:id>")
@login_required
def complete(id):

    appointment = Appointment.query.get_or_404(id)

    appointment.status = "Completed"

    db.session.commit()

    flash("Appointment marked as completed.")

    return redirect(url_for("appointment.appointments"))


@appointment.route("/cancel/<int:id>")
@login_required
def cancel(id):

    appointment = Appointment.query.get_or_404(id)

    appointment.status = "Cancelled"

    db.session.commit()

    flash("Appointment has been cancelled.")

    return redirect(url_for("appointment.appointments"))