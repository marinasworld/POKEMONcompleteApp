from . import main
from flask import request, render_template, redirect, url_for, flash
import requests
from app.models import Pokemon, CapturedPokemon
from flask_login import current_user

@main.route('/')
def home():
    return render_template('home.html')
    
@main.route("/pokemon", methods=['GET', 'POST'])
def pokemon():
    if request.method == 'POST':
        pokemonName = request.form.get('pokemonNameInput')
        pokemonData = GetPokemonData(pokemonName)
        return render_template('pokemon.html', drivers=pokemonData)
    else:
        return render_template('pokemon.html')

def GetPokemonData(pokemonName):
    if pokemonName == '':
        return

    pokemonUrl = "https://pokeapi.co/api/v2/pokemon/" + pokemonName
    pokemon = requests.get(pokemonUrl)

    if pokemon.ok:
        pokemonJson = pokemon.json()

        hp = 0
        attack = 0
        defense = 0

        pokemonStats = pokemonJson["stats"]
        for stat in pokemonStats:
            if stat["stat"]["name"] == "hp":
                hp = stat["base_stat"]
            if stat["stat"]["name"] == "attack":
                attack = stat["base_stat"]
            if stat["stat"]["name"] == "defense":
                defense = stat["base_stat"]

        pokemonDictionary = {
            "id": pokemonJson["id"],
            "name": pokemonJson["name"],
            "ability": pokemonJson["abilities"][0]["ability"]["name"],
            "hp": hp,
            "attack": attack,
            "defense": defense,
            "pokemonImage": pokemonJson["sprites"]["back_default"]
        }

        return pokemonDictionary

@main.route('/capture/<pokemonName>', methods=['GET', 'POST'])
def capturePokemon(pokemonName): #pokemonName can also be the pokemonId
    if not pokemonName:
        return redirect(url_for('main.pokemon'))

    # If pokemon doesn't exist in the Pokemon table, add to it from API
    queried_pokemon = Pokemon.query.filter(Pokemon.name == pokemonName).first()
    if not queried_pokemon:
        api_Pokemon = GetPokemonData(pokemonName)
        new_Pokemon = Pokemon(pokemonName, api_Pokemon["hp"], api_Pokemon["attack"], api_Pokemon["defense"], api_Pokemon["pokemonImage"])
        new_Pokemon.save()
        testPokemon = Pokemon.query.filter(Pokemon.name == pokemonName).first()
        addPokemonToTeam(testPokemon.id)
    else:
        # Add pokemon to logged-in user's team
        addPokemonToTeam(queried_pokemon.id)

    # Return to pokemon page
    return redirect(url_for('main.pokemon'))

def addPokemonToTeam(pokemonId):
        # Check if the user has 6 pokemon
        pokemonForUser = CapturedPokemon.query.filter(CapturedPokemon.username == current_user.username)
        if pokemonForUser.count() > 5:
            flash('The user already has 6 pokemon.  Remove 1 to add a new pokemon')
            return redirect(url_for('main.pokemon'))

        # Check if pokemon is on the user's team already
        teamPokemon = CapturedPokemon.query.filter(CapturedPokemon.username == current_user.username and CapturedPokemon.id == pokemonId).first()
        if teamPokemon:
            flash('The user already has this pokemon on their team')
            return redirect(url_for('main.pokemon'))

        # Add pokemon to logged-in user's team
        new_CapturedPokemon = CapturedPokemon(current_user.username, pokemonId)
        new_CapturedPokemon.save()