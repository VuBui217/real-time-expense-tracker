import re
from flask import Blueprint, request, jsonify
from flask_login import LoginManager, login_required, login_user, current_user
from app import db, bcrypt
from app.models import User

auth = Blueprint("auth", __name__)
login_manager = LoginManager()
login_manager.login_view = "auth.signin"


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

    # Check if the user password matches
    if user is None or not bcrypt.check_password_hash(user.password, password):
        return jsonify({"error": "Invalid email or password"}), 401

    # Log the user in
    login_user(user)

    return jsonify({"message": f"Welcome back, {user.username}!"}), 200


@auth.route("/users", methods=["GET"])
def list_users():
    users = User.query.all()  # Query all users from the database
    user_list = [
        {"username": user.username, "email": user.email} for user in users
    ]  # Create a list of user details
    return jsonify(user_list)  # Return the list as a JSON response


@auth.route("/password-reset", methods=["POST"])
def password_reset():
    data = request.get_json()
    token = data.get("token")
    new_password = data.get("password")

    # Find user by reset token
    user = User.query.filter_by(reset_token=token).first()
    if not user:
        return jsonify({"error": "Invalid or expired token"}), 400

    # Update the user's password
    hashed_password = bcrypt.generate_password_hash(
        new_password).decode("utf-8")
    user.password = hashed_password
    user.reset_token = None  # Invalidate the token
    db.session.commit()

    return jsonify({"message": "Your password has been reset successfully"}), 200


@auth.route("/change-password", methods=["PUT"])
@login_required
def change_password():
    data = request.get_json()
    current_password = data.get("current_password")
    new_password = data.get("new_password")

    # Validate presence of current and new passwords
    if not current_password:
        return jsonify({"error": "Current password is required"}), 400

    if not new_password:
        return jsonify({"error": "New password is required"}), 400

    # Validate that the current password is correct
    if not bcrypt.check_password_hash(current_user.password, current_password):
        return jsonify({"error": "Incorrect current password"}), 400

    # Validate the new password (e.g., length, complexity)
    if len(new_password) < 8:
        return (
            jsonify({"error": "New password must be at least 8 characters long"}),
            400,
        )

    # Hash the new password and update the user record
    hashed_password = bcrypt.generate_password_hash(
        new_password).decode("utf-8")
    current_user.password = hashed_password
    db.session.commit()

    return jsonify({"message": "Password updated successfully"}), 200
