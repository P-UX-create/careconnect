from datetime import datetime, timedelta, date
from functools import wraps

from flask import redirect, url_for, flash
from flask_login import current_user, login_required

from models.appointment import Appointment
from models.availability import DoctorAvailability

DAYS = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]

SLOT_MINUTES = 30


def role_required(role):
    """Allow only logged-in users with the given role ("Patient" or "Doctor")."""

    def decorator(view):

        @wraps(view)
        @login_required
        def wrapper(*args, **kwargs):

            if current_user.role != role:
                flash("You do not have access to that page.", "error")
                return redirect(url_for("dashboard"))

            return view(*args, **kwargs)

        return wrapper

    return decorator


def fmt_time(t):
    return t.strftime("%I:%M %p").lstrip("0") if t else ""


def free_slots(doctor, day):
    """Return the list of free start times (datetime.time) for a doctor on a date."""

    windows = DoctorAvailability.query.filter_by(
        doctor_id=doctor.id,
        day_of_week=day.weekday()
    ).order_by(DoctorAvailability.start_time).all()

    booked = {
        a.appointment_time
        for a in Appointment.query.filter(
            Appointment.doctor_id == doctor.id,
            Appointment.appointment_date == day,
            Appointment.status != "Cancelled"
        )
    }

    now = datetime.now()

    slots = []

    for w in windows:

        current = datetime.combine(day, w.start_time)
        end = datetime.combine(day, w.end_time)

        while current + timedelta(minutes=SLOT_MINUTES) <= end:

            t = current.time()

            in_past = day == date.today() and current <= now

            if t not in booked and not in_past:
                slots.append(t)

            current += timedelta(minutes=SLOT_MINUTES)

    return sorted(set(slots))
