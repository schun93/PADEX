from flask import Flask
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "mysql+pymysql://root:crayons@localhost/testdb?charset=utf8"
db = SQLAlchemy(app)
