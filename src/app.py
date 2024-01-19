"""
This module takes care of starting the API Server, Loading the DB and Adding the endpoints
"""
import os
from flask import Flask, request, jsonify, url_for
from flask_cors import CORS
from utils import APIException, generate_sitemap
from datastructures import FamilyStructure
#from models import Person

app = Flask(__name__)
app.url_map.strict_slashes = False
CORS(app)

# create the jackson family object
jackson_family = FamilyStructure("Jackson")

# Handle/serialize errors like a JSON object
@app.errorhandler(APIException)
def handle_invalid_usage(error):
    return jsonify(error.to_dict()), error.status_code

# generate sitemap with all your endpoints
@app.route('/')
def sitemap():
    return generate_sitemap(app)

@app.route('/members', methods=['GET'])
def handle_hello():

    # this is how you can use the Family datastructure by calling its methods
    members = jackson_family.get_all_members()
    response_body = {
        "hello": "world",
        "family": members
    }


    return jsonify(response_body), 200

@app.route('/member/<int:member_id>', methods=['GET']) #creacion de un endpoint 
            #  1.primero definimos la ruta y el metodo. 
            #  2. hay que crear la funcion que va a procesar la peticion(el nombre de la funcion tiene que tener un nombre de acuerdo con lo que trabajas). 
            # 3.retornar una respuesta(cada endpoint es una funcion distinta, cada una tiene un return propio)
            # 4. escribir la logica
def get_one_member(member_id):

    # this is how you can use the Family datastructure by calling its methods
    # members = jackson_family.get_all_members()
    # response_body = {
    #     "hello": "world",
    #     "family": member
    # }


    return jsonify("OK"), 200

# this only runs if `$ python src/app.py` is executed
if __name__ == '__main__':
    PORT = int(os.environ.get('PORT', 3000))
    app.run(host='0.0.0.0', port=PORT, debug=True)
