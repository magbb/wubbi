from flask import Flask, Response, request, session, g, redirect, url_for, \
     abort, render_template, flash, make_response
from flask_bootstrap import Bootstrap
from flask_sqlalchemy import SQLAlchemy
import webapp.config as c

app = Flask(__name__)
app.config.from_object(__name__)
app.config["SECRET_KEY"] = "SETT INN SUPERSIKKER NØKKEL HER"

# whitespace control for Jinja2 templates
app.jinja_env.trim_blocks = True
app.jinja_env.lstrip_blocks = True
app.config["WTF_CSRF_ENABLED"] = False
app.config["WTF_CSRF_CHECK_DEFAULT"] = False

# db config
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_DATABASE_URI'] = c.dbConnectString

bootstrap = Bootstrap(app)
db = SQLAlchemy(app)

from webapp.models import Token, Lemmata
from webapp.forms import SearchForm, ResultsForm

#bootstrap.init_app(app)
#db.init_app(app)

# register Blueprints
# main blueprint

from .views.main import main
app.register_blueprint(main)
