from . import db

class File(db.Model):
    __tablename__ = 'files'

    fileid = db.Column(db.Integer, primary_key=True, server_default=db.text("nextval('files_fileid_seq'::regclass)"))
    file_path = db.Column(db.Text)


class Lemmata(db.Model):
    __tablename__ = 'lemmata'

    lemmaid = db.Column(db.Integer, primary_key=True, server_default=db.text("nextval('lemmata_lemmaid_seq'::regclass)"))
    lemma = db.Column(db.Text, index=True)
    lang = db.Column(db.Text)
    tokens = db.relationship('Token', backref='lemmata', lazy=True)


class LemmataPo(db.Model):
    __tablename__ = 'lemmata_pos'

    lemmaposid = db.Column(db.Integer, primary_key=True, server_default=db.text("nextval('lemmata_pos_lemmaposid_seq'::regclass)"))
    lemmaid = db.Column(db.Integer)
    pos = db.Column(db.Text)


class Raw(db.Model):
    __tablename__ = 'raw'

    rawid = db.Column(db.Integer, primary_key=True, server_default=db.text("nextval('raw_rawid_seq'::regclass)"))
    chapter = db.Column(db.Text)
    line = db.Column(db.Text)
    document = db.Column(db.Text)
    poslemma = db.Column(db.Text)
    inflectionclass = db.Column(db.Text)
    edition = db.Column(db.Text)
    lemma = db.Column(db.Text)
    inflectionclasslemma = db.Column(db.Text)
    pos = db.Column(db.Text)
    translation = db.Column(db.Text)
    text = db.Column(db.Text)
    verse = db.Column(db.Text)
    page = db.Column(db.Text)
    lang = db.Column(db.Text)
    inflection = db.Column(db.Text)
    subchapter = db.Column(db.Text)
    file_path = db.Column(db.Text)


class Text(db.Model):
    __tablename__ = 'texts'

    textid = db.Column(db.Integer, primary_key=True, server_default=db.text("nextval('texts_textid_seq'::regclass)"))
    name = db.Column(db.String(100))


class Token(db.Model):
    __tablename__ = 'tokens'

    tokenid = db.Column(db.Integer, primary_key=True, server_default=db.text("nextval('tokens_tokenid_seq'::regclass)"))
    text = db.Column(db.Text, index=True)
    edition = db.Column(db.Text)
    lemmaid = db.Column(db.Integer, db.ForeignKey('lemmata.lemmaid'))
    pos = db.Column(db.Text)
    inflection = db.Column(db.Text)
    lang = db.Column(db.Text)
    translation = db.Column(db.Text, index=True)
    fileid = db.Column(db.Integer, db.ForeignKey('file.fileid'))
