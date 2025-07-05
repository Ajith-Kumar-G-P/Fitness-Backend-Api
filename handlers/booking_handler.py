from models.class_model import FitnessClass
from models.booking_model import Booking
from db import db
from utils.time_utils import convert_to_timezone

def create_class_handler(data):
    new_class = FitnessClass(
        name=data["name"],
        datetime=data["datetime"],
        instructor=data["instructor"],
        total_slots=data["total_slots"],
        available_slots=data["total_slots"]
    )
    db.session.add(new_class)
    db.session.commit()
    return {"message": "Class created successfully"}, 201

def list_classes_handler(user_tz="Asia/Kolkata"):
    classes = FitnessClass.query.all()
    return [{
        "id": c.id,
        "name": c.name,
        "datetime": convert_to_timezone(c.datetime, user_tz),
        "instructor": c.instructor,
        "available_slots": c.available_slots
    } for c in classes]

def book_class_handler(class_id, name, email):
    cls = FitnessClass.query.get(class_id)
    if not cls:
        return {"error": "Class not found"}, 404
    if cls.available_slots <= 0:
        return {"error": "No slots available"}, 400

    booking = Booking(class_id=class_id, client_name=name, client_email=email)
    cls.available_slots -= 1
    db.session.add(booking)
    db.session.commit()
    return {"message": "Booking successful"}, 200

def get_bookings_handler(email):
    bookings = Booking.query.filter_by(client_email=email).all()
    return [{
        "booking_id": b.id,
        "class_name": b.fitness_class.name,
        "datetime": b.fitness_class.datetime,
        "instructor": b.fitness_class.instructor
    } for b in bookings]
