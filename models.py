from extensions import db

# ---------- INFOGRAPHICS ----------
class Infographics(db.Model):
    __tablename__ = "infographics"

    id = db.Column(db.Integer, primary_key=True)

    total_population = db.Column(db.Integer, nullable=False)
    total_family = db.Column(db.Integer, nullable=False)


# ---------- NEWS ----------
class News(db.Model):
    __tablename__ = "news"

    id = db.Column(db.Integer, primary_key=True)

    title = db.Column(db.String(255), nullable=False)
    slug = db.Column(db.String(255), nullable=False, unique=True)

    content = db.Column(db.Text, nullable=False)

    thumbnail = db.Column(db.String(255), nullable=True)

    published_at = db.Column(db.DateTime, nullable=False)

    created_at = db.Column(db.DateTime)

    updated_at = db.Column(db.DateTime)

# ---------- ANNOUNCEMENT ----------
class Announcement(db.Model):
    __tablename__ = "announcement"

    id = db.Column(db.Integer, primary_key=True)

    title = db.Column(db.String(255), nullable=False)

    description = db.Column(db.Text)

    event_date = db.Column(db.DateTime)

    location = db.Column(db.String(255))

    created_at = db.Column(db.DateTime)

    type = db.Column(db.String(100))