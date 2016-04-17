#!/usr/bin/env python

import sys
sys.path.append("../")

import scrapy
import bs4
import requests

from flask import Flask

from scrapy import signals
from scrapy.xlib.pydispatch import dispatcher
from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor
from bs4 import BeautifulSoup

from app.model.base import db
from app.model.active_skill import ActiveSkill

class ActiveSkillSpider(CrawlSpider):
    name = "active_skill_spider"
    allowed_domains = ["puzzledragonx.com"]
    start_urls = ["http://puzzledragonx.com/en/skill-list.asp"]
    rules = (
        Rule(LinkExtractor(allow=("/skill.asp?.*",), deny=("/skill.asp?.*signin.*")), \
                           callback="parse_active_skill", follow=True),
    )

    def __init__(self, *a, **kw):
        super(ActiveSkillSpider, self).__init__(*a, **kw)

        print("Starting spider")
        db.metadata.drop_all(db.engine, tables=[ActiveSkill.__table__])
        db.metadata.create_all(db.engine, tables=[ActiveSkill.__table__])

        self.active_skills = {}

        dispatcher.connect(self.spider_closed, signals.spider_closed)

    def spider_closed(self, spider):

        print("Populating ActiveSkill table")
        for active_skill in self.active_skills.itervalues():
            db.session.add(active_skill)

        db.session.commit()
        print("Populated ActiveSkill table")

        print("ActiveSkills dict contains " + str(len(self.active_skills)) + " elements.")
        print("ActiveSkill TABLE contains " + str(len(ActiveSkill.query.all())) + " rows.")

        print("Stopping Spider")

    def parse_active_skill(self, response):
        as_id = int(response.url.split("s=")[1])

        soup = BeautifulSoup(response.body, "lxml")

        as_tag  = soup.find("table", {"id" : "tablestat"})    
        as_name = as_tag.find("td", text="Name:").find_next("td").string.encode("utf-8").strip()
        as_effect = as_tag.find("td", text="Effect:").find_next("td")

        if as_effect.find_next("a") != None:
            result = as_effect.contents[0]
            
            for effect in as_effect.find_all("a"):
                result += effect.string + ", "

            as_effect = result.strip(", ").encode("utf-8")
        else:
            as_effect = as_effect.string.strip()

        as_original_effect = as_tag.find("td", text="Original:").find_next("td").string.encode("utf-8").strip()

        as_max_cd = as_tag.find("td", text="Max CD:").find_next("td").string.encode("utf-8").strip()
        as_min_cd = as_tag.find("td", text="Min CD:").find_next("td").string.encode("utf-8").strip()
        as_max_lvl = as_tag.find("td", text="Max Lv:").find_next("td").string.encode("utf-8").strip()

        owned_by_monsters_tag = as_tag.find_next("table", {"id" : "tablestat"})
        owned_by_monsters = []

        for monster_tag in owned_by_monsters_tag.find_all("a"):
            owned_by_monsters.append(int(monster_tag["href"].split("n=")[1]))

        active_skill = ActiveSkill(id=as_id, 
                                   name=as_name, 
                                   effect=as_effect, 
                                   original_effect=as_original_effect, 
                                   max_cd=as_max_cd, 
                                   min_cd=as_min_cd, 
                                   max_lvl=as_max_lvl)

        self.active_skills[as_id] = active_skill
