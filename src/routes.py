from flask import jsonify, request
from app import app, db

@app.route('/people', methods=['GET'])
def get_people():
    from models import Person  # Local import
    people = Person.query.all()
    return jsonify([{'id': person.id, 'name': person.name} for person in people])

@app.route('/planets', methods=['GET'])
def get_planets():
    from models import Planet  # Local import
    planets = Planet.query.all()
    return jsonify([{'id': planet.id, 'name': planet.name} for planet in planets])

# Continue defining other routes...
