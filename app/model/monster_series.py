class MonsterSeries:

    def __init__(self, id, name, monsters_in_series=frozenset()):
        self.id = id
        self.name = name
        self.monsters_in_series = monsters_in_series

    def __str__(self):
        return "MonsterSeries\nID: " + str(self.id) + \
               "\nName: " + self.name + \
               "\nMonsters in series: " + str(self.monsters_in_series) + \
               "\n"
