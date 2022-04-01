"""
This module takes care of starting the API Server, Loading the DB and Adding the endpoints
"""
import os
from flask import Flask, request, jsonify, url_for
from flask_migrate import Migrate
from flask_swagger import swagger
from flask_cors import CORS
from utils import APIException, generate_sitemap
from admin import setup_admin
from models import db, User, Todo
#from models import Person

app = Flask(__name__)
app.url_map.strict_slashes = False
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DB_CONNECTION_STRING')
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

@app.route('/user', methods=['GET'])
def handle_hello():

    response_body = {
        "msg": "Hello, this is your GET /user response "
    }

    return jsonify(response_body), 200



@app.route('/todo', methods=['GET'])
def get_todo():

    todo_query = Todo.query.all()
    all_todos = list(map(lambda x: x.serialize(), todo_query))

    return jsonify(all_todos), 200



@app.route('/todo', methods=['POST'])
def post_todo():

    body = request.get_json()

    todo1 = Todo(label = body['label'], done = body['done'])
    db.session.add(todo1)
    db.session.commit()

    todo_query = Todo.query.all()
    all_todos = list(map(lambda x: x.serialize(), todo_query))

    return jsonify(all_todos), 200



@app.route('/todo', methods=['PUT'])
def put_todo():
    
    body = request.get_json()

    todo_id = Todo.query.get(body['id'])
    if todo_id is None:
        raise APIException('User not found', status_code=404)

    if "label" in body:
        todo_id.label = body["label"]
    if "done" in body:
        todo_id.done = body["done"]
    db.session.commit()

    todo_query = Todo.query.all()
    all_todos = list(map(lambda x: x.serialize(), todo_query))

    return jsonify(all_todos), 200




@app.route('/todo/<int:id>', methods=['DELETE'])
def delete_todo(id):

    body = request.get_json()

    todo1 = Todo.query.get(id)
    if todo1 is None:
        raise APIException('User not found', status_code=404)
    db.session.delete(todo1)
    db.session.commit()

    todo_query = Todo.query.all()
    all_todos = list(map(lambda x: x.serialize(), todo_query))

    return jsonify(all_todos), 200





# this only runs if `$ python src/main.py` is executed
if __name__ == '__main__':
    PORT = int(os.environ.get('PORT', 3000))
    app.run(host='0.0.0.0', port=PORT, debug=False)
