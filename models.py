from app import db

class Product(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    type = db.Column(db.String(100), nullable=False)
    price = db.Column(db.Float, nullable=False)
    site = db.Column(db.String(100), nullable=False)
    website = db.Column(db.String(200), nullable=False)
    image_url = db.Column(db.String(500), nullable=True)
