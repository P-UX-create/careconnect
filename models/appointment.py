from models import db


class Appointment(db.Model):
    __tablename__ = "appointments"

    id = db.Column(db.Integer, primary_key=True)

    patient_id = db.Column(db.Integer, db.ForeignKey("patients.id"))

    doctor_id = db.Column(db.Integer, db.ForeignKey("doctors.id"))

    appointment_date = db.Column(db.Date)

    appointment_time = db.Column(db.Time)

    reason = db.Column(db.Text)

    status = db.Column(db.String(30), default="Pending")

    patient = db.relationship("Patient", backref="appointments")

    doctor = db.relationship("Doctor", backref="appointments")