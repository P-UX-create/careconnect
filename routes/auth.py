from datetime import datetime
from urllib.parse import urlparse

from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_user, logout_user, login_required, current_user

from models import db
from models.user import User
from models.patient import Patient
from models.doctor import Doctor

auth = Blueprint("auth", __name__)


def _safe_next(target):
    """Only allow redirects back to a page on this same site."""
    if not target:
        return None

    parsed = urlparse(target)

    if parsed.scheme or parsed.netloc or not target.startswith("/"):
        return None

    return target


def _check_account_fields(username, email, password):
    """Return an error message if the account details are not acceptable."""

    if not username or not email or not password:
        return "Please fill in all the required fields."

    if len(password) < 6:
        return "Password must be at least 6 characters."

    if User.query.filter(db.func.lower(User.username) == username.lower()).first():
        return "That username is already taken."

    if User.query.filter_by(email=email).first():
        return "An account with that email already exists."

    return None


@auth.route("/login", methods=["GET", "POST"])
def login():

    role = "Doctor" if request.values.get("role", "").lower() == "doctor" else "Patient"

    if current_user.is_authenticated:
        return redirect(url_for("dashboard"))

    if request.method == "POST":

        username = request.form.get("username", "").strip()
        password = request.form.get("password", "")

        user = User.query.filter(
            db.func.lower(User.username) == username.lower()
        ).first()

        if user and user.check_password(password):

            if user.role != role:
                flash(
                    f"This account is a {user.role} account. "
                    f"Please use the \"{user.role}\" login.",
                    "error"
                )
                return render_template("login.html", role=role)

            login_user(user)

            return redirect(_safe_next(request.args.get("next")) or url_for("dashboard"))

        flash("Invalid username or password.", "error")

    return render_template("login.html", role=role)


@auth.route("/register/patient", methods=["GET", "POST"])
def register_patient():

    if current_user.is_authenticated:
        return redirect(url_for("dashboard"))

    if request.method == "POST":

        f = request.form

        first_name = f.get("first_name", "").strip()
        last_name = f.get("last_name", "").strip()
        username = f.get("username", "").strip()
        email = f.get("email", "").strip().lower()
        password = f.get("password", "")

        error = None

        if not first_name or not last_name or not f.get("gender"):
            error = "Please fill in all the required fields."
        else:
            error = _check_account_fields(username, email, password)

        dob = None

        if not error and f.get("date_of_birth"):
            try:
                dob = datetime.strptime(f["date_of_birth"], "%Y-%m-%d").date()
            except ValueError:
                error = "Please enter a valid date of birth."

        if error:
            flash(error, "error")
            return render_template("register_patient.html", form=f)

        user = User(
            fullname=f"{first_name} {last_name}",
            username=username,
            email=email,
            role="Patient"
        )

        user.set_password(password)

        db.session.add(user)
        db.session.flush()

        db.session.add(Patient(
            user_id=user.id,
            first_name=first_name,
            last_name=last_name,
            gender=f["gender"],
            date_of_birth=dob,
            phone=f.get("phone", "").strip(),
            email=email,
            blood_group=f.get("blood_group", "").strip(),
            emergency_contact=f.get("emergency_contact", "").strip(),
            address=f.get("address", "").strip()
        ))

        db.session.commit()

        flash("Account created! Please log in as a patient.", "success")

        return redirect(url_for("auth.login", role="patient"))

    return render_template("register_patient.html", form={})


@auth.route("/register/doctor", methods=["GET", "POST"])
def register_doctor():

    if current_user.is_authenticated:
        return redirect(url_for("dashboard"))

    if request.method == "POST":

        f = request.form

        fullname = f.get("fullname", "").strip()
        specialization = f.get("specialization", "").strip()
        username = f.get("username", "").strip()
        email = f.get("email", "").strip().lower()
        password = f.get("password", "")

        if not fullname or not specialization:
            error = "Please fill in all the required fields."
        else:
            error = _check_account_fields(username, email, password)

        if error:
            flash(error, "error")
            return render_template("register_doctor.html", form=f)

        user = User(
            fullname=fullname,
            username=username,
            email=email,
            role="Doctor"
        )

        user.set_password(password)

        db.session.add(user)
        db.session.flush()

        db.session.add(Doctor(
            user_id=user.id,
            fullname=fullname,
            specialization=specialization,
            phone=f.get("phone", "").strip(),
            email=email,
            room_number=f.get("room_number", "").strip(),
            about=f.get("about", "").strip()
        ))

        db.session.commit()

        flash("Account created! Please log in as a doctor.", "success")

        return redirect(url_for("auth.login", role="doctor"))

    return render_template("register_doctor.html", form={})


@auth.route("/logout")
@login_required
def logout():

    logout_user()

    flash("You have been logged out.", "success")

    return redirect(url_for("auth.login"))
