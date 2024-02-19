from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin
from werkzeug.security import generate_password_hash

db = SQLAlchemy()

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String, unique=True, nullable=False)
    email = db.Column(db.String, unique=True, nullable=False)
    password = db.Column(db.String, nullable=False)

    def __init__(self, username, email, password):
        self.username = username
        self.email = email
        self.password = generate_password_hash(password)

    def save(self):
        db.session.add(self)
        db.session.commit()

class Pokemon(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, unique=True)
    baseHp = db.Column(db.Integer, nullable=False)
    baseAttack = db.Column(db.Integer, nullable=False)
    baseDefense = db.Column(db.Integer, nullable=False)
    spriteImage = db.Column(db.String, nullable=False)

    def __init__(self, name, baseHp, baseAttack, baseDefense, spriteImage=''):
        self.name = name
        self.baseHp = baseHp
        self.baseAttack = baseAttack
        self.baseDefense = baseDefense
        self.spriteImage = spriteImage

    def save(self):
        db.session.add(self)
        db.session.commit()

class CapturedPokemon(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String, db.ForeignKey('user.username'), nullable=False)
    pokemonId = db.Column(db.Integer, db.ForeignKey('pokemon.id'), nullable=False)

    def __init__(self, username, pokemonId):
        self.username = username
        self.pokemonId = pokemonId

    def save(self):
        db.session.add(self)
        db.session.commit()