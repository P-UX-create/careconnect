from models import db


class Patient(db.Model):
    __tablename__ = "patients"

    id = db.Column(db.Integer, primary_key=True)

    first_name = db.Column(db.String(50), nullable=False)

    last_name = db.Column(db.String(50), nullable=False)

    gender = db.Column(db.String(10), nullable=False)

    date_of_birth = db.Column(db.Date)

    phone = db.Column(db.String(20))

    email = db.Column(db.String(100))

    address = db.Column(db.String(200))

    blood_group = db.Column(db.String(10))

    emergency_contact = db.Column(db.String(20))

    created_at = db.Column(db.DateTime, server_default=db.func.now())