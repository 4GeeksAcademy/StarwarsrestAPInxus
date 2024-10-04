def get_user_favorites(user_id):
    from models import FavoritePlanet, FavoritePerson
    from app import db

    favorites = {
        'planets': [fav.planet_id for fav in FavoritePlanet.query.filter_by(user_id=user_id).all()],
        'people': [fav.person_id for fav in FavoritePerson.query.filter_by(user_id=user_id).all()],
    }
    return favorites
