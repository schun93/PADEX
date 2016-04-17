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


for active_skill in ActiveSkill.query.all():
    print(active_skill)

print(Monster.query.filter_by(id=115).first() != None)
print(Monster.query.filter_by(id=115).first() != None)