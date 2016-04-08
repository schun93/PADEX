#!/usr/bin/env python

import scrapy
import bs4
import requests
import re

from bs4 import BeautifulSoup

class EventScraper(scrapy.Spider):
    name = "event_spider"
    allowed_domains = ["http://www.puzzledragonx.com"]
    start_urls = ["http://puzzledragonx.com"]

    def obtain_alert_events(self, event_table_tag):
        alert_event_dungeons = [[], [], [], [], []]

        for (i, events_tag) in enumerate(event_table_tag):
            if i % 2 == 0:
                group_count = 0
                group_events = []
                for (j, event_tag) in enumerate(events_tag.find_all("td")):
                    if j % 3 == 2:
                        alert_event_dungeons[group_count].append(group_events)
                        group_count += 1
                        group_events = []
                    else:
                        try:
                            d_id = requests.get("http://puzzledragonx.com/" + event_tag.find("a")["href"]).url.encode("utf-8").split("m=")[1]
                            group_events.append(d_id)
                        except:
                            group_events.append(None)

                alert_event_dungeons[group_count].append(group_events)

        return alert_event_dungeons

    def obtain_alert_times(self, event_table_tag):
        alert_event_times = [[], [], [], [], []]

        for times_tag in event_table_tag:
            for (i, time_tag) in enumerate(times_tag.find_all("td", {"class" : "metaltime"})):
                alert_event_times[i].append(time_tag.text.encode("utf-8"))

        return alert_event_times

    def obtain_weekly_dungeon_events(self, weekly_event_table_tag):
        events = []

        for dungeon_tag in weekly_event_table_tag.find_all("tr"):
            dungeon_date_tag = dungeon_tag.find("td", {"class" : "eventdate"})
            if dungeon_date_tag:
                start_date = dungeon_date_tag.find("span", {"class" : "brown"}).text.split()[0].encode("utf-8")
                start_time = dungeon_date_tag.find("span", {"class" : "brown"}).text.split()[1].encode("utf-8")
                end_date =  dungeon_date_tag.find("br").next_sibling.string.split()[0].encode("utf-8")
                end_time = dungeon_date_tag.find("br").next_sibling.string.split()[1].encode("utf-8")
                
                try:
                    d_id = int(dungeon_tag.find("td", {"class" : "eventname"}).find_next("a")["href"].split("m=")[1])
                except:
                    d_id = None

                try:
                    e_info = dungeon_tag.find("td", {"class" : "eventname"}).text.encode("utf-8")
                except:
                    e_info = None

                events.append([(start_date, end_date), (start_time, end_time), d_id, e_info])

        return events

    def parse(self, response):
        soup = BeautifulSoup(response.body, "lxml")

        event_table_tag = soup.find("div", id="metal1a").find_next("table", id="event").find_all("tr")
        event_table_tag.pop(0)

        print("Today's Events:")
        print(self.obtain_alert_events(event_table_tag))
        print(self.obtain_alert_times(event_table_tag))

        tomorrow_table_tag = soup.find("div", id="metal1b").find_next("table", id="event").find_all("tr")
        tomorrow_table_tag.pop(0)

        print("Tomorrow's Events:")
        print(self.obtain_alert_events(tomorrow_table_tag))
        print(self.obtain_alert_times(tomorrow_table_tag))

        weekly_event_dungeon_table_tag = soup.find("h2", text=re.compile("NA Puzzle & Dragons Dungeon Schedule")) \
                                             .find_previous("table", id="event")

        print("Weekly Dungeon Event:")
        print(self.obtain_weekly_dungeon_events(weekly_event_dungeon_table_tag))

        weekly_event_table_tag = weekly_event_dungeon_table_tag.find_next("table", id="event")

        print("Weekly Event:")
        print(self.obtain_weekly_dungeon_events(weekly_event_table_tag))

