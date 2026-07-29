from models import db


class Doctor(db.Model):
    __tablename__ = "doctors"

    id = db.Column(db.Integer, primary_key=True)

    fullname = db.Column(db.String(100), nullable=False)

    specialization = db.Column(db.String(100))

    phone = db.Column(db.String(20))

    email = db.Column(db.String(100))

    room_number = db.Column(db.String(20))

    available = db.Column(db.Boolean, default=True)