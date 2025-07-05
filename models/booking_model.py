from db import db

class Booking(db.Model):
    __tablename__ = "bookings"

    id = db.Column(db.Integer, primary_key=True)
    class_id = db.Column(db.Integer, db.ForeignKey("classes.id"))
    client_name = db.Column(db.String(50), nullable=False)
    client_email = db.Column(db.String(100), nullable=False)

    fitness_class = db.relationship("FitnessClass", backref="bookings")
