class Monster:

    def __init__(self, id, name, primary_type, secondary_type, ternary_type, primary_element, secondary_element, rarity, team_cost, monster_points, evolves_to, min_lvl, max_lvl, min_hp, max_hp, min_atk, max_atk, min_rcv, max_rcv, min_sell_value, max_sell_value, min_exp_feed, max_exp_feed, exp_needed, active_skill, leader_skill, awoken_skills, obtainable_in_dungeons, evolves_from, series_name):
        self.id = id
        self.name = name

        #type_id foreign keys
        self.primary_type = primary_type
        self.secondary_type = secondary_type
        self.ternary_type = ternary_type

        #element_id foreign keys
        self.primary_element = primary_element
        self.secondary_element = secondary_element

        self.rarity = rarity
        self.team_cost = team_cost
        self.monster_points = monster_points

        #evolution_id foreign key
        self.evolves_to = evolves_to

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

        #active_skill_id foreign key
        self.active_skill = active_skill

        #leader_skill_id foreign key
        self.leader_skill = leader_skill

        #List of awoken_skill_id foreign key
        self.awoken_skills = awoken_skills

        #List of dungeon_id foreign key
        self.obtainable_in_dungeons = obtainable_in_dungeons

        #evolution_id foreign key
        self.evolves_from = evolves_from

        #series_id foreign key
        self.series_name = series_name



    def __str__(self):
        return  "ID: " + str(self.id) + \
                "\nName: " + str(self.name) + \
                "\nPrimary Type: " + str(self.primary_type) + \
                "\nSecondary Type: " + str(self.secondary_type) + \
                "\nTernary Type: " + str(self.ternary_type) + \
                "\nPrimary Element: " + str(self.primary_element) + \
                "\nSecondary Element: " + str(self.secondary_element) + \
                "\nRarity: " + str(self.rarity) + \
                "\nTeam Cost: " + str(self.team_cost) + \
                "\nMonster Points: " + str(self.monster_points) + \
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
                "\nObtainable In Dungeon: " + str(self.obtainable_in_dungeons) + \
                "\nSeries Name: " + str(self.series_name) + \
                "\n"

