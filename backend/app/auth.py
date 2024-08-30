from flask import Blueprint, request, jsonify
from app import db, bcrypt
from app.models import User

auth = Blueprint("auth", __name__)


@auth.route("/signup", methods=["POST"])
def signup():
    data = request.get_json()
    username = data.get("username")
    email = data.get("email")
    password = data.get("password")

    # Check if the username or email already exists
    user_exists = User.query.filter(
        (User.email == email) | (User.username == username)
    ).first()
    if user_exists:
        return jsonify({"error": "Username or email already exists"}), 400

    # Hash the password
    hashed_password = bcrypt.generate_password_hash(password).decode("utf-8")

    # Create a new user and add to the database
    user = User(username=username, email=email, password=hashed_password)
    db.session.add(user)
    db.session.commit()

    return jsonify({"message": "User created successfully"}), 201


@auth.route("/signin", methods=["POST"])
def signin():
    data = request.get_json()
    email = data.get("email")
    password = data.get("password")

    # Check if the user exists
    user = User.query.filter_by(email=email).first()
    if user is None:
        return jsonify({"errror": "Invalid email or password"}), 401

    # Check if the user password matches
    if not bcrypt.check_password_hash(user.password, password):
        return jsonify({"error": "Invalid email or password"}), 401

    # Log the user in
    # login_user(user)  # Ignore for now

    return jsonify({"message": f"Welcome back, {user.username}!"}), 200


@auth.route("/users", methods=["GET"])
def list_users():
    users = User.query.all()  # Query all users from the database
    user_list = [
        {"username": user.username, "email": user.email} for user in users
    ]  # Create a list of user details
    return jsonify(user_list)  # Return the list as a JSON response
