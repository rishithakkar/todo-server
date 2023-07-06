from flask import request
from include import app
from include.db.user_controller import create_user, login_user, check_user, invalid_user_response
from include.db.todo_controller import create_todo, get_todos, update_todo, delete_todo

# Custom middleware
@app.before_request
def header_validation_middleware():
    # List of APIs (routes) to apply the middleware
    api_routes = ['/todo', '/todos']

    # Check if the current request matches the API routes to apply the middleware
    route = request.url_rule.rule if request.url_rule else ''
    if any(route.startswith(api_route) for api_route in api_routes):
        user_id = request.headers.get('Userid')
        is_valid = check_user(user_id)
        if not is_valid:
            return invalid_user_response()


@app.route('/')
def index():
    return "Hello, How are you doing today!"


@app.route('/register', methods=['POST'])
def register():
    data = request.get_json()   # get data from request
    res = create_user(data)    # create user in database
    return res


@app.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    res = login_user(data)
    return res


@app.route('/todo', methods=['POST'])
def create():
    data = request.get_json()
    user_id = request.headers.get('Userid')

    res = create_todo(data, user_id)
    return res


@app.route('/todos', methods=['GET'])
def get():
    user_id = request.headers.get('Userid')
    sorting = request.args.get('created_at')  # query param: asc or desc
    res = get_todos(user_id, sorting)
    return res


@app.route('/todo/<todo_id>', methods=['PUT'])
def update(todo_id):
    data = request.get_json()
    user_id = request.headers.get('Userid')

    res = update_todo(data, todo_id, user_id)
    return res


@app.route('/todo/<todo_id>', methods=['DELETE'])
def delete(todo_id):
    user_id = request.headers.get('Userid')

    res = delete_todo(todo_id, user_id)
    return res
