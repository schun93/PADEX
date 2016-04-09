class EventDungeon:

    def __init__(self, start_date, end_date, start_time, end_time, dungeon_id, event_info):
        self.start_date = start_date
        self.end_date = end_date
        self.start_time = start_time
        self.end_time = end_time
        self.dungeon_id = dungeon_id
        self.event_info = event_info


    def __str__(self):
        return  "Event\nStart Date: " + str(self.start_date) + \
                "\nEnd Date: " + str(self.end_date) + \
                "\nStart Time: " + str(self.start_time) + \
                "\nEnd Time: " + str(self.end_time) + \
                "\nDungeon ID: " + str(self.dungeon_id) + \
                "\nInfo: " + str(self.event_info) + \
                "\n"


class DailyDungeon:
    def __init__(self, dungeon_id, start_time):
        self.dungeon_id = dungeon_id
        self.start_time = start_time

    def __str__(self):
        return "Daily Dungeon:\nDungeon ID: " + str(self.dungeon_id) + \
               "\nStart Time: " + str(self.start_time) + \
               "\n"