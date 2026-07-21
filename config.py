import os

class Config:
    SQLALCHEMY_DATABASE_URI = "mysql+pymysql://root:@127.0.0.1:3306/website-kkn?charset=utf8mb4"
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SECRET_KEY = 'supersecretkey123'  # Ganti dengan kunci tetap jika tidak ingin kunci acak setiap kali
