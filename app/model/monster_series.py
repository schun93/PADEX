from app.model.base import db

class MonsterSeries(db.Model):

    __tablename__ = "monster_series"
    
    id = db.Column(db.Integer, primary_key=True, autoincrement=False)
    name = db.Column(db.String(80), nullable=False, unique=True)

    def __init__(self, id, name):
        self.id = id
        self.name = name

    def __str__(self):
        return "\nID: " + str(self.id) + \
               "\nName: " + self.name
