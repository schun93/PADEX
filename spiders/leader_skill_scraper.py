#!/usr/bin/env python

import sys
sys.path.append("../")

import scrapy
import bs4
import requests

from scrapy import signals
from scrapy.xlib.pydispatch import dispatcher
from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor

from bs4 import BeautifulSoup

from app.model.base import db
from app.model.leader_skill import LeaderSkill

class LeaderSkillScraper(CrawlSpider):
    name = "leader_skill_spider"
    allowed_domains = ["puzzledragonx.com"]
    start_urls = ["http://puzzledragonx.com/en/leaderskill-list.asp"]
    rules = (
        Rule(LinkExtractor(allow=("/leaderskill.asp\?s=.*",), deny=("/leaderskill.asp\?s=.*signin.*")), \
                           callback="parse_leader_skill", follow=True),
    )

    def __init__(self, *a, **kw):
        super(LeaderSkillScraper, self).__init__(*a, **kw)

        print("Starting spider")
        db.metadata.drop_all(db.engine, tables=[LeaderSkill.__table__])
        db.metadata.create_all(db.engine, tables=[LeaderSkill.__table__])

        self.leader_skills = {}

        dispatcher.connect(self.spider_closed, signals.spider_closed)

    def spider_closed(self, spider):

        print("Populating LeaderSkill table")
        for leader_skill in self.leader_skills.itervalues():
            db.session.add(leader_skill)

        db.session.commit()
        print("Populated LeaderSkill table")

        print("LeaderSkills dict contains " + str(len(self.leader_skills)) + " elements.")
        print("LeaderSkill TABLE contains " + str(len(LeaderSkill.query.all())) + " rows.")

        print("Stopping Spider")

    def parse_leader_skill(self, response):
        ls_id = int(response.url.split("s=")[1])
        soup = BeautifulSoup(response.body, "lxml")

        ls_name = soup.find("td", text="Name:").find_next("td").text.encode("utf-8")
        ls_effect = soup.find("td", text="Effect:").find_next("td").text.encode("utf-8")
        ls_original_effect = soup.find("td", text="Original:").find_next("td").text.encode("utf-8")

        owned_by_monsters = [int(monster_tag["href"].encode("utf-8").split("n=")[1]) \
                             for monster_tag in soup.find("h2", text="Ability owned by ...").find_next("td").find_all("a")]

        leader_skill = LeaderSkill(id=ls_id, name=ls_name, effect=ls_effect, original_effect=ls_original_effect)

        self.leader_skills[ls_id] = leader_skill
