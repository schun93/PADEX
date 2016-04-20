#!/usr/bin/env python

import sys
sys.path.append("../")

import scrapy
import bs4
import requests
import re

from scrapy import signals
from scrapy.xlib.pydispatch import dispatcher

from app.model.base import db
from app.model.dungeon import *
from app.model.monster import *
from app.model.type import *
from app.model.element import *
from app.model.monster_series import *
from app.model.active_skill import *
from app.model.leader_skill import *
from app.model.awoken_skill import *

from bs4 import BeautifulSoup

class EventScraper(scrapy.Spider):
    name = "event_spider"
    allowed_domains = ["http://www.puzzledragonx.com"]
    start_urls = ["http://puzzledragonx.com/en/mission.asp?m=680"]

    def __init__(self, *a, **kw):
        super(EventScraper, self).__init__(*a, **kw)

        print("Starting spider")
        db.metadata.drop_all(db.engine, tables=[EnemyMoveType.__table__])
        db.metadata.create_all(db.engine, tables=[EnemyMoveType.__table__])

        dispatcher.connect(self.spider_closed, signals.spider_closed)

    def spider_closed(self, spider):
        print("Stopping spider")

    def parse(self, response):
        soup = BeautifulSoup(response.body, "lxml")

        imgs = soup.find_all("img", {"data-original": re.compile("^img/skill/")})

        for img in imgs:
            text = img.find_previous("td").text.encode("utf-8")

            if len(text) > 16:
                continue

            img_id = int(img["data-original"].split("img/skill/")[1].split(".png")[0])
            url = "/api/v1/enemy_move_type/" + str(img_id) + ".png"

            move_type = EnemyMoveType(id=img_id, name=text, img=url)

            db.session.add(move_type)

        db.session.commit()
