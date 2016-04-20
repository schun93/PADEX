from app.model.base import db

from sqlalchemy.orm import backref

from collections import OrderedDict

class EnemySkill(db.Model):

    __tablename__ = "enemy_skill"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), nullable=False)
    effect = db.Column(db.String(256))

    def __init__(self, id, name, effect):
        self.id = id
        self.name = name
        self.effect = effect

    def __str__(self):
        return str(self.dictify(thinify=False))

    def dictify(self, thinify=True):
        dictified = OrderedDict()
        dictified["name"] = self.name
        dictified["effect"] = self.effect

        if not thinify:
            dictified["part_of_moves"] = [move.id for move in self.part_of_moves]

        return dictified

enemy_move_move_type_n = db.Table("enemy_move_move_type_n",
                                  db.Column("id", db.Integer, primary_key=True),
                                  db.Column("enemy_move_id", db.ForeignKey("enemy_move.id")),
                                  db.Column("enemy_move_type_id", db.ForeignKey("enemy_move_type.id"))
                                  )

class EnemyMove(db.Model):

    __tablename__ = "enemy_move"

    id = db.Column(db.Integer, primary_key=True)
    atk = db.Column(db.Integer)
    atk_condition = db.Column(db.String(128))

    # enemy_monster_id = db.Column(db.Integer, db.ForeignKey("enemy_monster.id"), nullable=False)
    enemy_monster_id = db.Column(db.Integer, db.ForeignKey("enemy_monster.id"))
    enemy_monster = db.relationship("EnemyMonster", backref="moves", foreign_keys="EnemyMove.enemy_monster_id")

    enemy_skill_id = db.Column(db.Integer, db.ForeignKey("enemy_skill.id"), nullable=False)
    enemy_skill = db.relationship("EnemySkill", backref="part_of_moves", foreign_keys="EnemyMove.enemy_skill_id")

    enemy_move_types = db.relationship("EnemyMoveType", secondary=enemy_move_move_type_n, backref="part_of_moves")

    def __init__(self, atk_condition, atk=None):
        self.atk = atk
        self.atk_condition = atk_condition

    def __str__(self):
        return  "\nMove Information:" + \
                "\nM_ID: " + str(self.id) + \
                "\nATK: " + str(self.atk) + \
                "\nATK Condition: " + str(self.atk_condition) + \
                "\nFK.S_ID: " + str(self.enemy_skill_id) + \
                "\nEnemy Skill: " + str(self.enemy_skill)

    def dictify(self):
        dictified = OrderedDict()
        dictified["name"] = self.enemy_skill.name
        dictified["attack"] = self.atk
        dictified["attack_condition"] = self.atk_condition
        dictified["effect"] = self.enemy_skill.effect
        dictified["move_types"] = [move_type.id for move_type in self.enemy_move_types]

        return dictified

class EnemyMoveType(db.Model):

    __tablename___ = "enemy_move_type"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), nullable=False)
    img = db.Column(db.String(128))

    def __init__(self, id, name, img=None, description=None):
        self.id = id
        self.name = name
        self.img = img

    def dictify(self, thinify=True):
        dictified = OrderedDict()
        dictified["id"] = self.id
        dictified["name"] = self.name
        dictified["img"] = self.img

class EnemyMonster(db.Model):

    __tablename__ = "enemy_monster"

    id = db.Column(db.Integer, primary_key=True)
    hp = db.Column(db.Integer)
    atk = db.Column(db.Integer)
    defn = db.Column(db.Integer, nullable=False)
    turn = db.Column(db.Integer)
    quantity = db.Column(db.Integer)
    memo = db.Column(db.String(512))

    common_monster_id = db.Column(db.Integer, db.ForeignKey("common_monster.id"), nullable=False)
    common_monster = db.relationship("CommonMonster", backref="enemy_monsters", foreign_keys="EnemyMonster.common_monster_id")

    random_encounter_in_dungeon_id = db.Column(db.Integer, db.ForeignKey("dungeon.id"))
    random_encounter_in_dungeon = db.relationship("Dungeon", backref="random_encounters", foreign_keys="EnemyMonster.random_encounter_in_dungeon_id")

    major_encounter_on_floor_id = db.Column(db.Integer, db.ForeignKey("floor.id"))
    major_encounter_on_floor = db.relationship("Floor", backref="encounters", foreign_keys="EnemyMonster.major_encounter_on_floor_id")

    def __init__(self, hp, atk, defn, turn, quantity=None):
        self.hp = hp
        self.atk = atk
        self.defn = defn
        self.quantity = quantity
        self.turn = turn

    def __str__(self):
        return str(self.dictify())

    def encounter_in_dungeon(self):
        return self.random_encounter_in_dungeon if self.random_encounter_in_dungeon_id != None else self.major_encounter_on_floor.dungeon

    def dictify(self):
        dictified = OrderedDict()
        dictified["common_id"] = self.common_monster_id
        dictified["name"] = self.common_monster.name
        dictified["hit_points"] = self.hp
        dictified["attack"] = self.atk
        dictified["defense"] = self.defn
        dictified["turn"] = self.turn
        dictified["quantity"] = self.quantity
        dictified["drop"] = [drop.monster_id for drop in self.drops]
        dictified["moves"] = [move.dictify() for move in self.moves]

        return dictified

class Dungeon(db.Model):

    __tablename__ = "dungeon"
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), nullable=False)

    def __init__(self, id, name):
        self.id = id
        self.name = name

    def __str__(self):
        return str(self.dictify())

    def dictify(self):
        dictified = OrderedDict()
        dictified["id"] = self.id
        dictified["name"] = self.name
        dictified["random_encounters"] = [random_encounter.dictify() for random_encounter in self.random_encounters]
        dictified["major_floors"] = [floor.dictify() for floor in self.floors]

        return dictified

class Floor(db.Model):

    __tablename__ = "floor"

    id = db.Column(db.Integer, primary_key=True)
    number = db.Column(db.Integer)

    dungeon_id = db.Column(db.Integer, db.ForeignKey("dungeon.id"))
    dungeon = db.relationship("Dungeon", backref=backref("floors", order_by="Floor.number"), foreign_keys="Floor.dungeon_id")

    def __init__(self, number):
        self.number = number

    def dictify(self):
        dictified = OrderedDict()
        dictified["floor_number"] = self.number
        dictified["encounter"] = [monster.dictify() for monster in self.encounters]
        dictified["memos"] = [floor.memo for floor in self.floor_memos]

        return dictified

class FloorMemo(db.Model):
    
    __tablename__ = "floor_memo"

    id = db.Column(db.Integer, primary_key=True)
    memo = db.Column(db.String(512))

    floor_id = db.Column(db.Integer, db.ForeignKey("floor.id"))
    floor = db.relationship("Floor", backref="floor_memos", foreign_keys="FloorMemo.floor_id")

    def __init__(self, memo):
        self.memo = memo

    def dictify(self):
        return {"memo": self.memo}


class Drop(db.Model):
    __tablename__ = "monster_drop"

    id = db.Column(db.Integer, primary_key=True)
    chance = db.Column(db.Integer)

    enemy_monster_id = db.Column(db.Integer, db.ForeignKey("enemy_monster.id"))
    enemy_monster = db.relationship("EnemyMonster", backref="drops", foreign_keys="Drop.enemy_monster_id")

    monster_id = db.Column(db.Integer, db.ForeignKey("monster.id"))
    monster = db.relationship("Monster", backref="drops", foreign_keys="Drop.monster_id")

    def __init__(self, chance=None):
        self.chance = chance
