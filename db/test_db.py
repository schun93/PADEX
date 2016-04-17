import sys

sys.path.append("../.")

from flask import Flask
from flask_sqlalchemy import SQLAlchemy

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from app.model.base import db
from app.model.dungeon import EnemySkill, EnemyMove, EnemyMonster, Dungeon
from app.model.monster import CommonMonster, Monster
from app.model.type import Type
from app.model.element import Element
from app.model.active_skill import ActiveSkill
from app.model.leader_skill import LeaderSkill
from app.model.awoken_skill import AwokenSkill
from app.model.monster_series import MonsterSeries

print("Connection created.")

# print(len(Dungeon.query.all()))
db.drop_all()

print("All tables dropped.\n")

db.create_all()
db.session.commit()

print("Adding dungeon.")

creator_goddess_legend = Dungeon(id=683, name="Creator Goddess - Legend")

dungeons = {
            683: creator_goddess_legend
            }

db.session.add_all(dungeon for dungeon in dungeons.values())
db.session.commit()

print("Added dungeon.")

print("Adding type.")

god = Type(id=6, name="God")
healer = Type(id=4, name="Healer")
attacker = Type(id=5, name="Attacker")

types = {
         6: god,
         4: healer,
         5: attacker
         }

db.session.add_all(type for type in types.values())
db.session.commit()

print("Added type.")

print("Adding element.")

wood = Element(id=3, name="Wood")
light = Element(id=4, name="Light")

elements = {
         3: wood,
         4: light    
         }

db.session.add_all(element for element in elements.values())
db.session.commit()

print("Added element.")

print("Adding active_skill.")

shower_of_healing = ActiveSkill(id=32, \
                                name="Shower Of Healing", \
                                effect="Full HP recovery. Full bind recovery.", \
                                original_effect="HP fully recovers, and all bind statuses are recovered.", \
                                max_cd=20, \
                                min_cd=10, \
                                max_lvl=11)

active_skills = {
                 32: shower_of_healing
                 }

db.session.add_all(active_skill for active_skill in active_skills.values())
db.session.commit()

print("Added active_skill.")


print("Adding leader_skill.")

godly_wall_of_holy_forest = LeaderSkill(id=383, \
                                        name="Godly Wall Of Holy Forest", \
                                        effect="God type cards ATK x1.5. 55% Wood & Light damage reduction.", \
                                        original_effect="Greatly reduces damage from Wood & Light Att. enemies, plus 1.5x ATK for God Type.")

leader_skills = {
                 383: godly_wall_of_holy_forest    
                 }

db.session.add_all(leader_skill for leader_skill in leader_skills.values())
db.session.commit()

print("Added leader_skill.")

print("Adding awoken_skill.")

recover_bind = AwokenSkill(id=22, \
                           name="Recover Bind", \
                           description="Eliminating 1 row of hearts will reduce binds by 3 turns.", \
                           img="/api/awoken_skill/img/22.png")

auto_recover = AwokenSkill(id=11, \
                           name="Auto-Recover",
                           description="Heal for 500 HP when you clear any drops.", \
                           img="/api/awoken_skill/img/11.png")

awoken_skills = {
                 22: recover_bind,
                 11: auto_recover
                 }

db.session.add_all(awoken_skill for awoken_skill in awoken_skills.values())
db.session.commit()

print("Added awoken_skill.")

print("Adding monster_series.")

greco_roman_series = MonsterSeries(id=13, \
                             name="Greco-Roman")

monster_series = {
                 13: greco_roman_series
                 }

# Yes I know this is spelled wrong
db.session.add_all(monster_serie for monster_serie in monster_series.values())
db.session.commit()

print("Added monster_series.")

print("Adding monster.")

ceres = Monster(id=392, name="Fertility Deity, Holy Ceres", rarity=7, team_cost=30, sells_for_monster_points=5000, min_lvl=1, max_lvl=99, \
                 min_hp=1110, max_hp=2574, min_atk=675, max_atk=1161, min_rcv=675, max_rcv=741, min_sell_value=585, max_sell_value=57915, \
                 min_exp_feed=1388, max_exp_feed=137363, exp_needed=4000000000)
ceres.monster_series = greco_roman_series
ceres.active_skill = shower_of_healing
ceres.leader_skill = godly_wall_of_holy_forest
ceres.awoken_skills = list(awoken_skills.values())

print("Added monster.")

print("Adding common_monster.")

common_ceres = CommonMonster(id=392, name="Fertility Deity, Holy Ceres", img="/api/monster/img/392.png", thmb="/api/monster/thmb/392.png")
common_ceres.monster = ceres
common_ceres.primary_type = god
common_ceres.secondary_type = healer
common_ceres.primary_element = wood
common_ceres.secondary_element = light

common_monsters = {
                    392: common_ceres
                   }

db.session.add_all(common_monster for common_monster in common_monsters.values())
db.session.commit()

print("Added common_monster.")

print("Adding enemy_monster.")

enemy_ceres = EnemyMonster(id=1, hp=2259946, atk=21994, defn=0, turn=2, floor=5, quantity=None)
enemy_ceres.common_monster = common_ceres
enemy_ceres.major_encounter_in_dungeon = creator_goddess_legend

enemy_monsters = {
                 1: enemy_ceres
                 }

db.session.add_all(enemy_monster for enemy_monster in enemy_monsters.values())
db.session.commit()

print("Added enemy_monster.\n")

print("Adding enemy_skills.")

flower_world_s = EnemySkill(id=795, name="Flower World", effect=" Deal 150% damage and converts all Heart orbs into Wood orbs")
ground_revenge_s = EnemySkill(id=803, name="Ground Revenge", effect="Deal 120% damage ( 3 hits, 40% per hit )")
earths_core_s = EnemySkill(id=799, name="Earth's Core", effect="Absorbs 100% Fire damage for 5 turns")

enemy_skills = {
                795: flower_world_s, 
                803: ground_revenge_s,
                799: earths_core_s
                }

db.session.add_all(enemy_skill for enemy_skill in enemy_skills.values())
db.session.commit()

print("Added enemy_skills\n")

print("Adding enemy_move.")

flower_world_m = EnemyMove(id=1, atk=32991, atk_condition="100% Chance. Will use every other turn when above 50% HP")
flower_world_m.enemy_skill = flower_world_s
flower_world_m.enemy_monster = enemy_ceres

enemy_moves = {
               1: flower_world_m
               }

db.session.add_all(enemy_move for enemy_move in enemy_moves.values())
db.session.commit()

print("Added enemy_move.\n")

dungeon_table = Dungeon.query.all()

for dungeon in dungeon_table:
    print(dungeon)

db.session.close()
