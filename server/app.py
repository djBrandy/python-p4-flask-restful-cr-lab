#!/usr/bin/env python3

from flask import Flask, jsonify, request, make_response
from flask_migrate import Migrate
from flask_restful import Api, Resource

from models import db, Plant

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///plants.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.json.compact = True

migrate = Migrate(app, db)
db.init_app(app)

api = Api(app)

class Plants(Resource):
    def get(self):
        plant_getter = Plant.query.all()
        plant_list = [plant.to_dict() for plant in plant_getter]
      
        return make_response(jsonify(plant_list), 200)
    

    def post(self):
        data = request.get_json()

        plant_getter = Plant(
            name=data.get('name'),
            image=data.get('image'),
            price=data.get('price')
)
        db.session.add(plant_getter)
        db.session.commit()
        
        return make_response(plant_getter.to_dict(), 500)
 
api.add_resource(Plants, '/plants')


class PlantById(Resource):
    def get(self, id):
        
        plant_getter_dict = Plant.query.filter_by(id=id).first().to_dict()
   
        return make_response(jsonify(plant_getter_dict), 200)
    
api.add_resource(PlantById, '/plants/<int:id>')     

if __name__ == '__main__':
    app.run(port=5555, debug=True)
