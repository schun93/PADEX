from app.model.base import db

from sqlalchemy.orm import backref

class CommonMonster(db.Model):

    __tablename__ = "common_monster"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), nullable=False)
    img = db.Column(db.String(128), nullable=False, unique=True)
    thmb = db.Column(db.String(128), nullable=False, unique=True)

    primary_type_id = db.Column(db.Integer, db.ForeignKey("type.id"), nullable=False)
    primary_type = db.relationship("Type", backref="primary_type_owned_by_monsters", foreign_keys="CommonMonster.primary_type_id")

    secondary_type_id = db.Column(db.Integer, db.ForeignKey("type.id"))
    secondary_type = db.relationship("Type", backref="secondary_type_owned_by_monsters", foreign_keys="CommonMonster.secondary_type_id")

    ternary_type_id = db.Column(db.Integer, db.ForeignKey("type.id"))
    ternary_type = db.relationship("Type", backref="ternary_type_owned_by_monsters", foreign_keys="CommonMonster.ternary_type_id")

    primary_element_id = db.Column(db.Integer, db.ForeignKey("element.id"), nullable=False)
    primary_element = db.relationship("Element", backref="primary_element_owned_by_monsters", foreign_keys="CommonMonster.primary_element_id")

    secondary_element_id = db.Column(db.Integer, db.ForeignKey("element.id"))
    secondary_element = db.relationship("Element", backref="secondary_element_owned_by_monsters", foreign_keys="CommonMonster.secondary_element_id")

    monster_id = db.Column(db.Integer, db.ForeignKey("monster.id"), nullable=False)
    monster = db.relationship("Monster", backref=backref("common_monster", uselist=False))

    def __init__(self, id, name, img, thmb):
        self.id = id
        self.name = name
        self.img = img
        self.thmb = thmb

    def __str__(self):
        return "\nID: " + str(self.id) + \
               "\nName: " + str(self.name) + \
               "\nIMG: " + str(self.img) + \
               "\nTHMB: " + str(self.thmb) + \
               "\nPrimary Type: " + str(self.primary_type) + \
               "\nSecondary Type: " + str(self.secondary_type) + \
               "\nTernary Type: " + str(self.ternary_type) + \
               "\nPrimary Element: " + str(self.primary_element) + \
               "\nSecondary Element: " + str(self.secondary_element) + \
               "\nMonster: " + str(self.monster)

awoken_skill_monster_n = db.Table("awoken_skill_monster_n", 
                                  db.Column("id", db.Integer, primary_key=True),
                                  db.Column("awoken_skill_id", db.ForeignKey("awoken_skill.id")),
                                  db.Column("monster_id", db.ForeignKey("monster.id"))
                                  )

class Monster(db.Model):

    __tablename__ = "monster"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), nullable=False)
    rarity = db.Column(db.Integer, nullable=False)
    team_cost = db.Column(db.Integer, nullable=False)
    sells_for_monster_points = db.Column(db.Integer, nullable=False)
    min_lvl = db.Column(db.Integer, nullable=False)
    max_lvl = db.Column(db.Integer, nullable=False)
    min_hp = db.Column(db.Integer, nullable=False)
    max_hp = db.Column(db.Integer, nullable=False)
    min_atk = db.Column(db.Integer, nullable=False)
    max_atk = db.Column(db.Integer, nullable=False)
    min_rcv = db.Column(db.Integer, nullable=False)
    max_rcv = db.Column(db.Integer, nullable=False)
    min_sell_value = db.Column(db.Integer, nullable=False)
    max_sell_value = db.Column(db.Integer, nullable=False)
    min_exp_feed = db.Column(db.Integer, nullable=False)
    max_exp_feed = db.Column(db.Integer, nullable=False)
    exp_needed = db.Column(db.Integer, nullable=False)

    monster_series_id = db.Column(db.Integer, db.ForeignKey("monster_series.id"))
    monster_series = db.relationship("MonsterSeries", backref="monsters_in_series", foreign_keys="Monster.monster_series_id")

    active_skill_id = db.Column(db.Integer, db.ForeignKey("active_skill.id"))
    active_skill = db.relationship("ActiveSkill", backref="owned_by_monsters", foreign_keys="Monster.active_skill_id")

    leader_skill_id = db.Column(db.Integer, db.ForeignKey("leader_skill.id"))
    leader_skill = db.relationship("LeaderSkill", backref="owned_by_monsters", foreign_keys="Monster.leader_skill_id")

    awoken_skills = db.relationship("AwokenSkill", secondary=awoken_skill_monster_n, backref="owned_by_monsters")

    def __init__(self, id, name, rarity, team_cost, sells_for_monster_points, min_lvl, max_lvl, \
                 min_hp, max_hp, min_atk, max_atk, min_rcv, max_rcv, min_sell_value, max_sell_value, \
                 min_exp_feed, max_exp_feed, exp_needed):
        self.id = id
        self.name = name
        self.rarity = rarity
        self.team_cost = team_cost
        self.sells_for_monster_points = sells_for_monster_points
        self.min_lvl = min_lvl
        self.max_lvl = max_lvl
        self.min_hp = min_hp
        self.max_hp = max_hp
        self.min_atk = min_atk
        self.max_atk = max_atk
        self.min_rcv = min_rcv
        self.max_rcv = max_rcv
        self.min_sell_value = min_sell_value
        self.max_sell_value = max_sell_value
        self.min_exp_feed = min_exp_feed
        self.max_exp_feed = max_exp_feed
        self.exp_needed = exp_needed

        #List of dungeon_id foreign key
        # self.obtainable_in_dungeons = obtainable_in_dungeons

    def __str__(self):
        return  "ID: " + str(self.id) + \
                "\nName: " + str(self.name) + \
                "\nRarity: " + str(self.rarity) + \
                "\nTeam Cost: " + str(self.team_cost) + \
                "\nMonster Points: " + str(self.sells_for_monster_points) + \
                "\nEvolves To: " + str(self.evolves_to) + \
                "\nEvolves From: " + str(self.evolves_from) + \
                "\nLvl: " + str(self.min_lvl) + "\t- " + str(self.max_lvl) + \
                "\nHP: " + str(self.min_hp) + "\t- " + str(self.max_hp) + \
                "\nATK: " + str(self.min_atk) + "\t- " + str(self.max_atk) + \
                "\nRCV: " + str(self.min_rcv) + "\t- " + str(self.max_rcv) + \
                "\nSell Value: " + str(self.min_sell_value) + "\t- " + str(self.max_sell_value) + \
                "\nFeed Value: " + str(self.min_exp_feed) + "\t- " + str(self.max_exp_feed) + \
                "\nExp Needed: " + str(self.exp_needed) + \
                "\nActive Skill: " + str(self.active_skill) + \
                "\nLeader Skill: " + str(self.leader_skill) + \
                "\nAwoken Skills: " + str(self.awoken_skills) + \
                "\nMonster Series: " + str(self.monster_series)

required_materials_evolution_n = db.Table("required_materials_evolution_n", 
                                        db.Column("id", db.Integer, primary_key=True),
                                        db.Column("evolution_id", db.ForeignKey("evolution.id")),
                                        db.Column("monster_id", db.ForeignKey("monster.id"))
                                        )

class Evolution(db.Model):

    __tablename__ = "evolution"

    id = db.Column(db.Integer, primary_key=True)

    from_monster_id = db.Column(db.Integer, db.ForeignKey("monster.id"), nullable=False)
    from_monster = db.relationship("Monster", backref=backref("evolves_from", uselist=False), foreign_keys="Evolution.from_monster_id")

    to_monster_id = db.Column(db.Integer, db.ForeignKey("monster.id"), nullable=False)
    to_monster = db.relationship("Monster", backref="evolves_to", foreign_keys="Evolution.to_monster_id")

    required_materials = db.relationship("Monster", secondary=required_materials_evolution_n, backref="material_for_evolution")

    def __init__(self):
        pass

    def __str__(self):
        pass