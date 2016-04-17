#!/usr/bin/env python

import sys
sys.path.append("../")

import scrapy
import bs4

from scrapy import signals
from scrapy.xlib.pydispatch import dispatcher

from bs4 import BeautifulSoup

from app.model.base import db
from app.model.awoken_skill import AwokenSkill

class AwokenSkillSpider(scrapy.Spider):
    L_BOUND = 3
    U_BOUND = 40
    name = "awoken_skill_spider"
    allowed_domains = ["http://www.puzzledragonx.com"]
    start_urls = ["http://puzzledragonx.com/en/awokenskill.asp?s=" + \
                  str(i) for i in range(L_BOUND, U_BOUND + 1)]

    def __init__(self, *a, **kw):
        super(AwokenSkillSpider, self).__init__(*a, **kw)

        print("Starting spider")
        db.metadata.drop_all(db.engine, tables=[AwokenSkill.__table__])
        db.metadata.create_all(db.engine, tables=[AwokenSkill.__table__])

        self.awoken_skills = {}

        dispatcher.connect(self.spider_closed, signals.spider_closed)

    def spider_closed(self, spider):

        print("Populating AwokenSkill table")
        for awoken_skill in self.awoken_skills.itervalues():
            db.session.add(awoken_skill)

        db.session.commit()
        print("Populated AwokenSkill table")

        print("AwokenSkills dict contains " + str(len(self.awoken_skills)) + " elements.")
        print("AwokenSkill TABLE contains " + str(len(AwokenSkill.query.all())) + " rows.")

        print("Stopping Spider")

    def parse(self, response):
        as_id = int(response.url.split("s=")[1])
        soup = BeautifulSoup(response.body, "lxml")

        as_tag = soup.find("table", {"id": "tablestat"})
        as_name = as_tag.find("td", text="Name:").find_next("td").string.encode("utf-8")
        as_effect = as_tag.find("td", text="Effect:").find_next("td").string.encode("utf-8")
        as_img_url = as_tag.find("img")["src"]

        monster_list = soup.find("td", {"class" : "listicon"}).find_all("div", {"class" : "relative"})
        owned_by_monsters = []

        for monster in monster_list:
            owned_by_monsters.append(int(monster.find("a")["href"].split("n=")[1]))

        awoken_skill = AwokenSkill(id=as_id, 
                                   name=as_name, 
                                   description=as_effect, 
                                   img="/api/awoken_skill/img/" + str(as_id) + ".png")

        self.awoken_skills[as_id] = awoken_skill

