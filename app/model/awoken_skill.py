from app.model.base import db

from collections import OrderedDict

class AwokenSkill(db.Model):

    __tablename__ = "awoken_skill"
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), nullable=False)
    description = db.Column(db.String(256), nullable=False)
    img = db.Column(db.String(128), nullable=False)

    def __init__(self, id, name, description, img):
        self.id = id
        self.name = name
        self.description = description
        self.img = img

    def __str__(self):
        return  "\nID: " + str(self.id) + \
                "\nName: " + self.name + \
                "\nEffect: " + self.description + \
                "\nImg: " + self.img + \
                "\nMonsters: " + str(self.owned_by_monsters)

    def dictify(self, thinify=True):
        dictified = OrderedDict()
        dictified["id"] = self.id
        dictified["name"] = self.name
        dictified["description"] = self.description
        dictified["img"] = self.img
        
        if not thinify:
            dictified["owned_by_monsters"] = [monster.id for monster in self.owned_by_monsters]

        return dictified
