from flask import Flask, render_template, request,jsonify
app = Flask(__name__)

import json
from bson import ObjectId

from pymongo import MongoClient
import certifi
ca = certifi.where()
client = MongoClient('mongodb+srv://sparta:test@cluster0.cbeupio.mongodb.net/?retryWrites=true&w=majority', tlsCAFile = ca)
db = client.dbsparta
class JsonEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, ObjectId):
            return str(obj)
        return super(JsonEncoder, self).default(obj)

app.json_encoder = JsonEncoder

@app.route('/')
def home():
    return render_template('index.html')

@app.route("/todo", methods=["POST"])
def todo_post():
    todo_receive = request.form['todo_give']
    todo_list = list(db.todo.find({}, {'_id': False}))
    count = len(todo_list) + 1
    doc = {
        'todo':todo_receive,
        'num' :count,
        'done' : 0,
    }
    db.todo.insert_one(doc)
    return jsonify({'msg': '저장완료!'})
    
@app.route("/todo", methods=["GET"])
def todo_get():
    all_todos = list(db.todo.find({}, {'_id': False}))
    return jsonify({'result': all_todos})
    
@app.route("/todo/active", methods=["GET"])
def todos_active():
    todos = list(db.todo.find({'done': 0}, {'_id': False}))
    return jsonify({"actives": todos})

@app.route("/todo/completed", methods=["GET"])
def todos_completed():
    done = list(db.todo.find({'done': 1}, {'_id': False}))
    return jsonify({"completed": done})

@app.route("/todo", methods=["DELETE"])
def todo_delete():
    num_receive = request.form["num"]
    db.todo.delete_one({'num': int(num_receive)})
    return jsonify({'msg': "삭제 완료!"})

@app.route("/todo/done", methods=["POST"])
def todo_done():
    num_receive = request.form['done_give']
    db.todo.update_one({'num': int(num_receive)}, {'$set': {'done': 1}})
    return jsonify({'msg': '계획 완료!'})

if __name__ == "__main__":
    app.run("0.0.0.0", port=5001, debug=True)
    