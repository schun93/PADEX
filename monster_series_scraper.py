#!/usr/bin/env python

import scrapy
import bs4
import model
import re

from bs4 import BeautifulSoup

class MonsterSeriesScraper(scrapy.Spider):
    L_BOUND = 0
    U_BOUND = 145
    name = "awoken_skill_spider"
    allowed_domains = ["http://www.puzzledragonx.com"]
    start_urls = ["http://puzzledragonx.com/en/monsterbook.asp?s=" + str(i) \
                 for i in range(L_BOUND, U_BOUND + 1)]

    def parse(self, response):
        soup = BeautifulSoup(response.body, "lxml")

        s_id = int(response.url.split("s=")[1])
        s_name = soup.find("input", {"name" : "category", "value": str(s_id)}).find_next("td").string
        s_monsters = [int(monster_tag["href"].split("n=")[1]) \
                     for monster_tag in soup.find("h2", text="Card Catalogue").find_previous("table", {"id" : "tablestat"}).find_all("a", href=re.compile("^monster.asp\?n="))]

        print("Series ID: " + str(s_id))
        print("Series Name: " + str(s_name))
        print("Monsters in Series: " + str(s_monsters))
        print("")