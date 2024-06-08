import requests

from pycountry import countries

from models import db, Country, City, Gods

API_KEY = 'AIzaSyDToH_dCRhQJ8t9XOEQkSqpLg_yFUXioDU'
country = 'Ukraine'
URL = 'https://maps.googleapis.com/maps/api/place/textsearch/json'


def fill_db_countries():
    for country in countries:
        country_add = Country(name=country.name)
        db.session.add(country_add)
        db.session.commit()


def fill_db_cities():
    countries = Country.query.all()
    for country in countries:
        params = {
            'query': f'cities in {country.name}',
            'key': API_KEY
        }
        cities = requests.get(URL, params=params).json()['results']
        for city in cities:
            city_name = city['formatted_address'].split(',')[0]
            if len(city_name) >= 50:
                continue
            city_add = City(name=city_name, country_id=country.id)
            db.session.add(city_add)
            db.session.commit()


