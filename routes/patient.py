from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_required
from datetime import datetime

from models import db
from models.patient import Patient

patient = Blueprint("patient", __name__)


@patient.route("/patients")
@login_required
def patients():

    all_patients = Patient.query.all()

    return render_template(
        "patients.html",
        patients=all_patients
    )

@patient.route("/add_patient", methods=["POST"])
@login_required
def add_patient():

    dob = None

    if request.form.get("date_of_birth"):
        dob = datetime.strptime(
            request.form["date_of_birth"],
            "%Y-%m-%d"
        ).date()

    new_patient = Patient(

        first_name=request.form["first_name"],

        last_name=request.form["last_name"],

        gender=request.form["gender"],

        phone=request.form["phone"],

        email=request.form["email"],

        blood_group=request.form["blood_group"],

        emergency_contact=request.form["emergency_contact"],

        address=request.form["address"]

    )

    db.session.add(new_patient)

    db.session.commit()


    flash("Patient registered successfully!")


    return redirect(url_for("patient.patients"))


@patient.route("/edit_patient/<int:id>", methods=["GET", "POST"])
@login_required
def edit_patient(id):

    patient_data = Patient.query.get_or_404(id)

    if request.method == "POST":

        patient_data.first_name = request.form["first_name"]
        patient_data.last_name = request.form["last_name"]
        patient_data.gender = request.form["gender"]
        patient_data.phone = request.form["phone"]
        patient_data.email = request.form["email"]
        patient_data.address = request.form["address"]

        db.session.commit()

        flash("Patient updated successfully!")

        return redirect(url_for("patient.patients"))

    return render_template("edit_patient.html", patient=patient_data)



@patient.route("/delete_patient/<int:id>")
@login_required
def delete_patient(id):

    patient_data = Patient.query.get_or_404(id)

    db.session.delete(patient_data)

    db.session.commit()

    flash("Patient deleted successfully!")

    return redirect(url_for("patient.patients"))