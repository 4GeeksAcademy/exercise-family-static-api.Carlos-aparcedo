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
# a partir de esta línea construyo los endpoints

@app.route('/members', methods=['GET'])
def get_all_members():

    # this is how you can use the Family datastructure by calling its methods
    members = jackson_family.get_all_members()
    response_body = members
    
    return jsonify(response_body), 200


@app.route('/member/<int:member_id>', methods=['GET'])
def get_member(member_id):

    # this is how you can use the Family datastructure by calling its methods
    get_member = jackson_family.get_member(member_id)
    #deleted_member = jackson_family.delete_member(id)
    if get_member is not None:
        response_body = {"message": "Member generate successfully", "family": get_member}
        return jsonify(response_body), 200
    else:
        response_body = {"message": "Member not found"}
        return jsonify(response_body), 404

   


@app.route('/member', methods=['POST'])
def member():
    request_body = request.json

    member = {
        "id": jackson_family._generateId(),
        "first_name": request_body["first_name"],
        "last_name": "Jackson",
        "age": request_body["age"],
        "lucky_numbers": request_body["lucky_numbers"]
    }

    jackson_family.add_member(member)

    return jsonify({"message": "Member added successfully"}), 200


@app.route('/members/<int:id>', methods=['DELETE'])
def delete_member(id):

    # this is how you can use the Family datastructure by calling its methods
    deleted_member = jackson_family.delete_member(id)
    if deleted_member is not None:
        response_body = {"message": "Member deleted successfully", "family": deleted_member}
        return jsonify(response_body), 200
    else:
        response_body = {"message": "Member not found"}
        return jsonify(response_body), 404
    
    



# this only runs if `$ python src/app.py` is executed
if __name__ == '__main__':
    PORT = int(os.environ.get('PORT', 3000))
    app.run(host='0.0.0.0', port=PORT, debug=True)