#!/usr/bin/env python

import sys
sys.path.append("../")

import scrapy
import bs4
import requests
import re

from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor
from bs4 import BeautifulSoup
from app.model.monster import Monster

class MonsterScraper(CrawlSpider):
    name = "monster_spider"
    allowed_domains = ["puzzledragonx.com"]
    start_urls = ["http://puzzledragonx.com/en/monsterbook.asp"]
    rules = (
        Rule(LinkExtractor(allow=("/monster.asp?.*",), deny=("/monster.asp?.*signin.*", "/monster.asp?.*csort.*", "/monster.asp?.*gray.*")), \
                           callback="parse_monster", follow=True),
    )

    def parse_monster(self, response):
        m_id = int(response.url.split("n=")[1])

        soup = BeautifulSoup(response.body, "lxml")

        m_name = soup.find("span", text="Name").find_next("td", {"class" : "data"}).string.encode("utf-8").strip()

        m_types = [type_tag.string.encode("utf-8") \
                   for type_tag in soup.find("td", text="Type:").find_next("td").find_all("a")]

        while len(m_types) < 3:
            m_types.append(None)

        m_elements = [element_tag.string.encode("utf-8") \
                      for element_tag in soup.find("td", text="Element:").find_next("td").find_all("a")]

        while len(m_elements) < 2:
            m_elements.append(None)

        m_rarity = int(soup.find("td", text="Rarity:").find_next("a").string.split()[0])

        m_cost = int(soup.find("td", text="Cost:").find_next("a").string)

        m_points = soup.find("span", text="M Point").find_next("td", {"class" : "data"}).string
        m_points = -1 if m_points == "--" else int(m_points)

        m_min_lvl = int(soup.find("td", {"class" : "statlevel"}).find_next("td").string)

        m_max_lvl = int(soup.find("td", {"class" : "statlevel"}).find_next("td").find_next("td").string)

        m_min_hp = int(soup.find("td", {"class" : "stathp"}).find_next("td").string)
        
        m_max_hp = int(soup.find("td", {"class" : "statlevel"}).find_next("td").find_next("td").string)
        
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
                         if m_active_skill != None else -1
        
        m_leader_skill = soup.find("a", href=re.compile("^leaderskill.asp\?s="))
        m_leader_skill = int(m_leader_skill["href"].split("s=")[1]) \
                         if m_leader_skill != None else -1

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

        # If Evo Material or Enhance Material don't check for Exp necessary to max
        print(Monster(id=m_id, name=m_name, primary_type=m_types[0], \
                      secondary_type=m_types[1], ternary_type=m_types[2], primary_element=m_elements[0], \
                      secondary_element=m_elements[1], rarity=m_rarity, team_cost=m_cost, \
                      monster_points=m_points, evolves_to=m_evolves_to, min_lvl=m_min_lvl, \
                      max_lvl=m_max_lvl, min_hp=m_min_hp, max_hp=m_max_hp, \
                      min_atk=m_min_atk, max_atk=m_max_atk, min_rcv=m_min_rcv, \
                      max_rcv=m_max_rcv, min_sell_value=m_min_sell, max_sell_value=m_max_sell, \
                      min_exp_feed=m_min_feed_exp, max_exp_feed=m_max_feed_exp, exp_needed=m_exp_curve, \
                      active_skill=m_active_skill, leader_skill=m_leader_skill, awoken_skills=m_awoken_skills, \
                      obtainable_in_dungeons=m_obtained_in_dungeons, evolves_from=m_evolves_from, series_name=m_series_name))


