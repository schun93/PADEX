from app.model.base import db

class ActiveSkill(db.Model):

    __tablename__ = "active_skill"
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), nullable=False)
    effect = db.Column(db.String(256), nullable=False)
    original_effect = db.Column(db.String(256), nullable=False)
    max_cd = db.Column(db.String(80))
    min_cd = db.Column(db.String(80))
    max_lvl = db.Column(db.String(80))

    def __init__(self, id, name, effect, original_effect, max_cd, min_cd, max_lvl):
        self.id = id
        self.name = name
        self.effect = effect
        self.original_effect = original_effect
        self.max_cd = max_cd
        self.min_cd = min_cd
        self.max_lvl = max_lvl

    def __str__(self):
        return "\nID: " + str(self.id) + \
               "\nName: " + self.name + \
               "\nEffect: " + self.effect + \
               "\nOriginal Effect: " + self.original_effect + \
               "\nMax CD: " + str(self.max_cd) + \
               "\nMin CD: " + str(self.min_cd) + \
               "\nMax Lvl: " + str(self.max_lvl)
