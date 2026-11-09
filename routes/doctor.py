from datetime import datetime, date

from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import current_user

from models import db
from models.appointment import Appointment
from models.availability import DoctorAvailability
from utils.helper import role_required, DAYS, fmt_time

doctor = Blueprint("doctor", __name__, url_prefix="/doctor")


def _me():
    return current_user.doctor_profile


@doctor.route("/dashboard")
@role_required("Doctor")
def dashboard():

    me = _me()

    today = date.today()

    base = Appointment.query.filter_by(doctor_id=me.id)

    upcoming = base.filter(
        Appointment.status == "Scheduled",
        Appointment.appointment_date >= today
    ).order_by(
        Appointment.appointment_date, Appointment.appointment_time
    ).limit(5).all()

    return render_template(
        "doctor_dashboard.html",
        doctor=me,
        today_count=base.filter_by(appointment_date=today, status="Scheduled").count(),
        upcoming_count=base.filter(
            Appointment.status == "Scheduled",
            Appointment.appointment_date >= today
        ).count(),
        completed_count=base.filter_by(status="Completed").count(),
        slots_count=len(me.availability),
        upcoming=upcoming,
        fmt_time=fmt_time
    )


@doctor.route("/profile", methods=["GET", "POST"])
@role_required("Doctor")
def profile():

    me = _me()

    if request.method == "POST":

        fullname = request.form.get("fullname", "").strip()
        specialization = request.form.get("specialization", "").strip()

        if not fullname or not specialization:
            flash("Name and specialization are required.", "error")
            return redirect(url_for("doctor.profile"))

        me.fullname = fullname
        me.specialization = specialization
        me.phone = request.form.get("phone", "").strip()
        me.room_number = request.form.get("room_number", "").strip()
        me.about = request.form.get("about", "").strip()
        me.available = request.form.get("available") == "on"

        current_user.fullname = fullname

        db.session.commit()

        flash("Your details have been updated.", "success")

        return redirect(url_for("doctor.profile"))

    return render_template("doctor_profile.html", doctor=me)


@doctor.route("/availability", methods=["GET", "POST"])
@role_required("Doctor")
def availability():

    me = _me()

    if request.method == "POST":

        try:
            day = int(request.form["day"])
            start = datetime.strptime(request.form["start_time"], "%H:%M").time()
            end = datetime.strptime(request.form["end_time"], "%H:%M").time()
        except (KeyError, ValueError):
            flash("Please choose a day, a start time and an end time.", "error")
            return redirect(url_for("doctor.availability"))

        if day not in range(7):
            flash("Please choose a valid day.", "error")
        elif end <= start:
            flash("The end time must be after the start time.", "error")
        elif any(
            w.day_of_week == day and start < w.end_time and end > w.start_time
            for w in me.availability
        ):
            flash("That time overlaps one you have already added for that day.", "error")
        else:
            db.session.add(DoctorAvailability(
                doctor_id=me.id, day_of_week=day, start_time=start, end_time=end
            ))
            db.session.commit()
            flash(f"Added {DAYS[day]} {fmt_time(start)} - {fmt_time(end)}.", "success")

        return redirect(url_for("doctor.availability"))

    windows = sorted(me.availability, key=lambda w: (w.day_of_week, w.start_time))

    return render_template(
        "doctor_availability.html",
        doctor=me,
        windows=windows,
        days=DAYS,
        fmt_time=fmt_time
    )


@doctor.route("/availability/delete/<int:id>")
@role_required("Doctor")
def delete_availability(id):

    window = DoctorAvailability.query.get_or_404(id)

    if window.doctor_id != _me().id:
        flash("You do not have access to that.", "error")
        return redirect(url_for("doctor.availability"))

    db.session.delete(window)
    db.session.commit()

    flash("Time removed.", "success")

    return redirect(url_for("doctor.availability"))


@doctor.route("/appointments")
@role_required("Doctor")
def appointments():

    items = Appointment.query.filter_by(doctor_id=_me().id).order_by(
        Appointment.appointment_date.desc(), Appointment.appointment_time.desc()
    ).all()

    return render_template("doctor_appointments.html", appointments=items, fmt_time=fmt_time)


def _own_appointment(id):
    appt = Appointment.query.get_or_404(id)
    return appt if appt.doctor_id == _me().id else None


@doctor.route("/complete/<int:id>")
@role_required("Doctor")
def complete(id):

    appt = _own_appointment(id)

    if appt is None:
        flash("You do not have access to that appointment.", "error")
    elif appt.status == "Scheduled":
        appt.status = "Completed"
        db.session.commit()
        flash("Appointment marked as completed.", "success")

    return redirect(url_for("doctor.appointments"))


@doctor.route("/cancel/<int:id>")
@role_required("Doctor")
def cancel(id):

    appt = _own_appointment(id)

    if appt is None:
        flash("You do not have access to that appointment.", "error")
    elif appt.status == "Scheduled":
        appt.status = "Cancelled"
        db.session.commit()
        flash("Appointment cancelled.", "success")

    return redirect(url_for("doctor.appointments"))
