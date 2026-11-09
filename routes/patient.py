from datetime import datetime, date

from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import current_user

from models import db
from models.appointment import Appointment
from models.doctor import Doctor
from utils.helper import role_required, free_slots, fmt_time, DAYS

patient = Blueprint("patient", __name__, url_prefix="/patient")


def _me():
    return current_user.patient_profile


@patient.route("/dashboard")
@role_required("Patient")
def dashboard():

    me = _me()

    today = date.today()

    base = Appointment.query.filter_by(patient_id=me.id)

    upcoming = base.filter(
        Appointment.status == "Scheduled",
        Appointment.appointment_date >= today
    ).order_by(
        Appointment.appointment_date, Appointment.appointment_time
    ).limit(5).all()

    return render_template(
        "patient_dashboard.html",
        patient=me,
        upcoming=upcoming,
        upcoming_count=base.filter(
            Appointment.status == "Scheduled",
            Appointment.appointment_date >= today
        ).count(),
        completed_count=base.filter_by(status="Completed").count(),
        doctor_count=Doctor.query.filter_by(available=True).count(),
        fmt_time=fmt_time
    )


@patient.route("/profile", methods=["GET", "POST"])
@role_required("Patient")
def profile():

    me = _me()

    if request.method == "POST":

        f = request.form

        first_name = f.get("first_name", "").strip()
        last_name = f.get("last_name", "").strip()

        if not first_name or not last_name:
            flash("First name and last name are required.", "error")
            return redirect(url_for("patient.profile"))

        dob = me.date_of_birth

        if f.get("date_of_birth"):
            try:
                dob = datetime.strptime(f["date_of_birth"], "%Y-%m-%d").date()
            except ValueError:
                flash("Please enter a valid date of birth.", "error")
                return redirect(url_for("patient.profile"))

        me.first_name = first_name
        me.last_name = last_name
        me.gender = f.get("gender") or me.gender
        me.date_of_birth = dob
        me.phone = f.get("phone", "").strip()
        me.blood_group = f.get("blood_group", "").strip()
        me.emergency_contact = f.get("emergency_contact", "").strip()
        me.address = f.get("address", "").strip()

        current_user.fullname = f"{first_name} {last_name}"

        db.session.commit()

        flash("Your details have been updated.", "success")

        return redirect(url_for("patient.profile"))

    return render_template("patient_profile.html", patient=me)


@patient.route("/doctors")
@role_required("Patient")
def doctors():

    search = request.args.get("search", "").strip()

    query = Doctor.query.filter_by(available=True)

    if search:
        like = f"%{search}%"
        query = query.filter(
            Doctor.fullname.ilike(like) | Doctor.specialization.ilike(like)
        )

    doctor_list = query.order_by(Doctor.fullname).all()

    def days_for(doc):
        return [DAYS[d][:3] for d in sorted({w.day_of_week for w in doc.availability})]

    return render_template(
        "find_doctors.html",
        doctors=doctor_list,
        search=search,
        days_for=days_for
    )


@patient.route("/doctors/<int:id>", methods=["GET", "POST"])
@role_required("Patient")
def book(id):

    doc = Doctor.query.get_or_404(id)

    windows = sorted(doc.availability, key=lambda w: (w.day_of_week, w.start_time))

    chosen = None
    slots = []
    message = None

    raw_date = request.values.get("date", "")

    if raw_date:
        try:
            chosen = datetime.strptime(raw_date, "%Y-%m-%d").date()
        except ValueError:
            message = "Please choose a valid date."

    if chosen is not None:

        if chosen < date.today():
            message = "You cannot book a date in the past."
            chosen = None
        else:
            slots = free_slots(doc, chosen)
            if not slots:
                message = (
                    f"Dr. {doc.fullname} has no free times on "
                    f"{chosen.strftime('%A, %d %B %Y')}. Please try another date."
                )

    if request.method == "POST" and chosen is not None:

        try:
            wanted = datetime.strptime(request.form.get("time", ""), "%H:%M").time()
        except ValueError:
            wanted = None

        reason = request.form.get("reason", "").strip()

        if not doc.available:
            flash("This doctor is not taking appointments right now.", "error")
        elif wanted is None or wanted not in slots:
            flash("That time is no longer available. Please pick another.", "error")
        elif not reason:
            flash("Please enter a reason for the appointment.", "error")
        else:
            appt = Appointment(
                patient_id=_me().id,
                doctor_id=doc.id,
                appointment_date=chosen,
                appointment_time=wanted,
                reason=reason,
                status="Scheduled"
            )

            db.session.add(appt)
            db.session.commit()

            flash(
                {
                    "doctor": f"Dr. {doc.fullname}",
                    "specialization": doc.specialization or "",
                    "room": doc.room_number or "",
                    "date": chosen.strftime("%A, %d %B %Y"),
                    "time": fmt_time(wanted),
                    "status": appt.status
                },
                "appointment_success"
            )

            return redirect(url_for("patient.appointments"))

        return redirect(url_for("patient.book", id=doc.id, date=chosen.isoformat()))

    return render_template(
        "book_appointment.html",
        doctor=doc,
        windows=windows,
        days=DAYS,
        chosen=chosen,
        slots=slots,
        message=message,
        today=date.today().isoformat(),
        fmt_time=fmt_time
    )


@patient.route("/appointments")
@role_required("Patient")
def appointments():

    items = Appointment.query.filter_by(patient_id=_me().id).order_by(
        Appointment.appointment_date.desc(), Appointment.appointment_time.desc()
    ).all()

    return render_template("patient_appointments.html", appointments=items, fmt_time=fmt_time)


@patient.route("/cancel/<int:id>")
@role_required("Patient")
def cancel(id):

    appt = Appointment.query.get_or_404(id)

    if appt.patient_id != _me().id:
        flash("You do not have access to that appointment.", "error")
    elif appt.status == "Scheduled":
        appt.status = "Cancelled"
        db.session.commit()
        flash("Your appointment has been cancelled.", "success")

    return redirect(url_for("patient.appointments"))
