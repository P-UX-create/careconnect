from models import db


class Doctor(db.Model):
    __tablename__ = "doctors"

    id = db.Column(db.Integer, primary_key=True)

    user_id = db.Column(db.Integer, db.ForeignKey("user.id"), unique=True)

    fullname = db.Column(db.String(100), nullable=False)

    specialization = db.Column(db.String(100))

    phone = db.Column(db.String(20))

    email = db.Column(db.String(100))

    room_number = db.Column(db.String(20))

    about = db.Column(db.Text)

    available = db.Column(db.Boolean, default=True)

    user = db.relationship(
        "User",
        backref=db.backref("doctor_profile", uselist=False)
    )