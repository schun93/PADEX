from app.model.base import db

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
        return "\nS_ID: " + str(self.id) + \
               "\nName: " + str(self.name) + \
               "\nEffect: " + str(self.effect) + \
               "\nPart of Moves: " + str(self.part_of_moves)

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

class EnemyMonster(db.Model):

    __tablename__ = "enemy_monster"

    id = db.Column(db.Integer, primary_key=True)
    hp = db.Column(db.Integer)
    atk = db.Column(db.Integer)
    defn = db.Column(db.Integer, nullable=False)
    turn = db.Column(db.Integer)
    floor = db.Column(db.Integer)
    quantity = db.Column(db.Integer)

    common_monster_id = db.Column(db.Integer, db.ForeignKey("common_monster.id"), nullable=False)
    common_monster = db.relationship("CommonMonster", backref="enemy_monsters", foreign_keys="EnemyMonster.common_monster_id")

    random_encounter_in_dungeon_id = db.Column(db.Integer, db.ForeignKey("dungeon.id"))
    random_encounter_in_dungeon = db.relationship("Dungeon", backref="random_encounters", foreign_keys="EnemyMonster.random_encounter_in_dungeon_id")

    major_encounter_in_dungeon_id = db.Column(db.Integer, db.ForeignKey("dungeon.id"))
    major_encounter_in_dungeon = db.relationship("Dungeon", backref="major_encounters", foreign_keys="EnemyMonster.major_encounter_in_dungeon_id")

    def __init__(self, hp, atk, defn, turn, floor=None, quantity=None):
        self.hp = hp
        self.atk = atk
        self.defn = defn
        self.floor = floor
        self.quantity = quantity
        self.turn = turn

    def __str__(self):
        moves_string = ""

        for move_info in self.moves:
            moves_string += str(move_info) + "\n"

        return  "\nDungeon Monster ID: " + str(self.id) + \
                "\nHP: " + str(self.hp) + \
                "\nATK: " + str(self.atk) + \
                "\nDEF: " + str(self.defn) + \
                "\nFloor: " + str(self.floor) + \
                "\nQuantity: " + str(self.quantity) + \
                "\nTurn: " + str(self.turn) + \
                "\nCommon Monster: " + str(self.common_monster) + \
                "\nMoves Info: " + moves_string

    def encounter_in_dungeon(self):
        return self.random_encounter_in_dungeon if self.random_encounter_in_dungeon_id != None else self.major_encounter_in_dungeon

class Dungeon(db.Model):

    __tablename__ = "dungeon"
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), nullable=False)

    def __init__(self, id, name):
        self.id = id
        self.name = name

    def __str__(self):
        random_encounters_string = ""

        for dungeon_monster in self.random_encounters:
            random_encounters_string += str(dungeon_monster) + "\n"

        major_encounters_string = ""

        for dungeon_monster in self.major_encounters:
            major_encounters_string += str(dungeon_monster) + "\n"

        return  "\n\nDungeon ID: " + str(self.id) + \
                "\nName: " + str(self.name) + \
                "\nRandom Encounters:" + random_encounters_string + \
                "\n\nMajor Encounters:" + major_encounters_string

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
