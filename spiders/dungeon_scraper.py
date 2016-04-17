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
from app.model.monster import CommonMonster
from app.model.dungeon import Dungeon, EnemySkill, EnemyMove, EnemyMonster

def represents_int(s):   
    try: 
        int(s)
        return True
    except ValueError:
        return False
    except TypeError:
        return False

class DungeonScraper(CrawlSpider):
    name = "dungeon_spider"
    allowed_domains = ["puzzledragonx.com"]
    start_urls = [
        "http://puzzledragonx.com/en/normal-dungeons.asp",
        "http://puzzledragonx.com/en/special-dungeons.asp", 
        "http://puzzledragonx.com/en/technical-dungeons.asp",
        "http://puzzledragonx.com/en/multiplayer-dungeons.asp"
    ]
    rules = (
        Rule(LinkExtractor(allow=("/mission.asp\?m=.*",), deny=("/mission.asp.*csort.*", "/mission.asp.*signin.*")), \
                           callback="parse_dungeon", follow=True),
    )

    def __init__(self, *a, **kw):
        super(DungeonScraper, self).__init__(*a, **kw)

        print("Starting spider")
        db.metadata.drop_all(db.engine, tables=[EnemySkill.__table__, EnemyMove.__table__, Dungeon.__table__, EnemyMonster.__table__])
        db.metadata.create_all(db.engine, tables=[EnemyMonster.__table__, Dungeon.__table__, EnemyMove.__table__, EnemySkill.__table__])

        dispatcher.connect(self.spider_closed, signals.spider_closed)

    def spider_closed(self, spider):
        print("Stopping spider")

    def obtain_encounter_quantity(self, tag):
        try:
            return int(tag.find_next("td", {"class" : "quantity"}).contents[0].split("x ")[1].encode("utf-8"))
        except:
            return 1

    def obtain_floor_number(self, tag):
        return int(tag.find_next("td").string.encode("utf-8"))

    def obtain_encounter_monster(self, tag):
        return int(tag.find_next("a", href=re.compile("^monster.asp\?n="))["href"].split("n=")[1].encode("utf-8"))

    def obtain_encounter_type(self, tag):
        types = [type_tag["title"] for type_tag in tag.find_next("div", {"class" : "type"}).find_all("img")]

        while len(types) < 3:
            types.append(None)

        return tuple(types)

    def obtain_turn_number(self, tag):
        try:
            return int(tag.find_next("td", {"class" : "quantity"}).next_sibling.string.encode("utf-8"))
        except:
            return 1

    def obtain_attack_value(self, tag):
        try:
            return int(tag.find_next("td", {"class" : "quantity"}).next_sibling.next_sibling.string.encode("utf-8"))
        except:
            return None

    def obtain_defense_value(self, tag):
        try:
            return int(tag.find_next("td", {"class" : "quantity"}).next_sibling.next_sibling.next_sibling.find_next("span").string.encode("utf-8"))
        except:
            return 0

    def obtain_hp_value(self, tag):
        try:
            return int(tag.find_next("td", {"class" : "quantity"}).next_sibling.next_sibling.next_sibling.next_sibling.find_next("span").string.encode("utf-8"))
        except:
            return None

    def obtain_move_info(self, tag, result):
        move_tag = tag.find("td", {"class" : "mmemodetail"})

        try:
            move_name = tag.find_next("a").text.encode("utf-8") \
                        if move_tag == None else move_tag.find("span", {"class" : "skillexpand"}).find_next("a").text.encode("utf-8")
        except Exception as e:
            return tuple([])

        try:
            move_attack = int(tag.find("a").next_sibling.next_sibling.text.encode("utf-8")) \
                          if move_tag == None else int(move_tag.find("span").find("a").next_sibling.next_sibling.text.encode("utf-8"))
        except Exception as e:
            move_attack = None

        try:
            move_info = tag.find_all("div", id=re.compile("\d-info"))[0].text.encode("utf-8") \
                        if move_tag == None else move_tag.find("span", {"class" : "skillexpand"}).find_all("div", id=re.compile("\d-info"))[0].text.encode("utf-8")

            move_des_tag = tag.find_all("div", id=re.compile("\d-info"))[0] \
                           if move_tag == None else move_tag.find("span", {"class" : "skillexpand"}).find_all("div", id=re.compile("\d-info"))[0]

            move_id = int(move_des_tag.find("a", href=re.compile("^enemyskill.asp"))["href"].split("s=")[1])

            if len(move_des_tag.contents) > 1:
                move_description = move_des_tag.find("a", href=re.compile("^enemyskill.asp")).previous_sibling.string.encode("utf-8")
                move_condition = move_info.split(move_description)[0]

                try:
                    move_description = move_description.split("Pre-emptive Strike. ")[1]
                except:
                    move_description = move_description

            else:
                move_condition = None
                move_description = None

        except Exception as e:
            return tuple([])


        skills_left = tag.find_all("span", {"class" : "skillexpand"}) \
                      if move_tag == None else move_tag.find_all("span", {"class" : "skillexpand"})
        num_skills_left = len(tag.find_all("span", {"class" : "skillexpand"})) \
                          if move_tag == None else len(move_tag.find_all("span", {"class" : "skillexpand"})) - 1
        if num_skills_left > 0:
            if move_tag != None:
                skills_left.pop(0)

            result.append(tuple([move_id, move_name, move_attack, move_condition, move_description]))
            return self.obtain_move_info(skills_left[0], result)
        else:
            result.append(tuple([move_id, move_name, move_attack, move_condition, move_description]))
            return tuple(result)

    def parse_dungeon(self, response):
        d_id = int(response.url.split("m=")[1])

        soup = BeautifulSoup(response.body, "lxml")

        d_name = soup.find("h1").text.encode("utf-8")

        # Monster_ID
        d_random_encounter_monsters = {(self.obtain_encounter_monster(monster_tag), \
                                        self.obtain_encounter_type(monster_tag), \
                                        self.obtain_turn_number(monster_tag), \
                                        self.obtain_attack_value(monster_tag), \
                                        self.obtain_defense_value(monster_tag), \
                                        self.obtain_hp_value(monster_tag), \
                                        self.obtain_move_info(monster_tag, [])) \
                                        for monster_tag in soup.find("div", {"id" : "dungeon-info"}).find_next("table", id="tabledrop").find_all("tr") \
                                        if monster_tag.find("td", text="\xc2\xa0") != None}
        
        # Floor #, Monster_ID, Quantity, Type, Turn, Attack, Defense, HP
        d_major_encounter_monsters = {( self.obtain_floor_number(monster_tag), 
                                        self.obtain_encounter_monster(monster_tag), \
                                        self.obtain_encounter_quantity(monster_tag), \
                                        self.obtain_encounter_type(monster_tag), \
                                        self.obtain_turn_number(monster_tag), \
                                        self.obtain_attack_value(monster_tag), \
                                        self.obtain_defense_value(monster_tag), \
                                        self.obtain_hp_value(monster_tag), \
                                        self.obtain_move_info(monster_tag, [])) \
                                        for monster_tag in soup.find("div", {"id" : "dungeon-info"}).find_next("table", id="tabledrop").find_all("tr") \
                                        if represents_int(monster_tag.find_next("td").string)}

        dungeon = Dungeon(id=d_id, name=d_name)
        db.session.add(dungeon)
        db.session.commit()

        for monster_id, monster_type, turn, atk, defn, hp, moves_info in d_random_encounter_monsters:
            enemy_monster = EnemyMonster(hp=hp, atk=atk, defn=defn, turn=turn)
            enemy_monster.common_monster = CommonMonster.query.filter_by(id=monster_id).first()
            enemy_monster.random_encounter_in_dungeon = dungeon

            db.session.add(enemy_monster)
            db.session.commit()

            for move_id, move_name, move_attack, move_condition, move_description in moves_info:
                if EnemySkill.query.filter_by(id=move_id).first() == None:
                    db.session.add(EnemySkill(id=move_id, name=move_name, effect=move_description))
                    db.session.commit()

                enemy_skill = EnemySkill.query.filter_by(id=move_id).first()
                enemy_move = EnemyMove(atk_condition=move_condition, atk=move_attack)
                enemy_move.enemy_skill = enemy_skill
                enemy_move.enemy_monster = enemy_monster

                db.session.add(enemy_move)
                db.session.commit()
