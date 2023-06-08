from flask import Flask, render_template, request,jsonify
app = Flask(__name__)


from pymongo import MongoClient
import certifi
ca = certifi.where()
client = MongoClient('mongodb+srv://sparta:test@cluster0.cbeupio.mongodb.net/?retryWrites=true&w=majority', tlsCAFile = ca)
db = client.dbsparta

@app.route('/')
def home():
    return render_template('index.html')

@app.route("/todo", methods=["POST"])
def todo_post():
    todo_receive = request.form['todo_give']
    doc = {
        'todo':todo_receive
    }
    db.todo.insert_one(doc)
    return jsonify({'msg': '저장완료!'})
    
@app.route("/todo", methods=["GET"])
def todo_get():
    all_todos = list(db.todo.find({},{'_id':False}))

    return jsonify({'result': all_todos })

@app.route("/todo", methods=["PUT"])
def todo_put():
    todo_receive = request.form['todo_give']
    change_receive = request.form['change_give']

    doc = {
        'todo':todo_receive,
        'change':change_receive
    }
    db.users.insert_one(doc)
    db.users.update_one({'todo':todo_receive},{'$set':{'change':change_receive}})
    
    # 삭제
    return jsonify({'msg': '수정완료!'})

# # 진행중인 목록 가져오기-
# def todo_state():
#     todos = list(db.todo.find({},{'state':0}))
#     return jsonify({"actives":todos})

# # 완료된 목록 가져오기
# def todo_state_Done():
#     done = list(db.todo.find({},{'state':1}))
#     return jsonify({"completed":done})
# if __name__ == "__main__":
#     app.run("0.0.0.0", port=5001, debug=True)

#[2]
# @app.route("/todo", methods=["POST"])
# def todo_post():
#     todo_receive = request.form['todo_give']
#     todo_list = list(db.todo.find({}, {'_id': False}))
#     count = len(todo_list) + 1
#     doc = {
#         'todo':todo_receive,
#         'num' :count,
#         'done' : 0,
#     }
#     db.todo.insert_one(doc)
#     return jsonify({'msg': '저장완료!'})

# @app.route("/todo", methods=["DELETE"])
# def todo_delete():
#     num_receive = request.form["num"]
#     db.todo.delete_one({'num': int(num_receive)})
#     return jsonify({'msg': "삭제 완료!"})

# @app.route("/todo/done", methods=["POST"])
# def todo_done():
#     num_receive = request.form['done_give']
#     db.todo.update_one({'num': int(num_receive)}, {'$set': {'done': 1}})
#     return jsonify({'msg': '계획 완료!'})

if __name__ == "__main__":
    app.run("0.0.0.0", port=5001, debug=True)
    