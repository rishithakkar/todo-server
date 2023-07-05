'''
    This file contains the functions that are used to interact with the database.
    The functions are used to create, read, update and delete data from todo collection.

    todo schema:
    {
        "title": "string",
        "description": "string",
        "label": "string",
        "created_at": "datetime",
        "created_by": ObjectId(user_id), # reference to user collection
        "completed": "boolean"
    }
'''

from datetime import datetime
from include import db_con
from flask import jsonify, make_response
from bson.objectid import ObjectId


def create_todo(data, user_id):
    # insert todo in todo collection
    db_con.todos.insert_one({
        "title": data["title"],
        "description": data["description"],
        "label": data["label"],
        "created_at": datetime.utcnow(),
        "created_by": ObjectId(user_id),
        "completed": False,
    })

    return make_response(
        jsonify({"message": "Todo created!"}),
        200,
    )


def get_todos(user_id, sorting):
    if sorting == 'asc':
        sort = 1
    elif sorting == 'desc':
        sort = -1
    else:
        sort = -1   # default sorting

    # get todos from todo collection
    todos = db_con.todos.find(
        {"created_by": ObjectId(user_id)}).sort("created_at", sort)

    # check if todos exist
    if not todos:
        return make_response(
            jsonify({"message": "No todos found!"}),
            400,
        )

    # create list of todos
    todo_list = []
    for todo in todos:
        todo_list.append({
            "id": str(todo["_id"]),
            "title": todo["title"],
            "description": todo["description"],
            "label": todo["label"],
            "created_at": todo["created_at"],
            "completed": todo["completed"],
        })

    return make_response(
        jsonify({"todos": todo_list}),
        200,
    )


def update_todo(data, todo_id, user_id):
    # check if todo id is valid
    if not ObjectId.is_valid(todo_id):
        return make_response(
            jsonify({"message": "Invalid todo id!"}),
            400,
        )
    
    # check if todo exists
    todo = db_con.todos.find_one(
        {"_id": ObjectId(todo_id), "created_by": ObjectId(user_id)})
    if not todo:
        return make_response(
            jsonify({"message": "Todo not found!"}),
            400,
        )
    
    # create payload of data to be updated
    payload = {}
    for key in data:
        if data[key] != '':
            payload[key] = data[key]

    # update todo in todo collection
    db_con.todos.update_one(
        {"_id": ObjectId(todo_id)},
        {"$set": payload}
    )

    return make_response(
        jsonify({"message": "Todo updated!"}),
        200,
    )


def delete_todo(todo_id, user_id):
    # check if todo id is valid
    if not ObjectId.is_valid(todo_id):
        return make_response(
            jsonify({"message": "Invalid todo id!"}),
            400,
        )
    
    # check if todo exists
    todo = db_con.todos.find_one(
        {"_id": ObjectId(todo_id), "created_by": ObjectId(user_id)})
    if not todo:
        return make_response(
            jsonify({"message": "Todo not found!"}),
            400,
        )

    # delete todo from todo collection
    db_con.todos.delete_one({"_id": ObjectId(todo_id)})

    return make_response(
        jsonify({"message": "Todo deleted!"}),
        200,
    )
