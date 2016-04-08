#!/usr/bin/env python3

class ActiveSkill:

    def __init__(self, id, name, effect, original_effect, max_cd, min_cd, max_lvl, owned_by_monsters=frozenset()):
        self.id = id
        self.name = name
        self.effect = effect
        self.original_effect = original_effect
        self.max_cd = max_cd
        self.min_cd = min_cd
        self.max_lvl = max_lvl

        # List of foreign keys
        self.owned_by_monsters = owned_by_monsters

    def __str__(self):
        return "ActiveSkill\nID: " + str(self.id) + \
               "\nName: " + self.name + \
               "\nEffect: " + self.effect + \
               "\nOriginal Effect: " + self.original_effect + \
               "\nMax CD: " + self.max_cd + \
               "\nMin CD: " + self.min_cd + \
               "\nMax Lvl: " + self.max_lvl + \
               "\nOwned By Monsters: " + str(self.owned_by_monsters) + \
               "\n"
