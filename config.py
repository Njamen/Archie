import os
from flask_moment import Moment
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import Column, String, Integer
import json
from flask import Flask

SECRET_KEY = os.urandom(32)
# Grabs the folder where the script runs.
# basedir = os.path.abspath(os.path.dirname(__file__))

SQLALCHEMY_TRACK_MODIFICATIONS = False

# Enable debug mode.
DEBUG = True

database_filename = "database.db"
project_dir = os.path.dirname(os.path.abspath(__file__))
# database_path = "sqlite:///{}".format(os.path.join(project_dir, database_filename))
# database_path = 'postgresql://admin:pass_admin@localhost:5432/fyyur_db'
database_path = 'mysql+pymysql://yanord:yanord@localhost:3306/cl_dbname'


app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = database_path
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
db = SQLAlchemy(app)

class Drink(db.Model):
    # Autoincrementing, unique primary key
    id = Column(Integer().with_variant(Integer, "sqlite"), primary_key=True)
    # String Title
    title = Column(String(80), unique=True)
    # the ingredients blob - this stores a lazy json blob
    # the required datatype is [{'color': string, 'name':string, 'parts':number}]
    recipe = Column(String(180), nullable=False)

    '''
    short()
        short form representation of the Drink model
    '''

    def short(self):
        print("in short")
        print(json.loads(self.recipe))
        short_recipe = [{'color': r['color'], 'parts': r['parts']} for r in json.loads(self.recipe)]
        return {
            'id': self.id,
            'title': self.title,
            'recipe': short_recipe
        }

    def long(self):
        print("JSON")
        print(self.recipe)

        return {
            'id': self.id,
            'title': self.title,
            'recipe': json.loads(self.recipe)
        }

    def insert(self):
        db.session.add(self)
        db.session.commit()


    def delete(self):
        db.session.delete(self)
        db.session.commit()

    def update(self):
        db.session.commit()

    def __repr__(self):
        return json.dumps(self.short())


db.app = app
db.init_app(app)


db.drop_all()
db.create_all()
# drink = Drink(
#     title='water',
#     recipe='[{"name": "water", "color": "blue", "parts": 1}]'
# )
# drink.insert()


# moment = Moment(app)
# app.config.from_object('config')
# db = SQLAlchemy(app)
# migrate = Migrate(app, db)
# # app.config['SQLALCHEMY_DATABASE_URI'] = SQLALCHEMY_DATABASE_URI
# app.config['SQLALCHEMY_DATABASE_URI'] = database_path

# db.init_app(app)
