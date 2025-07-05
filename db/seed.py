from models.class_model import FitnessClass
from models.booking_model import Booking
from db import db

def insert_seed_data():
    if FitnessClass.query.first():
        return  # Prevent reseeding if already present

    classes = [
        FitnessClass(
            name="Yoga",
            datetime="2025-07-07T06:00:00",
            instructor="Alice",
            total_slots=10,
            available_slots=10
        ),
        FitnessClass(
            name="Zumba",
            datetime="2025-07-08T08:00:00",
            instructor="Bob",
            total_slots=15,
            available_slots=15
        ),
        FitnessClass(
            name="HIIT",
            datetime="2025-07-09T07:30:00",
            instructor="Charlie",
            total_slots=12,
            available_slots=12
        ),
        FitnessClass(
            name="Pilates",
            datetime="2025-07-10T09:00:00",
            instructor="Daisy",
            total_slots=8,
            available_slots=8
        )
    ]

    db.session.bulk_save_objects(classes)
    db.session.commit()
    print("Seed data inserted.")
