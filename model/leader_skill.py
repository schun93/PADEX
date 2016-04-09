#!/usr/bin/env python3

class LeaderSkill:

    def __init__(self, id, name, effect, original_effect, owned_by_monsters=frozenset()):
        self.id = id
        self.name = name
        self.effect = effect
        self.original_effect = original_effect

        # List of foreign keys
        self.owned_by_monsters = owned_by_monsters

    def __str__(self):
        return "LeaderSkill\nID: " + str(self.id) + \
               "\nName: " + self.name + \
               "\nEffect: " + self.effect + \
               "\nOriginal Effect: " + self.original_effect + \
               "\nOwned By Monsters: " + str(self.owned_by_monsters) + \
               "\n"
