from models import db


class MedicalRecord(db.Model):
    __tablename__ = "medical_records"

    id = db.Column(db.Integer, primary_key=True)

    patient_id = db.Column(db.Integer, db.ForeignKey("patients.id"))

    diagnosis = db.Column(db.Text)

    treatment = db.Column(db.Text)

    prescription = db.Column(db.Text)

    notes = db.Column(db.Text)

    visit_date = db.Column(db.Date)

    patient = db.relationship(
        "Patient",
        backref=db.backref("medical_records", cascade="all, delete-orphan")
    )