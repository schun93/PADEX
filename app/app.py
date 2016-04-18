import json

from functools import wraps

# Import Models
from app.model.active_skill import ActiveSkill
from app.model.awoken_skill import AwokenSkill
from app.model.leader_skill import LeaderSkill
from app.model.monster_series import MonsterSeries
from app.model.type import Type
from app.model.element import Element
from app.model.monster import Evolution, Monster

# Import flask and template operators
from flask import Flask

# Import SQLAlchemy
from flask.ext.sqlalchemy import SQLAlchemy

# Define the WSGI application object
app = Flask(__name__)

# Configurations
app.config.from_object("config")

# Define the database object which is imported
# by modules and controllers
db = SQLAlchemy(app)


def handle_none_query(func):
    @wraps(func)
    def func_wrapper(**args):
        try:
            return json.dumps(func(**args))
        except Exception as e:
            print("None Query: " + str(e))
            return json.dumps("{}")
    return func_wrapper

# Thin API Routes

@app.route("/api/v1/active_skill/thin/<active_skill_id>")
@handle_none_query
def api_thin_active_skill(active_skill_id):
    return ActiveSkill.query.filter_by(id=active_skill_id).first().dictify()

@app.route("/api/v1/awoken_skill/thin/<awoken_skill_id>")
@handle_none_query
def api_thin_awoken_skill(awoken_skill_id):
    return AwokenSkill.query.filter_by(id=awoken_skill_id).first().dictify()

@app.route("/api/v1/leader_skill/thin/<leader_skill_id>")
@handle_none_query
def api_thin_leader_skill(leader_skill_id):
    return LeaderSkill.query.filter_by(id=leader_skill_id).first().dictify()

@app.route("/api/v1/monster_series/thin/<monster_series_id>")
@handle_none_query
def api_thin_monster_series(monster_series_id):
    return MonsterSeries.query.filter_by(id=monster_series_id).first().dictify()

@app.route("/api/v1/type/thin/<type_id>")
@handle_none_query
def api_thin_type(type_id):
    return Type.query.filter_by(id=type_id).first().dictify()

@app.route("/api/v1/element/thin/<element_id>")
@handle_none_query
def api_thin_element(element_id):
    return Element.query.filter_by(id=element_id).first().dictify()

# API Routes

@app.route("/api/v1/active_skill/<active_skill_id>")
@handle_none_query
def api_active_skill(active_skill_id):
    return ActiveSkill.query.filter_by(id=active_skill_id).first().dictify(thinify=False)

@app.route("/api/v1/awoken_skill/<awoken_skill_id>")
@handle_none_query
def api_awoken_skill(awoken_skill_id):
    return AwokenSkill.query.filter_by(id=awoken_skill_id).first().dictify(thinify=False)

@app.route("/api/v1/leader_skill/<leader_skill_id>")
@handle_none_query
def api_leader_skill(leader_skill_id):
    return LeaderSkill.query.filter_by(id=leader_skill_id).first().dictify(thinify=False)

@app.route("/api/v1/monster_series/<monster_series_id>")
@handle_none_query
def api_monster_series(monster_series_id):
    return MonsterSeries.query.filter_by(id=monster_series_id).first().dictify(thinify=False)

@app.route("/api/v1/type/<type_id>")
@handle_none_query
def api_type(type_id):
    return Type.query.filter_by(id=type_id).first().dictify(thinify=False)

@app.route("/api/v1/element/<element_id>")
@handle_none_query
def api_element(element_id):
    return Element.query.filter_by(id=element_id).first().dictify(thinify=False)

@app.route("/api/v1/evolution/<evolution_id>")
@handle_none_query
def api_evolution(evolution_id):
    return Evolution.query.filter_by(id=evolution_id).first().dictify()

@app.route("/api/v1/monster/<monster_id>")
@handle_none_query
def api_monster(monster_id):
    return Monster.query.filter_by(id=monster_id).first().dictify(thinify=False)

# Sample HTTP error handling
@app.errorhandler(404)
def not_found(error):
    return "404 Not Found"

