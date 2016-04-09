#!/usr/bin/env python

import sys
sys.path.append("../")

import scrapy
import bs4

from bs4 import BeautifulSoup
from app.model.awoken_skill import AwokenSkill

class AwokenSkillSpider(scrapy.Spider):
    L_BOUND = 3
    U_BOUND = 36
    name = "awoken_skill_spider"
    allowed_domains = ["http://www.puzzledragonx.com"]
    start_urls = ["http://puzzledragonx.com/en/awokenskill.asp?s=" + \
                  str(i) for i in range(L_BOUND, U_BOUND + 1)]

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

        print(AwokenSkill(id=as_id, 
                          name=as_name, 
                          description=as_effect, 
                          url=as_img_url, 
                          owned_by_monsters=frozenset(owned_by_monsters)))