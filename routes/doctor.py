from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_required

from models import db
from models.doctor import Doctor

doctor = Blueprint("doctor", __name__)


@doctor.route("/doctors")
@login_required
def doctors():

    doctors = Doctor.query.all()

    return render_template(
        "doctors.html",
        doctors=doctors
    )


@doctor.route("/add_doctor", methods=["POST"])
@login_required
def add_doctor():

    doctor = Doctor(

        fullname=request.form["fullname"],

        specialization=request.form["specialization"],

        phone=request.form["phone"],

        email=request.form["email"],

        room_number=request.form["room_number"]

    )

    db.session.add(doctor)

    db.session.commit()

    flash("Doctor registered successfully!")

    return redirect(url_for("doctor.doctors"))



@doctor.route("/edit_doctor/<int:id>", methods=["GET", "POST"])
@login_required
def edit_doctor(id):

    doctor_data = Doctor.query.get_or_404(id)

    if request.method == "POST":

        doctor_data.fullname = request.form["fullname"]
        doctor_data.specialization = request.form["specialization"]
        doctor_data.phone = request.form["phone"]
        doctor_data.email = request.form["email"]
        doctor_data.room_number = request.form["room_number"]

        db.session.commit()

        flash("Doctor updated successfully!")

        return redirect(url_for("doctor.doctors"))

    return render_template(
        "edit_doctor.html",
        doctor=doctor_data
    )



@doctor.route("/delete_doctor/<int:id>")
@login_required
def delete_doctor(id):

    doctor_data = Doctor.query.get_or_404(id)

    db.session.delete(doctor_data)

    db.session.commit()

    flash("Doctor deleted successfully!")

    return redirect(url_for("doctor.doctors"))