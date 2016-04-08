#!/usr/bin/env python3

class DungeonMonsterMove:
    def __init__(self, name, atk, chance, hp_threshold, description):
        self.name = name
        self.atk = atk
        self.chance = chance
        self.hp_threshold = hp_threshold
        self.description = description

    def __str__(self):
        return  "Move Information:" + \
                "\nName: " + str(self.name) + \
                "\nATK: " + str(self.atk) + \
                "\nChance: " + str(self.chance) + \
                "\nHP Threshold: " + str(self.hp_threshold) + \
                "\nDescription: " + str(self.description) + \
                "\n"

class DungeonMonster:
    def __init__(self, id, primary_type, secondary_type, ternary_type, hp, atk, defn, turn, moves_info, floor=-1, quantity=-1):
        self.id = id
        self.primary_type = primary_type
        self.secondary_type = secondary_type
        self.ternary_type = ternary_type
        self.hp = hp
        self.atk = atk
        self.defn = defn
        self.floor = floor
        self.quantity = quantity
        self.turn = turn
        self.moves_info = [DungeonMonsterMove(name=move_info[0], \
                                              atk=move_info[1], \
                                              chance=move_info[2], \
                                              hp_threshold=move_info[3], \
                                              description=move_info[4]) for move_info in moves_info]

    def __str__(self):
        moves_string = ""

        for move_info in self.moves_info:
            moves_string += str(move_info) + "\n"

        return  "Dungeon Monster ID: " + str(self.id) + \
                "\nPrimary Type: " + str(self.primary_type) + \
                "\nSecondary Type: " + str(self.secondary_type) + \
                "\nTernary Type: " + str(self.ternary_type) + \
                "\nHP: " + str(self.hp) + \
                "\nATK: " + str(self.atk) + \
                "\nDEF: " + str(self.defn) + \
                "\nFloor: " + str(self.floor) + \
                "\nQuantity: " + str(self.quantity) + \
                "\nTurn: " + str(self.turn) + \
                "\nMoves Info: " + moves_string + \
                "\n"

class Dungeon:

    def __init__(self, id, name, random_encounters, major_encounters):
        self.id = id
        self.name = name
        self.random_encounters = [DungeonMonster(id=encounter[0], \
                                                 primary_type=encounter[1][0], \
                                                 secondary_type=encounter[1][1], \
                                                 ternary_type=encounter[1][2], \
                                                 hp=encounter[5], \
                                                 atk=encounter[3], \
                                                 defn=encounter[4], \
                                                 turn=encounter[2], \
                                                 moves_info=encounter[6]) \
                                                 for encounter in random_encounters]
        self.major_encounters = [DungeonMonster(id=encounter[1], \
                                                primary_type=encounter[3][0], \
                                                secondary_type=encounter[3][1], \
                                                ternary_type=encounter[3][2], \
                                                hp=encounter[7], \
                                                atk=encounter[5], \
                                                defn=encounter[6], \
                                                floor=encounter[0], \
                                                quantity=encounter[2], \
                                                turn=encounter[4], \
                                                moves_info=encounter[8]) for encounter in major_encounters]

    def __str__(self):
        random_encounters_string = ""

        for dungeon_monster in self.random_encounters:
            random_encounters_string += str(dungeon_monster) + "\n"

        major_encounters_string = ""

        for dungeon_monster in self.major_encounters:
            major_encounters_string += str(dungeon_monster) + "\n"

        return  "Dungeon ID: " + str(self.id) + \
                "\nName: " + str(self.name) + \
                "\nRandom Encounters:\n" + random_encounters_string + \
                "\nMajor Encounters:\n" + major_encounters_string + \
                "\n"