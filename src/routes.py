from flask import jsonify, request
from app import app, db
from models import Person, Planet, User, FavoritePlanet, FavoritePerson

@app.route('/people', methods=['GET'])
def get_people():
    people = Person.query.all()
    return jsonify([{'id': person.id, 'name': person.name} for person in people])

@app.route('/people/<int:people_id>', methods=['GET'])
def get_person(people_id):
    person = Person.query.get_or_404(people_id)
    return jsonify({'id': person.id, 'name': person.name})

@app.route('/planets', methods=['GET'])
def get_planets():
    planets = Planet.query.all()
    return jsonify([{'id': planet.id, 'name': planet.name} for planet in planets])

@app.route('/planets/<int:planet_id>', methods=['GET'])
def get_planet(planet_id):
    planet = Planet.query.get_or_404(planet_id)
    return jsonify({'id': planet.id, 'name': planet.name})

@app.route('/users', methods=['GET'])
def get_users():
    users = User.query.all()
    return jsonify([{'id': user.id, 'username': user.username} for user in users])

@app.route('/users/favorites', methods=['GET'])
def get_favorites():
    user_id = request.args.get('user_id')
    favorites = {
        'planets': [fav.planet_id for fav in FavoritePlanet.query.filter_by(user_id=user_id).all()],
        'people': [fav.person_id for fav in FavoritePerson.query.filter_by(user_id=user_id).all()],
    }
    return jsonify(favorites)

@app.route('/favorite/planet/<int:planet_id>', methods=['POST'])
def add_favorite_planet(planet_id):
    user_id = request.json.get('user_id')
    favorite = FavoritePlanet(user_id=user_id, planet_id=planet_id)
    db.session.add(favorite)
    db.session.commit()
    return jsonify({'message': 'Favorite planet added'}), 201

@app.route('/favorite/people/<int:people_id>', methods=['POST'])
def add_favorite_people(people_id):
    user_id = request.json.get('user_id')
    favorite = FavoritePerson(user_id=user_id, person_id=people_id)
    db.session.add(favorite)
    db.session.commit()
    return jsonify({'message': 'Favorite person added'}), 201

@app.route('/favorite/planet/<int:planet_id>', methods=['DELETE'])
def delete_favorite_planet(planet_id):
    user_id = request.json.get('user_id')
    favorite = FavoritePlanet.query.filter_by(user_id=user_id, planet_id=planet_id).first()
    if favorite:
        db.session.delete(favorite)
        db.session.commit()
        return jsonify({'message': 'Favorite planet deleted'}), 200
    return jsonify({'message': 'Favorite planet not found'}), 404

@app.route('/favorite/people/<int:people_id>', methods=['DELETE'])
def delete_favorite_people(people_id):
    user_id = request.json.get('user_id')
    favorite = FavoritePerson.query.filter_by(user_id=user_id, person_id=people_id).first()
    if favorite:
        db.session.delete(favorite)
        db.session.commit()
        return jsonify({'message': 'Favorite person deleted'}), 200
    return jsonify({'message': 'Favorite person not found'}), 404
