from models import db


class DoctorAvailability(db.Model):
    """A weekly time window when a doctor accepts appointments."""

    __tablename__ = "doctor_availability"

    id = db.Column(db.Integer, primary_key=True)

    doctor_id = db.Column(db.Integer, db.ForeignKey("doctors.id"), nullable=False)

    # 0 = Monday ... 6 = Sunday
    day_of_week = db.Column(db.Integer, nullable=False)

    start_time = db.Column(db.Time, nullable=False)

    end_time = db.Column(db.Time, nullable=False)

    doctor = db.relationship(
        "Doctor",
        backref=db.backref("availability", cascade="all, delete-orphan")
    )
