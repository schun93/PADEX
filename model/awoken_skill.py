#!/usr/bin/env python3

class AwokenSkill:

    def __init__(self, id, name, description, url, owned_by_monsters):
        self.id = id
        self.name = name
        self.description = description
        self.url = url

        # List of monster_id foreign keys
        self.owned_by_monsters = owned_by_monsters

    def __str__(self):
        return  "ID: " + str(self.id) + \
                "\nName: " + self.name + \
                "\nEffect: " + self.description + \
                "\nImg: " + self.url + \
                "\nMonsters: " + str(self.owned_by_monsters) + \
                "\n"
