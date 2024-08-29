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
