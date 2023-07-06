'''
    This file contains the functions that are used to interact with the database.
    The functions are used to create, read, update and delete data from the user collection.

    user schema:
    {
        "username": "string",
        "password": "string",
        "created_at": "datetime"
    }    
'''


from datetime import datetime
from include import bcrypt, db_con
from flask import jsonify, make_response
from bson.objectid import ObjectId


def create_user(data):
    # check if user exists
    if db_con.users.find_one({"username": data["username"]}):
        return make_response(
            jsonify({"message": "User already exists!"}),
            400,
        )

    # hash password
    hashed_password = bcrypt.generate_password_hash(data["password"])

    # insert user in user collection
    user_id = db_con.users.insert_one({
        "username": data["username"],
        "password": hashed_password,
        "created_at": datetime.utcnow(),
    }).inserted_id

    return make_response(
        jsonify({"message": "User register successfully!", "user_id": str(user_id)}),
        201,
    )


def login_user(data):
    # check if user exists
    user = db_con.users.find_one({"username": data["username"]})
    if not user:
        return make_response(
            jsonify({"message": "User does not exist! Please register first!"}),
            400,
        )

    # check if password is correct
    if not bcrypt.check_password_hash(user["password"], data["password"]):
        return make_response(
            jsonify({"message": "Invalid credentials!"}),
            400,
        )

    return make_response(
        jsonify({"message": "User logged in!", "user_id": str(user["_id"])}),
        200,
    )

# check user is valid or not by user_id
def check_user(user_id):
    if not user_id:
        return False
    
    if ObjectId.is_valid(user_id):
        user = db_con.users.find_one({"_id": ObjectId(user_id)})
        if not user:
            return False
        return True
    return False


def invalid_user_response():
    return make_response(
        jsonify({"message": "Invalid user!"}),
        200,    # TODO: 200 because we I got CORS error with 401 in frontend
    )
