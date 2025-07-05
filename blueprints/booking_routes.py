from flask import Blueprint, request, jsonify
from handlers.booking_handler import (
    create_class_handler,
    list_classes_handler,
    book_class_handler,
    get_bookings_handler
)

booking_bp = Blueprint("booking", __name__)

@booking_bp.route("/classes", methods=["GET"])
def get_classes():
    tz = request.args.get("tz", "Asia/Kolkata")
    return jsonify(list_classes_handler(tz))

@booking_bp.route("/classes/create", methods=["POST"])
def create_class():
    data = request.get_json()
    required_fields = ["name", "datetime", "instructor", "total_slots"]
    if not all(field in data for field in required_fields):
        return jsonify({"error": "Missing required fields"}), 400
    return create_class_handler(data)

@booking_bp.route("/book", methods=["POST"])
def book_class():
    data = request.get_json()
    required_fields = ["class_id", "client_name", "client_email"]
    if not all(field in data for field in required_fields):
        return jsonify({"error": "Missing booking fields"}), 400
    return book_class_handler(data["class_id"], data["client_name"], data["client_email"])

@booking_bp.route("/bookings", methods=["GET"])
def get_bookings():
    email = request.args.get("email")
    if not email:
        return jsonify({"error": "Email is required"}), 400
    return jsonify(get_bookings_handler(email))
