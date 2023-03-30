"""
This module takes care of starting the API Server, Loading the DB and Adding the endpoints
"""
import os
from flask import Flask, request, jsonify, url_for, json
from flask_migrate import Migrate
from flask_swagger import swagger
from flask_cors import CORS
from utils import APIException, generate_sitemap
from admin import setup_admin
from models import db, User, Character, Planet, Favorites
#from models import Person

app = Flask(__name__)
app.url_map.strict_slashes = False

db_url = os.getenv("DATABASE_URL")
if db_url is not None:
    app.config['SQLALCHEMY_DATABASE_URI'] = db_url.replace("postgres://", "postgresql://")
else:
    app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:////tmp/test.db"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

MIGRATE = Migrate(app, db)
db.init_app(app)
CORS(app)
setup_admin(app)

# Handle/serialize errors like a JSON object
@app.errorhandler(APIException)
def handle_invalid_usage(error):
    return jsonify(error.to_dict()), error.status_code

# generate sitemap with all your endpoints
@app.route('/')
def sitemap():
    return generate_sitemap(app)

@app.route("/user", methods=['POST', 'GET'])
def handle_user():
    if request.method == 'POST':
        data = request.json
        if data.get("name") is None or data.get("email") is None or data.get("password") is None:
            return jsonify({
                "error": "Campos inválidos, complete correctamente los datos de user"
            }), 400
        ## Instantiate new user
        new_user = User()
        new_user.name = data['name']
        new_user.email = data['email']
        new_user.password = data['password']
        ## Add / Commit to DB
        db.session.add(new_user)
        db.session.commit()
        return jsonify(data), 201
    if request.method == 'GET':
        users_list = User.query.all()
        users = []
        for item in users_list:
            users.append(item.serialize())
        return jsonify(users), 200  

@app.route("/user/<int:user_id>", methods=['GET', 'DELETE'])
def handle_user_id(user_id):
    if request.method == 'GET':
        user_filter = User.query.filter_by(id = user_id)
        get_user = []
        for item in user_filter:
            get_user.append(item.serialize())
        if get_user != []:
            return jsonify(get_user), 200
        else:
            return jsonify({
                    "Error": "User not found"
                }), 400
    if request.method == 'DELETE':
        user_delete = User.query.filter_by(id = user_id).first()
        if user_delete is None:
            return jsonify({
                    "Error": "User not found"
                }), 400
        else:        
            db.session.delete(user_delete)
            db.session.commit()
        return jsonify({
                    "Message": "User deleted"
                }), 200

@app.route("/character", methods=['POST', 'GET'])
def handle_character():
    if request.method == 'POST':
        data = request.json
        if data.get("name") is None or data.get("birth_year") is None or data.get("gender") is None or data.get("eye_color") is None:
            return jsonify({
                "error": "Campos inválidos, complete correctamente los datos de character"
            }), 400
        ## Instantiate new character
        new_character = Character()
        new_character.name = data['name']
        new_character.birth_year = data['birth_year']
        new_character.gender = data['gender']
        new_character.eye_color = data['eye_color']
        ## Add / Commit to DB
        db.session.add(new_character)
        db.session.commit()
        return jsonify(data), 201
    if request.method == 'GET':
        characters_list = Character.query.all()
        characters = []
        for item in characters_list:
            characters.append(item.serialize()) 
        return jsonify(characters), 200

@app.route("/character/<int:character_id>", methods=['GET', 'DELETE'])
def handle_character_id(character_id):
    if request.method == 'GET':
        character_filter = Character.query.filter_by(id = character_id)
        get_character = []
        for item in character_filter:
            get_character.append(item.serialize())
        if get_character != []:
            return jsonify(get_character), 200
        else:
            return jsonify({
                    "Error": "Character not found"
                }), 400
    if request.method == 'DELETE':
        character_delete = Character.query.filter_by(id = character_id).first()
        if character_delete is None:
            return jsonify({
                    "Error": "Character not found"
                }), 400
        else:        
            db.session.delete(character_delete)
            db.session.commit()
        return jsonify({
                    "Message": "Character deleted"
                }), 200

@app.route("/planet", methods=['POST', 'GET'])
def handle_planet():
    if request.method == 'POST':
        data = request.json
        if data.get("name") is None or data.get("diameter") is None or data.get("climate") is None or data.get("terrain") is None:
            return jsonify({
                "error": "Campos inválidos, complete correctamente los datos de planet"
            }), 400
        ## Instantiate new planet
        new_planet = Planet()
        new_planet.name = data['name']
        new_planet.diameter = data['diameter']
        new_planet.climate = data['climate']
        new_planet.terrain = data['terrain']
        ## Add / Commit to DB
        db.session.add(new_planet)
        db.session.commit()
        return jsonify(data), 201
    if request.method == 'GET':
        planets_list = Planet.query.all()
        planets = []
        for item in planets_list:
            planets.append(item.serialize()) 
        return jsonify(planets), 200

@app.route("/planet/<int:planet_id>", methods=['GET', 'DELETE'])
def handle_planet_id(planet_id):
    if request.method == 'GET':
        planet_filter = Planet.query.filter_by(id = planet_id)
        get_planet = []
        for item in planet_filter:
            get_planet.append(item.serialize())
        if get_planet != []:
            return jsonify(get_planet), 200
        else:
            return jsonify({
                    "Error": "Planet not found"
                }), 400
    if request.method == 'DELETE':
        planet_delete = Planet.query.filter_by(id = planet_id).first()
        if planet_delete is None:
            return jsonify({
                    "Error": "Planet not found"
                }), 400
        else:        
            db.session.delete(planet_delete)
            db.session.commit()
        return jsonify({
                    "Message": "Planet deleted"
                }), 200

@app.route("/user/<int:user_id>/favorites/character/<int:character_id>", methods=['POST', 'DELETE'])
def handle_favorites_character(user_id, character_id):
    if request.method == 'POST':
        data = request.json
        if data.get("name") is None:
            return jsonify({
                "error": "Campos inválidos, complete correctamente los datos de favorites"
            }), 400
        ## Instantiate new favorite
        new_favorite = Favorites()
        new_favorite.user_id = user_id
        new_favorite.name = data['name']
        new_favorite.type = "Character"
        new_favorite.type_id = character_id
        ## Add / Commit to DB
        db.session.add(new_favorite)
        db.session.commit()
        return jsonify(data), 201
    if request.method == 'DELETE':
        favorite_character_delete = Favorites.query.filter_by(user_id = user_id, type_id = character_id, type = "Character").first()
        if favorite_character_delete is None:
            return jsonify({
                    "Error": "Favorite character not found"
                }), 400
        else:        
            db.session.delete(favorite_character_delete)
            db.session.commit()
        return jsonify({
                    "Message": "Favorite character deleted"
                }), 200

@app.route("/user/<int:user_id>/favorites/planet/<int:planet_id>", methods=['POST', 'DELETE'])
def handle_favorites_planet(user_id, planet_id):
    if request.method == 'POST':
        data = request.json
        if data.get("name") is None:
            return jsonify({
                "error": "Campos inválidos, complete correctamente los datos de favorites"
            }), 400
        ## Instantiate new favorite
        new_favorite = Favorites()
        new_favorite.user_id = user_id
        new_favorite.name = data['name']
        new_favorite.type = "Planet"
        new_favorite.type_id = planet_id
        ## Add / Commit to DB
        db.session.add(new_favorite)
        db.session.commit()
        return jsonify(data), 201
    if request.method == 'DELETE':
        favorite_planet_delete = Favorites.query.filter_by(user_id = user_id, type_id = planet_id, type = "Planet").first()
        if favorite_planet_delete is None:
            return jsonify({
                    "Error": "Favorite planet not found"
                }), 400
        else:        
            db.session.delete(favorite_planet_delete)
            db.session.commit()
        return jsonify({
                    "Message": "Favorite planet deleted"
                }), 200

@app.route("/user/<int:user_id>/favorites", methods=['GET'])
def handle_user_favorites(user_id):
    if request.method == 'GET':
        user_favorites_filter = Favorites.query.filter_by(user_id = user_id)
        get_user_favorites = []
        for item in user_favorites_filter:
            get_user_favorites.append(item.serialize())
        if get_user_favorites != []:
            return jsonify(get_user_favorites), 200
        else:
            return jsonify({
                    "Error": "User not found in favorites table"
                }), 400

# this only runs if `$ python src/app.py` is executed
if __name__ == '__main__':
    PORT = int(os.environ.get('PORT', 3000))
    app.run(host='0.0.0.0', port=PORT, debug=False)
