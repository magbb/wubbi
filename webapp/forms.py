from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, BooleanField, SelectField,SubmitField
from wtforms.validators import InputRequired
from .models import Token, Lemmata
from . import db

class SearchForm(FlaskForm):
    searchString = StringField('Search', [InputRequired()])
    submit = SubmitField('Go!')

class ResultsForm(FlaskForm):
    text = StringField('Token')
    count = StringField('Count')
    lemma = StringField('Lemma')
    lang = StringField("Language")
    pos = StringField("Part of Speech")
    inflection = StringField('Inflection')
    translation = StringField('Translation')
