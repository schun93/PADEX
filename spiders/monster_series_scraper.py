#!/usr/bin/env python

import sys
sys.path.append("../")

import scrapy
import bs4
import re

from scrapy import signals
from scrapy.xlib.pydispatch import dispatcher

from bs4 import BeautifulSoup

from app.model.base import db
from app.model.monster_series import MonsterSeries

class MonsterSeriesScraper(scrapy.Spider):
    L_BOUND = 0
    U_BOUND = 146
    name = "awoken_skill_spider"
    allowed_domains = ["http://www.puzzledragonx.com"]
    start_urls = ["http://puzzledragonx.com/en/monsterbook.asp?s=" + str(i) \
                 for i in range(L_BOUND, U_BOUND + 1)]

    def __init__(self, *a, **kw):
        super(MonsterSeriesScraper, self).__init__(*a, **kw)

        print("Starting spider")
        db.metadata.drop_all(db.engine, tables=[MonsterSeries.__table__])
        db.metadata.create_all(db.engine, tables=[MonsterSeries.__table__])

        self.monster_series = {}

        dispatcher.connect(self.spider_closed, signals.spider_closed)

    def spider_closed(self, spider):

        print("Populating MonsterSeries table")
        print("MonsterSeriess dict contains " + str(len(self.monster_series)) + " elements.")
        for monster_serie in self.monster_series.itervalues():
            db.session.add(monster_serie)
        db.session.commit()
        print("Populated MonsterSeries table")

        print("MonsterSeries TABLE contains " + str(len(MonsterSeries.query.all())) + " rows.")

        print("Stopping Spider")

    def parse(self, response):
        soup = BeautifulSoup(response.body, "lxml")

        s_id = int(response.url.split("s=")[1])

        if s_id == 0:
            s_name = "Uncategorized"
        elif s_id == 93:
            s_name = "Spirit Jewels Event"
        elif s_id == 121:
            s_name = "Angel & Reaper Event"
        elif s_id == 128:
            s_name = "Skill-Up Set"
        else:
            s_name = soup.find("input", {"name" : "category", "value": str(s_id)}).find_next("td").string.encode("utf-8")

        s_monsters = [int(monster_tag["href"].split("n=")[1]) \
                     for monster_tag in soup.find("h2", text="Card Catalogue").find_previous("table", {"id" : "tablestat"}).find_all("a", href=re.compile("^monster.asp\?n="))]

        monster_series = MonsterSeries(id=s_id, name=s_name)

        self.monster_series[s_id] = monster_series