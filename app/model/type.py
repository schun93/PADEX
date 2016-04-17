from app.model.base import db

class Type(db.Model):

    __tablename__ = "type"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), unique=True, nullable=False)

    def __init__(self, id, name):
        self.id = id
        self.name = name

    def __str__(self):
        return "\nID: " + str(self.id) + \
               "\nName: " + str(self.name)