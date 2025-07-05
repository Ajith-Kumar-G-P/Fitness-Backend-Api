from db import db
from config import Config
from blueprints.booking_routes import booking_bp
from db.seed import insert_seed_data 
import logging_config 

from flask import Flask

app = Flask(__name__)
app.config.from_object(Config)
db.init_app(app)

with app.app_context():
    db.create_all()
    insert_seed_data()

app.register_blueprint(booking_bp)

if __name__ == "__main__":
    app.run(debug=True)
