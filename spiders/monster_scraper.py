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
from app.model.monster import Monster, CommonMonster, awoken_skill_monster_n
from app.model.type import Type
from app.model.element import Element
from app.model.active_skill import ActiveSkill
from app.model.leader_skill import LeaderSkill
from app.model.awoken_skill import AwokenSkill
from app.model.monster_series import MonsterSeries

class MonsterScraper(CrawlSpider):
    name = "monster_spider"
    allowed_domains = ["puzzledragonx.com"]
    start_urls = ["http://puzzledragonx.com/en/monsterbook.asp"]
    rules = (
        Rule(LinkExtractor(allow=("/monster.asp?.*",), deny=("/monster.asp?.*signin.*", "/monster.asp?.*csort.*", "/monster.asp?.*gray.*")), \
                           callback="parse_monster", follow=True),
    )

    def __init__(self, *a, **kw):
        super(MonsterScraper, self).__init__(*a, **kw)

        print("Starting spider")
        db.metadata.drop_all(db.engine, tables=[awoken_skill_monster_n])
        db.metadata.drop_all(db.engine, tables=[CommonMonster.__table__])
        db.metadata.drop_all(db.engine, tables=[Monster.__table__])
        db.metadata.drop_all(db.engine, tables=[Element.__table__])
        db.metadata.drop_all(db.engine, tables=[Type.__table__])
        # db.metadata.drop_all(db.engine, tables=[Type.__table__, Element.__table__, Monster.__table__, CommonMonster.__table__, awoken_skill_monster_n])
        db.metadata.create_all(db.engine, tables=[awoken_skill_monster_n, Monster.__table__, CommonMonster.__table__, Type.__table__, Element.__table__])

        self.monsters = {}
        self.common_monsters = {}
        self.types = {}
        self.elements = {}

        dispatcher.connect(self.spider_closed, signals.spider_closed)

    def spider_closed(self, spider):
        print("Populating Monster table")
        for monster in self.monsters.itervalues():
            print("Monster ID: " + str(monster.id))
            # db.session.add(monster)
            # db.session.commit()

        for common_monster in self.common_monsters.itervalues():
            print("Common Monster ID: " + str(common_monster.id))
            # db.session.add(common_monster)
            # db.session.commit()

        for type in self.types.itervalues():
            print("Type ID: " + str(type.id))
            # db.session.add(type)
            # db.session.commit()

        for element in self.elements.itervalues():
            print("Element ID: " + str(element.id))
            # db.session.add(element)
            # db.session.commit()

        print("Populated Monster table")

        print("Monsters dict contains " + str(len(self.monsters)) + " elements.")
        print("Monster TABLE contains " + str(len(Monster.query.all())) + " rows.")

        print("Populated CommonMonster table")

        print("CommonMonsters dict contains " + str(len(self.common_monsters)) + " elements.")
        print("CommonMonster TABLE contains " + str(len(CommonMonster.query.all())) + " rows.")

        print("Types dict contains " + str(len(self.types)) + " elements.")
        print("Type TABLE contains " + str(len(Type.query.all())) + " rows.")

        print("Elements dict contains " + str(len(self.elements)) + " elements.")
        print("Element TABLE contains " + str(len(Element.query.all())) + " rows.")

        print("Stopping Spider")

    def parse_monster(self, response):
        m_id = int(response.url.split("n=")[1])

        soup = BeautifulSoup(response.body, "lxml")

        m_name = soup.find("span", text="Name").find_next("td", {"class" : "data"}).string.encode("utf-8").strip()

        m_types = [(type_tag.string.encode("utf-8"), int(type_tag["href"].split("t" + str(i + 1) + "=")[1].split("&")[0])) \
                   for (i, type_tag) in enumerate(soup.find("td", text="Type:").find_next("td").find_all("a"))]

        while len(m_types) < 3:
            m_types.append((None, None))

        m_elements = [(element_tag.string.encode("utf-8"), int(element_tag["href"].split("e" + str(i + 1) + "=")[1].split("&")[0])) \
                      for (i, element_tag) in enumerate(soup.find("td", text="Element:").find_next("td").find_all("a"))]

        while len(m_elements) < 2:
            m_elements.append((None, None))

        m_rarity = int(soup.find("td", text="Rarity:").find_next("a").string.split()[0])

        m_cost = int(soup.find("td", text="Cost:").find_next("a").string)

        m_points = soup.find("span", text="M Point").find_next("td", {"class" : "data"}).string
        m_points = -1 if m_points == "--" else int(m_points)

        m_min_lvl = int(soup.find("td", {"class" : "statlevel"}).find_next("td").string)

        m_max_lvl = int(soup.find("td", {"class" : "statlevel"}).find_next("td").find_next("td").string)

        m_min_hp = int(soup.find("td", {"class" : "stathp"}).find_next("td").string)
        
        m_max_hp = int(soup.find("td", {"class" : "stathp"}).find_next("td").find_next("td").string)
        
        m_min_atk = int(soup.find("td", {"class" : "statatk"}).find_next("td").string)
        
        m_max_atk = int(soup.find("td", {"class" : "statatk"}).find_next("td").find_next("td").string)
        
        m_min_rcv = int(soup.find("td", {"class" : "statrcv"}).find_next("td").string)
        
        m_max_rcv = int(soup.find("td", {"class" : "statrcv"}).find_next("td").find_next("td").string)
        
        m_min_sell = int(soup.find("td", {"class" : "statsell"}).find_next("td").string)
        
        m_max_sell = int(soup.find("td", {"class" : "statsell"}).find_next("td").find_next("td").string)
        
        m_min_feed_exp = int(soup.find("td", {"class" : "statexp"}).find_next("td").contents[0])
        
        m_max_feed_exp = int(soup.find("td", {"class" : "statexp"}).find_next("td").find_next("td").contents[0])
        
        m_exp_curve = soup.find("a", href=re.compile("^experiencechart.asp"))
        m_exp_curve = int(m_exp_curve.string.replace(",", "")) \
                      if m_exp_curve != None else 0
        
        m_active_skill = soup.find("a", href=re.compile("^skill.asp\?s="))
        m_active_skill = int(m_active_skill["href"].split("s=")[1]) \
                         if m_active_skill != None else None
        
        m_leader_skill = soup.find("a", href=re.compile("^leaderskill.asp\?s="))
        m_leader_skill = int(m_leader_skill["href"].split("s=")[1]) \
                         if m_leader_skill != None else None

        m_awoken_skills = soup.find("td", {"class" : "awoken1"})
        m_awoken_skills = [int(awoken_skill_tag["href"].split("s=")[1]) \
                          for awoken_skill_tag in m_awoken_skills.find_all("a", href=re.compile("^awokenskill.asp\?s="))] \
                          if m_awoken_skills != None else []

        # Add JP Awoken Skills

        m_obtained_in_dungeons = [int(dungeon_tag["href"].split("m=")[1]) 
                                 for dungeon_tag in soup.find("h2", text=("Drop Locations for #" + str(m_id))).find_next("table", {"id" : "tablestat"}).find_all("a", href=re.compile("^mission.asp\?m="))]

        m_evolves_from = soup.find("td", {"class": "title", "colspan": "4", "style": "white-space: nowrap;"})
        m_evolves_from = int(m_evolves_from.find_next("a", href=re.compile("^monster.asp\?n="))["href"].split("n=")[1]) \
                         if any("Evolution" in text for text in m_evolves_from.contents) else -1

        m_series_name = soup.find("span", text=re.compile("Series")).string.split(" Series")[0]



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
            assert MonsterSeries.query.filter_by(name=m_series_name).first() != None

            if m_active_skill != None:
                assert ActiveSkill.query.filter_by(id=m_active_skill).first() != None

            if m_leader_skill != None:
                assert LeaderSkill.query.filter_by(id=m_leader_skill).first() != None

            awoken_skills = [AwokenSkill.query.filter_by(id=awoken_skill_id).first() for awoken_skill_id in m_awoken_skills]

            # If Evo Material or Enhance Material don't check for Exp necessary to max
            monster = Monster(id=m_id, name=m_name, rarity=m_rarity, team_cost=m_cost, \
                              sells_for_monster_points=m_points, min_lvl=m_min_lvl, \
                              max_lvl=m_max_lvl, min_hp=m_min_hp, max_hp=m_max_hp, \
                              min_atk=m_min_atk, max_atk=m_max_atk, min_rcv=m_min_rcv, \
                              max_rcv=m_max_rcv, min_sell_value=m_min_sell, max_sell_value=m_max_sell, \
                              min_exp_feed=m_min_feed_exp, max_exp_feed=m_max_feed_exp, exp_needed=m_exp_curve)
            monster.monster_series = MonsterSeries.query.filter_by(name=m_series_name).first()
            monster.active_skill = ActiveSkill.query.filter_by(id=m_active_skill).first()
            monster.leader_skill = LeaderSkill.query.filter_by(id=m_leader_skill).first()
            monster.awoken_skills = awoken_skills

            primary_type = Type(id=m_types[0][1], name=m_types[0][0])
            secondary_type = Type(id=m_types[1][1], name=m_types[1][0]) if m_types[1][1] != None else None
            ternary_type = Type(id=m_types[2][1], name=m_types[2][0]) if m_types[2][1] != None else None

            primary_element = Element(id=m_elements[0][1], name=m_elements[0][0])
            secondary_element = Element(id=m_elements[1][1], name=m_elements[1][0]) if m_elements[1][1] != None else None

            if primary_type != None and Type.query.filter_by(id=primary_type.id).first() != None:
                # print("P Type ID: " + str(primary_type.id))
                primary_type = Type.query.filter_by(id=primary_type.id).first()

            if secondary_type != None and Type.query.filter_by(id=secondary_type.id).first() != None:
                # print("S Type ID: " + str(secondary_type.id))
                secondary_type = Type.query.filter_by(id=secondary_type.id).first()

            if ternary_type != None and Type.query.filter_by(id=ternary_type.id).first() != None:
                # print("T Type ID: " + str(ternary_type.id))
                ternary_type = Type.query.filter_by(id=ternary_type.id).first()

            if primary_element != None and Element.query.filter_by(id=primary_element.id).first() != None:
                # print("P Element ID: " + str(primary_element.id))
                primary_element = Element.query.filter_by(id=primary_element.id).first()

            if secondary_element != None and Element.query.filter_by(id=secondary_element.id).first() != None:
                # print("S Element ID: " + str(secondary_element.id))
                secondary_element = Element.query.filter_by(id=secondary_element.id).first()

            common_monster = CommonMonster(id=m_id, name=m_name, img="/api/monster/img/" + str(m_id) + ".png", thmb="/api/monster/thmb/" + str(m_id) + ".png")
            common_monster.primary_type = primary_type
            common_monster.secondary_type = secondary_type
            common_monster.ternary_type = ternary_type
            common_monster.primary_element = primary_element
            common_monster.secondary_element = secondary_element
            common_monster.monster = monster

            self.types[m_types[0][1]] = primary_type
            self.types[m_types[1][1]] = secondary_type
            self.types[m_types[2][1]] = ternary_type
            self.elements[m_elements[0][1]] = primary_element
            self.elements[m_elements[1][1]] = secondary_element
            self.common_monsters[m_id] = common_monster
            self.monsters[m_id] = monster

            # print("Monster ID: " + str(monster.id))
            db.session.add(monster)
            db.session.commit()

            # print("Common Monster ID: " + str(common_monster.id))
            db.session.add(common_monster)
            db.session.commit()

