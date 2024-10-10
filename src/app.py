from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_restful import Api, Resource

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///starwars.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)
migrate = Migrate(app, db)
api = Api(app)

# Define los modelos
class People(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)

class Planet(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True, nullable=False)

class FavoritePlanet(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    planet_id = db.Column(db.Integer, db.ForeignKey('planet.id'), nullable=False)

class FavoritePeople(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    people_id = db.Column(db.Integer, db.ForeignKey('people.id'), nullable=False)

# Define los recursos
class PeopleResource(Resource):
    def get(self):
        people = People.query.all()
        return [{'id': p.id, 'name': p.name} for p in people]

class PeopleDetailResource(Resource):
    def get(self, people_id):
        person = People.query.get_or_404(people_id)
        return {'id': person.id, 'name': person.name}

class PlanetResource(Resource):
    def get(self):
        planets = Planet.query.all()
        return [{'id': p.id, 'name': p.name} for p in planets]

class PlanetDetailResource(Resource):
    def get(self, planet_id):
        planet = Planet.query.get_or_404(planet_id)
        return {'id': planet.id, 'name': planet.name}

class UserResource(Resource):
    def get(self):
        users = User.query.all()
        return [{'id': u.id, 'username': u.username} for u in users]

class UserFavoritesResource(Resource):
    def get(self):
        user_id = 1  # Cambia esto según sea necesario
        favorites = FavoritePlanet.query.filter_by(user_id=user_id).all()
        return [{'planet_id': f.planet_id} for f in favorites]

class AddFavoritePlanetResource(Resource):
    def post(self, planet_id):
        user_id = 1  # Cambia esto según sea necesario
        favorite = FavoritePlanet(user_id=user_id, planet_id=planet_id)
        db.session.add(favorite)
        db.session.commit()
        return {'message': 'Favorite planet added'}, 201

class DeleteFavoritePlanetResource(Resource):
    def delete(self, planet_id):
        user_id = 1  # Cambia esto según sea necesario
        favorite = FavoritePlanet.query.filter_by(user_id=user_id, planet_id=planet_id).first()
        if favorite:
            db.session.delete(favorite)
            db.session.commit()
            return {'message': 'Favorite planet deleted'}, 200
        return {'message': 'Favorite planet not found'}, 404

# Agrega los endpoints
api.add_resource(PeopleResource, '/people')
api.add_resource(PeopleDetailResource, '/people/<int:people_id>')
api.add_resource(PlanetResource, '/planets')
api.add_resource(PlanetDetailResource, '/planets/<int:planet_id>')
api.add_resource(UserResource, '/users')
api.add_resource(UserFavoritesResource, '/users/favorites')
api.add_resource(AddFavoritePlanetResource, '/favorite/planet/<int:planet_id>')
api.add_resource(DeleteFavoritePlanetResource, '/favorite/planet/<int:planet_id>')

if __name__ == '__main__':
    app.run(debug=True)
