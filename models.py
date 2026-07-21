from extensions import db

# ---------- INFOGRAPHICS ----------
class Infographics(db.Model):
    __tablename__ = "infographics"

    id = db.Column(db.Integer, primary_key=True)

    total_population = db.Column(db.Integer, nullable=False)
    total_family = db.Column(db.Integer, nullable=False)