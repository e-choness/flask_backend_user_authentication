from flask import Flask, jsonify, abort, request

app = Flask(__name__)

todos = [
    {
        'id': 1,
        'title': u'learn flask',
        'description': u'Search youtube',
        'done': False
    },
    {
        'id': 2,
        'title': u'learn python',
        'description': u'Search again',
        'done': False
    }
]


@app.route('/todos', methods=['GET'])
def get_todos():
    return jsonify({'todos': todos})


@app.route('/todos/<int:todo_id>', methods=['GET'])
def get_todo(todo_id):
    todo = [todo for todo in todos if todo['id'] == todo_id]
    if len(todo) == 0:
        abort(404)
    return jsonify({'todo': todo[0]})


@app.route('/')
def index():
    return "Hello, Todos"


@app.route('/todos', methods=['POST'])
def creat_todo():
    if not request.json or not 'title' in request.json:
        abort(400)
    todo = {
        'id': todos[-1]['id'] + 1,
        'title': request.json['title'],
        'description': request.json.get('description', ""),
        'done': False
    }
    todos.append(todo)
    return jsonify({'todo': todo}), 201


@app.route('/todos/<int:todo_id>', methods=['POST'])
def update_todo(todo_id):
    todo = [todo for todo in todos if todo['id'] == todo_id]
    if len(todo) == 0:
        abort(404)
    if not request.json:
        abort(400)
    if 'title' in request.json and type(request.json['title']) != unicode:
        abort(400)
    if 'description' in request.json and type(request.json['description']) != unicode:
        abort(400)
    if 'done' in request.json and type(request.json['done']) is not bool:
        abort(400)

    todo[0]['title'] = request.json.get('title', todo[0]['title'])
    todo[0]['description'] = request.json.get('description', todo[0]['description'])
    todo[0]['done'] = request.json.get('done', todo[0]['done'])

    return jsonify({'todo': todo})


@app.route('/todos/<int:todo_id>', methods=['DELETE'])
def delete_todo(todo_id):
    todo = [todo for todo in todos if todo['id'] == todo_id]
    if len(todo) == 0:
        abort(404)
    todos.remove(todo[0])
    return jsonify({'result': True})


if __name__ == '__main__':
    app.run(debug=True)
