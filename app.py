# app.py
from flask import Flask
from config import Config
from extensions import db
from routes.route import main
from routes.admin_route import admin_bp
from dotenv import load_dotenv
load_dotenv()
import os

app = Flask(__name__)
app.config.from_object(Config)
app.config["UPLOAD_FOLDER"] = os.path.join(
    app.root_path,
    "static",
    "uploads",
    "news"
)
db.init_app(app)

# Membuat tabel jika belum ada
with app.app_context():
    db.create_all()  # Membuat semua tabel berdasarkan model

app.register_blueprint(main)
app.register_blueprint(admin_bp, url_prefix="/admin")

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)

