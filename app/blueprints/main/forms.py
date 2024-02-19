from flask_wtf import FlaskForm
from wtforms import EmailField, PasswordField, SubmitField, StringField
from wtforms.validators import DataRequired

class PokemonForm(FlaskForm):
    name = StringField('Pokemon Name: ')
    baseHp = StringField('Base HP: ')
    baseAttack = StringField('Base Attack')
    baseDefense = StringField('Base Defense: ')
    spriteImage = StringField('Image URL: ')
    capture_btn = SubmitField('Capture')