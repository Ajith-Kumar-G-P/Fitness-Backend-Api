
#  Fitness Booking API

A simple backend API built using **Flask**, **SQLAlchemy**, and **Blueprints** for a fictional fitness studio that offers Yoga, Zumba, and HIIT classes. Clients can view classes, book slots, and view their bookings.

---

##  Project Structure

```
fitness_booking_api/
│
├── app.py                    # App entry point
├── config.py                 # Config class with DB path
├── requirements.txt
│
├── db/
│   └── __init__.py           # SQLAlchemy instance
│
├── models/
│   ├── class_model.py        # FitnessClass model
│   └── booking_model.py      # Booking model
│
├── handlers/
│   └── booking_handler.py    # Core booking logic
│
├── blueprints/
│   └── booking_routes.py     # Route handlers
│
├── utils/
│   └── time_utils.py         # Timezone conversion
└── README.md
```

---

## ⚙️ Setup Instructions

###  1. Create Virtual Environment (optional)

```bash
python -m venv venv
venv\Scripts\activate       
```

###  2. Install Required Packages

```bash
pip install -r requirements.txt
```

##  Run the Application

```bash
python app.py 
    (or) 
flask run --debug
```

> App runs at: `http://localhost:5000`

---

##  Requirements

```
Flask
Flask-SQLAlchemy
tzdata    
```

---

##  API Endpoints

### 🔹 `GET /classes`

Returns all upcoming classes with converted time.

**Request:**
```
GET http://localhost:5000/classes?tz=UTC
```

**Response:**
```json
[
  {
    "id": 1,
    "name": "Yoga",
    "datetime": "2025-07-06T01:30:00+00:00",
    "instructor": "Alice",
    "available_slots": 10
  }
]
```

---

### 🔹 `POST /classes/create`

Creates a new class (admin use).

**Request:**
```
POST http://localhost:5000/classes/create
Content-Type: application/json
```

**JSON Body:**
```json
{
  "name": "Pilates",
  "datetime": "2025-07-08T09:00:00",
  "instructor": "Daisy",
  "total_slots": 12
}
```

**Success Response:**
```json
{
  "message": "Class created successfully"
}
```

---

### 🔹 `POST /book`

Books a slot for a client in a class.

**Request:**
```
POST http://localhost:5000/book
Content-Type: application/json
```

**JSON Body:**
```json
{
  "class_id": 1,
  "client_name": "Ajith Kumar",
  "client_email": "ajith@example.com"
}
```

**Success Response:**
```json
{
  "message": "Booking successful"
}
```

---

### 🔹 `GET /bookings`

Returns bookings made by a client.

**Request:**
```
GET http://localhost:5000/bookings?email=ajith@example.com
```

**Response:**
```json
[
  {
    "booking_id": 1,
    "class_name": "Yoga",
    "datetime": "2025-07-06T07:00:00",
    "instructor": "Alice"
  }
]
```

---

##  Timezone Handling

- By default, class times are stored in **Asia/Kolkata**.
- You can convert times using `?tz=Europe/London` or `?tz=UTC` etc.

Uses Python’s built-in `zoneinfo` (with `tzdata` for Windows).

---

> Built with ❤️ by Ajith Kumar G P
