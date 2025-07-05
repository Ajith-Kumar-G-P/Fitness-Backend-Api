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
    response = list_classes_handler(tz)

    if isinstance(response, tuple):
        return jsonify(response[0]), response[1]
    return jsonify(response)

@booking_bp.route("/classes/create", methods=["POST"])
def create_class():
    data = request.get_json()
    response = create_class_handler(data)

    if isinstance(response, tuple):
        return jsonify(response[0]), response[1]
    return jsonify(response)

@booking_bp.route("/book", methods=["POST"])
def book_class():
    data = request.get_json()
    response = book_class_handler(
        class_id=data.get("class_id"),
        name=data.get("client_name"),
        email=data.get("client_email")
    )
    if isinstance(response, tuple):
        return jsonify(response[0]), response[1]
    return jsonify(response)

@booking_bp.route("/bookings", methods=["GET"])
def get_bookings():
    email = request.args.get("email")
    response = get_bookings_handler(email)
    
    if isinstance(response, tuple):
        return jsonify(response[0]), response[1]
    return jsonify(response)
