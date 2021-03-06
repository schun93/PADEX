from app.model.base import db

from collections import OrderedDict

class LeaderSkill(db.Model):

    __tablename__ = "leader_skill"
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), nullable=False)
    effect = db.Column(db.String(512), nullable=False)
    original_effect = db.Column(db.String(256), nullable=False)

    def __init__(self, id, name, effect, original_effect):
        self.id = id
        self.name = name
        self.effect = effect
        self.original_effect = original_effect

    def __str__(self):
        return "\nID: " + str(self.id) + \
               "\nName: " + self.name + \
               "\nEffect: " + self.effect + \
               "\nOriginal Effect: " + self.original_effect

    def dictify(self, thinify=True):
        dictified = OrderedDict()
        dictified["id"] = self.id
        dictified["name"] = self.name
        dictified["effect"] = self.effect
        dictified["original_effect"] = self.original_effect

        if not thinify:
            dictified["owned_by_monsters"] = [monster.id for monster in self.owned_by_monsters]

        return dictified