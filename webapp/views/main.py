from .. import g
from .. import db
from flask import Blueprint, Response, render_template, request, abort, session, send_file, redirect, url_for, flash
from ..forms import SearchForm, ResultsForm
from ..models import Token, Lemmata
from difflib import Differ
from sqlalchemy.sql import text, func
import base64


main = Blueprint('main', __name__)

@main.route('/', methods=['GET'])
def index():
    searchForm = SearchForm()
    return render_template('index.html', searchForm=searchForm)

@main.route('/search', methods=['GET', 'POST'])
def search():
    data = []
    formObject = []
    urlList = []

    searchForm = SearchForm()

    if searchForm.validate_on_submit():
        if request.method == "POST":
            data = request.form.to_dict()

            if data["searchString"].startswith("@"):
                data["searchString"] = data["searchString"][1:]
                sql = """SELECT text as lower, count(*) as count, l.lemma, t.lang,array_to_string(array_agg(distinct(t.pos)), ' ') as pos,array_to_string(array_agg(distinct(t.inflection)), ' ') as inflection, array_to_string(array_agg(distinct(t.translation)), ' ') as translation
                      FROM tokens t
                      JOIN lemmata l ON l.lemmaid = t.lemmaid
                      WHERE l.lemma = :expr
                      GROUP BY l.lemma, t.text, t.lang
                      ORDER BY count DESC;"""

            elif data["searchString"].startswith("="):
                data["searchString"] = data["searchString"][1:]
                data["searchString"] = "%" + data["searchString"] + "%"
                sql = """SELECT text as lower, count(*) as count, l.lemma, t.lang,array_to_string(array_agg(distinct(t.pos)), ' ') as pos,array_to_string(array_agg(distinct(t.inflection)), ' ') as inflection, array_to_string(array_agg(distinct(t.translation)), ' ') as translation
                      FROM tokens t
                      JOIN lemmata l ON l.lemmaid = t.lemmaid
                      WHERE t.translation LIKE :expr
                      GROUP BY l.lemma, t.text, t.lang
                      ORDER BY count DESC;"""

            elif data["searchString"].startswith("\""):
                data["searchString"] = data["searchString"][1:-1]
                sql = """SELECT text as lower, count(*) as count, l.lemma, t.lang,array_to_string(array_agg(distinct(t.pos)), ' ') as pos,array_to_string(array_agg(distinct(t.inflection)), ' ') as inflection, array_to_string(array_agg(distinct(t.translation)), ' ') as translation
                      FROM tokens t
                      JOIN lemmata l ON l.lemmaid = t.lemmaid
                      WHERE text = :expr
                      GROUP BY text, l.lemma, t.lang
                      ORDER BY count DESC;"""

            else:
                sql = """SELECT lower(text), count(*) as count, similarity(lower(text), :expr) AS sml, l.lemma, t.lang,array_to_string(array_agg(distinct(t.pos)), ' ') as pos,array_to_string(array_agg(distinct(t.inflection)), ' ') as inflection,  array_to_string(array_agg(distinct(t.translation)), ' ') as translation
                      FROM tokens t
                      JOIN lemmata l ON l.lemmaid = t.lemmaid
                      WHERE text % :expr
                      GROUP BY lower(text), l.lemma, t.lang
                      ORDER BY sml DESC, lower(text);"""

            if data:
                tokens = db.engine.execute(text(sql), expr=data["searchString"])

                #tokens = Token.query.filter(Token.text==data["searchString"]).all()

                for token in tokens:
                    searchString = 'text="' + token.lower + '"'
                    url = """ https://korpling.german.hu-berlin.de/annis3/ddd#_q=%s&_c=RERELUFELUJlbmVkaWt0aW5lcl9SZWdlbF8xLjAsRERELUFELUJlbmVkaWt0aW5lcl9SZWdlbF9MYXRlaW5fMS4wLERERC1BRC1HZW5lc2lzXzEuMCxEREQtQUQtSGVsaWFuZF8xLjAsRERELUFELUlzaWRvcl8xLjAsRERELUFELUlzaWRvcl9MYXRlaW5fMS4wLERERC1BRC1LbGVpbmVyZV9BbHRob2NoZGV1dHNjaGVfRGVua23DpGxlcl8xLjAsRERELUFELUtsZWluZXJlX0FsdHPDpGNoc2lzY2hlX0Rlbmttw6RsZXJfMS4wLERERC1BRC1Nb25zZWVfMS4wLERERC1BRC1NdXJiYWNoZXJfSHltbmVuXzEuMCxEREQtQUQtTXVyYmFjaGVyX0h5bW5lbl9MYXRlaW5fMS4wLERERC1BRC1PdGZyaWRfMS4wLERERC1BRC1QaHlzaW9sb2d1c18xLjAsRERELUFELVRhdGlhbl8xLjAsRERELUFELVRhdGlhbl9MYXRlaW5fMS4wLERERC1BRC1aLU5vdGtlci1NYXJ0aWFudXNfQ2FwZWxsYV8xLjAsRERELUFELVotTm90a2VyLVBzYWxtZW5fMS4wLERERC1BRC1aLU5vdGtlcl9Cb2V0aGl1cy1DYXRlZ29yaWFlXzEuMCxEREQtQUQtWi1Ob3RrZXJfQm9ldGhpdXMtRGVfQ29uc29sYXRpb25lX3BoaWxvc29waGlhZV8xLjAsRERELUFELVotTm90a2VyX0JvZXRoaXVzLURlX0ludGVycHJldGF0aW9uZV8xLjAsRERELUFELVotTm90a2VyX0tsZWluZXJlLUFyc19SaGV0b3JpY2FfMS4wLERERC1BRC1aLU5vdGtlcl9LbGVpbmVyZS1EZV9NdXNpY2FfMS4wLERERC1BRC1aLU5vdGtlcl9LbGVpbmVyZS1EZV9QYXJ0aWJ1c19sb2dpY2FlXzEuMCxEREQtQUQtWi1Ob3RrZXJfS2xlaW5lcmUtU3lsbG9naXNtdXNfMS4w&cl=5&cr=5&s=0&l=10&_seg=ZWRpdGlvbg """ % (base64.b64encode(searchString.encode()).decode())
                    urlList.append(url)
                    form = ResultsForm()
                    form.text.data = token.lower
                    form.count.data = token.count
                    form.lemma.data = token.lemma
                    form.lang.data = token.lang
                    form.inflection.data = token.inflection
                    form.pos.data = token.pos
                    form.translation.data = token.translation
                    formObject.append(form)

                    # set cut-off points for similarity search
                    #if 'sml' in token:
                        # if exact match, stop after first result (exact)
                     #   if token.sml == 1:
                      #      break
                        # if not exact, set treshold to 0.5
                       # elif token.sml < 0.5:
#                            break

    return render_template('search.html', searchForm=searchForm, formObject=formObject, urlList=urlList)


@main.route('/impressum', methods=['GET'])
def showimpressum():
  return render_template('contact.html')
