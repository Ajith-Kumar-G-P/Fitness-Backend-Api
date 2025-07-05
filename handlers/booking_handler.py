
import re
import logging
from models.class_model import FitnessClass
from models.booking_model import Booking
from db import db
from utils.time_utils import convert_to_timezone
from sqlalchemy.exc import SQLAlchemyError

logger = logging.getLogger(__name__)

def is_valid_email(email):
    return re.match(r"[^@]+@[^@]+\.[^@]+", email)

def create_class_handler(data):
    required_fields = ["name", "datetime", "instructor", "total_slots"]
    if not all(field in data for field in required_fields):
        logger.warning("Missing required fields in class creation")
        return {"error": "Missing required fields"}, 400

    if not isinstance(data["total_slots"], int) or data["total_slots"] <= 0:
        logger.warning("Invalid total_slots input")
        return {"error": "total_slots must be a positive integer"}, 400

    try:
        new_class = FitnessClass(
            name=data["name"],
            datetime=data["datetime"],
            instructor=data["instructor"],
            total_slots=data["total_slots"],
            available_slots=data["total_slots"]
        )
        db.session.add(new_class)
        db.session.commit()
        logger.info(f"Class created: {new_class.name} by {new_class.instructor}")
        return {"message": "Class created successfully"}, 201
    except SQLAlchemyError as e:
        db.session.rollback()
        logger.error("Database error during class creation", exc_info=True)
        return {"error": "Database error", "details": str(e)}, 500

def list_classes_handler(user_tz="Asia/Kolkata"):
    try:
        classes = FitnessClass.query.all()
        logger.info("Fetched all classes")
        return [{
            "id": c.id,
            "name": c.name,
            "datetime": convert_to_timezone(c.datetime, user_tz),
            "instructor": c.instructor,
            "available_slots": c.available_slots
        } for c in classes]
    except Exception as e:
        logger.error("Error fetching classes", exc_info=True)
        return {"error": "Failed to fetch classes", "details": str(e)}, 500

def book_class_handler(class_id, name, email):
    if not all([class_id, name, email]):
        logger.warning("Missing fields in booking request")
        return {"error": "Missing booking fields"}, 400

    if not is_valid_email(email):
        logger.warning(f"Invalid email format: {email}")
        return {"error": "Invalid email format"}, 400

    try:
        cls = FitnessClass.query.get(class_id)
        if not cls:
            logger.warning(f"Class ID {class_id} not found")
            return {"error": "Class not found"}, 404

        if cls.available_slots <= 0:
            logger.warning(f"No slots available for class ID {class_id}")
            return {"error": "No slots available"}, 400

        booking = Booking(class_id=class_id, client_name=name, client_email=email)
        cls.available_slots -= 1

        db.session.add(booking)
        db.session.commit()
        logger.info(f"Booking successful for {email} in class ID {class_id}")
        return {"message": "Booking successful"}, 200
    except SQLAlchemyError as e:
        db.session.rollback()
        logger.error("Database error during booking", exc_info=True)
        return {"error": "Database error", "details": str(e)}, 500

def get_bookings_handler(email):
    if not email:
        logger.warning("Email missing in get_bookings request")
        return {"error": "Email is required"}, 400

    if not is_valid_email(email):
        logger.warning(f"Invalid email format in bookings request: {email}")
        return {"error": "Invalid email format"}, 400

    try:
        bookings = Booking.query.filter_by(client_email=email).all()
        if not bookings:
            logger.info(f"No bookings found for {email}")
            return {"message": "No bookings found"}, 200

        logger.info(f"Fetched bookings for {email}")
        return [{
            "booking_id": b.id,
            "class_name": b.fitness_class.name,
            "datetime": b.fitness_class.datetime,
            "instructor": b.fitness_class.instructor
        } for b in bookings]
    except SQLAlchemyError as e:
        logger.error("Database error fetching bookings", exc_info=True)
        return {"error": "Failed to fetch bookings", "details": str(e)}, 500
