#!/usr/bin/env python

import sys
sys.path.append("../")

import scrapy
import bs4
import requests

from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor
from bs4 import BeautifulSoup
from app.model.leader_skill import LeaderSkill

class LeaderSkillScraper(CrawlSpider):
    name = "leader_skill_spider"
    allowed_domains = ["puzzledragonx.com"]
    start_urls = ["http://puzzledragonx.com/en/leaderskill-list.asp"]
    rules = (
        Rule(LinkExtractor(allow=("/leaderskill.asp\?s=.*",), deny=("/leaderskill.asp\?s=.*signin.*")), \
                           callback="parse_leader_skill", follow=True),
    )

    def parse_leader_skill(self, response):
        ls_id = int(response.url.split("s=")[1])
        soup = BeautifulSoup(response.body, "lxml")

        ls_name = soup.find("td", text="Name:").find_next("td").text.encode("utf-8")
        ls_effect = soup.find("td", text="Effect:").find_next("td").text.encode("utf-8")
        ls_original_effect = soup.find("td", text="Original:").find_next("td").text.encode("utf-8")

        owned_by_monsters = [int(monster_tag["href"].encode("utf-8").split("n=")[1]) \
                             for monster_tag in soup.find("h2", text="Ability owned by ...").find_next("td").find_all("a")]

        print(LeaderSkill(id=ls_id, name=ls_name, effect=ls_effect, original_effect=ls_original_effect, owned_by_monsters=owned_by_monsters))