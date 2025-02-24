from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class Tab(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    artist = db.Column(db.String(100))
    tuning = db.Column(db.JSON)
    string1 = db.Column(db.String(500))
    string2 = db.Column(db.String(500))

    def to_dict(self):
        return {
            "id": self.id,
            "title": self.title,
            "artist": self.artist,
            "tuning": self.tuning,
            "string1": self.string1,
            "string2": self.string2
        }