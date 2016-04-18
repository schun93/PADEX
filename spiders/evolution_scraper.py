#!/usr/bin/env python

import sys
sys.path.append("../")

import scrapy
import bs4
import requests
import re

from scrapy import signals
from scrapy.xlib.pydispatch import dispatcher
from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor
from bs4 import BeautifulSoup

from app.model.base import db
from app.model.monster_series import MonsterSeries
from app.model.active_skill import ActiveSkill
from app.model.leader_skill import LeaderSkill
from app.model.awoken_skill import AwokenSkill
from app.model.type import Type
from app.model.element import Element
from app.model.monster import Monster, CommonMonster, Evolution, required_materials_evolution_n

class EvolutionScraper(CrawlSpider):
    name = "monster_spider"
    allowed_domains = ["puzzledragonx.com"]
    start_urls = ["http://puzzledragonx.com/en/monsterbook.asp"]
    rules = (
        Rule(LinkExtractor(allow=("/monster.asp?.*",), deny=("/monster.asp?.*signin.*", "/monster.asp?.*csort.*", "/monster.asp?.*gray.*")), \
                           callback="parse_evolution", follow=True),
    )

    def __init__(self, *a, **kw):
        super(EvolutionScraper, self).__init__(*a, **kw)

        print("Starting spider")
        db.metadata.drop_all(db.engine, tables=[Evolution.__table__, required_materials_evolution_n])
        db.metadata.create_all(db.engine, tables=[required_materials_evolution_n, Evolution.__table__])

        dispatcher.connect(self.spider_closed, signals.spider_closed)

    def spider_closed(self, spider):
        print("Stopping spider")

    def parse_evolution(self, response):
        m_id = int(response.url.split("n=")[1])

        soup = BeautifulSoup(response.body, "lxml")

        m_evolves_from = soup.find("td", {"class": "title", "colspan": "4", "style": "white-space: nowrap;"})
        m_evolves_from = int(m_evolves_from.find_next("a", href=re.compile("^monster.asp\?n="))["href"].split("n=")[1]) \
                         if any("Evolution" in text for text in m_evolves_from.contents) else None

        #Try/Except necessary because some monsters like Cecil's light form are not obtainable
        try:
            initial_evolve_tag = soup.find("div", {"class" : "eframenum"}, text=str(m_id)).find_next("div", {"class" : "eframenum"})
        except:
            initial_evolve_tag = None
        finally:
            m_evolves_to = []

        # None here would mean it doesn't have a next evolution
        if initial_evolve_tag != None:
            # Regular Evolution is next
            if initial_evolve_tag.find_previous("td", {"class" : "finalevolve nowrap"}) == None:
                # print("Regular Evolution")
                evolve_index = next((i for i, evolve_tag in enumerate(initial_evolve_tag.find_previous("tr").find_all("td", {"class" : "evolve"})) \
                               if evolve_tag.find_next("div", {"class" : "eframenum"}).string == str(m_id)))

                evo_to = int(initial_evolve_tag.string)
                evo_to_materials = [int(evo_material_tag["href"].split("n=")[1]) \
                                   for evo_material_tag in initial_evolve_tag.find_previous("tr").find_next("tr").find_all("td", {"class" : "require"})[evolve_index].find_all("a")] \
                                   if evolve_index != -1 else []

                m_evolves_to.append((evo_to, evo_to_materials))
            # Ultimate Evolutions are next
            elif initial_evolve_tag.find_previous("td", {"class" : "finalevolve nowrap"}) != None and \
                 initial_evolve_tag.find_previous("td", {"class" : "awokenevolve"}) == None and \
                 initial_evolve_tag.find_previous("div", {"class" : "eframenum"}).find_previous("td", {"class" : "finalevolve nowrap"}) == None:
                # print("Ultimate Evolution")
                while initial_evolve_tag != None and \
                      initial_evolve_tag.find_previous("td", {"class" : "finalevolve nowrap"}) != None:
                    evo_to = int(initial_evolve_tag.string)
                    evo_to_materials = [int(evo_material_tag["href"].split("n=")[1]) for evo_material_tag in initial_evolve_tag.find_previous("td", {"class" : "finalevolve nowrap"}).find_all("a")]

                    m_evolves_to.append((evo_to, evo_to_materials))

                    if initial_evolve_tag.find_next("td", {"class" : "evolve"}) == None:
                        break

                    initial_evolve_tag = initial_evolve_tag.find_next("td", {"class" : "evolve"}).find_next("div", {"class" : "eframenum"})
            # Super Ultimate Evolutions are next
            else:
                if initial_evolve_tag.find_parent("td", {"class" : "evolve"}) == None:
                    # print("Super Ultimate Evolution")
                    evo_to = int(initial_evolve_tag.string)
                    evo_to_materials = [int(evo_material_tag["href"].split("n=")[1]) \
                                       for evo_material_tag in initial_evolve_tag.find_next("td", {"class" : "finalawokenevolve nowrap"}).find_all("a")]
                    m_evolves_to.append((evo_to, evo_to_materials))

        with db.session.no_autoflush:
            from_monster = Monster.query.filter_by(id=m_id).first()

            for evolves_to_id, materials in m_evolves_to:
                if Evolution.query.filter_by(to_monster_id=evolves_to_id).first() == None:
                    required_materials = [Monster.query.filter_by(id=material_id).first() for material_id in materials]

                    evolution = Evolution()
                    evolution.from_monster = from_monster
                    evolution.to_monster = Monster.query.filter_by(id=evolves_to_id).first()
                    evolution.required_materials = required_materials

                    db.session.add(evolution)
            db.session.commit()
