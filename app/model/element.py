from app.model.base import db

from collections import OrderedDict

class Element(db.Model):

    __tablename__ = "element"
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), unique=True, nullable=False)

    def __init__(self, id, name):
        self.id = id
        self.name = name

    def __str__(self):
        return "\nID: " + str(self.id) + \
               "\nName: " + str(self.name)

    def dictify(self, thinify=True):
        dictified = OrderedDict()
        dictified["id"] = self.id
        dictified["name"] = self.name

        if not thinify:
            dictified["primary_element_owned_by"] = [monster.id for monster in self.primary_element_owned_by_monsters]
            dictified["secondary_element_owned_by"] = [monster.id for monster in self.secondary_element_owned_by_monsters]

        return dictified