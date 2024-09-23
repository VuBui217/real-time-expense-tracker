import re
from flask import Blueprint, request, jsonify
from flask_login import login_user, login_required, current_user
from app import db, bcrypt
from app.models import Users, Expense
from werkzeug.security import generate_password_hash, check_password_hash
import jwt
from datetime import datetime, timedelta, timezone
from functools import wraps
from sqlalchemy import func

auth = Blueprint("auth", __name__)

@auth.route("/signup", methods=["POST"])
def signup():
    data = request.get_json()
    print("Received data:", data)  # Check if request data is correct
    username = data.get("username")
    email = data.get("email")
    password = data.get("password")

    if not username or not email or not password:
        print("Missing fields")
        return jsonify({"error": "Username, email, and password are required"}), 400

    # Check if the user already exists by email
    user = Users.query.filter_by(email=email).first()
    print("User from database:", user)  # Check what is returned from the query
    if user:
        return jsonify({"message": "User already exists. Please sign in."}), 400

    # Create a new user
    new_user = Users(
        username=username,
        email=email,
        password=generate_password_hash(password)
    )
    
    print("Created user successfully:")  # Check if new user is created

    # Add the user to the database
    try:
        db.session.add(new_user)
        db.session.commit()
        return jsonify({"message": "User created successfully"}), 201
    except Exception as e:
        # Handle any database errors
        db.session.rollback()
        print("Error:", e)
        return jsonify({"error": str(e)}), 500



# Route for signin
@auth.route("/signin", methods=["POST"])
def signin():
    data = request.get_json()
    if not data or not data.get("email") or not data.get("password"):
        return jsonify({"Error": "Proper credentials were not provided"}), 401

    user = Users.query.filter(Users.email == data.get("email")).first()
    if not user:
        return jsonify({"Error": "Please create an account"}), 401

    if check_password_hash(user.password, data.get("password")):
        
        token = jwt.encode({
            'id': user.id,
            'exp': datetime.utcnow() + timedelta(minutes=3)
        }, "secret", algorithm="HS256")
        return jsonify({'token': token}), 201

    return jsonify({"Error": "Please check your credentials"}), 401


def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = None
        if "Authorization" in request.headers:
            token_header = request.headers["Authorization"]


            # Check if token starts with "Bearer"
            if token_header.startswith("Bearer "):
                token = token_header.split(" ")[1]  # Extract token part
   
            
        if not token:
            print("Token is missing")
            return jsonify({"Message": "Token is missing"}), 401

        try:
            # Decode the JWT using the secret key
            secret_key = "secret"
            user_data = jwt.decode(token, secret_key, algorithms=["HS256"])
            current_user = Users.query.filter_by(id=user_data["id"]).first()

            if not current_user:
                print("User not found")
                return jsonify({"Message": "User not found"}), 404

        except jwt.ExpiredSignatureError:
            print("Token has expired")
            return jsonify({"Message": "Token has expired"}), 401

        except jwt.InvalidTokenError:
            print("Token is invalid")
            return jsonify({"Message": "Token is invalid"}), 401

        # Proceed if the token is valid and user is found
        return f(current_user, *args, **kwargs)

    return decorated

    
    
    

@auth.route("/expenses", methods=["GET"])
@token_required
def getAllFunds(current_user):
    # Query expenses for the current user
    expenses = Expense.query.filter_by(userId=current_user.id).all()

    # Initialize total sum
    totalSum = 0

    # If there are expenses, calculate the total sum
    if expenses:
        totalSum = db.session.query(db.func.round(db.func.sum(Expense.amount), 2)).filter_by(userId=current_user.id).scalar() or 0
    
    # Return the list of expenses and the total sum
    return jsonify({
        "Data": [expense.serialize for expense in expenses],
        "sum": float(totalSum)  # Make sure the sum is returned as a float
    })
    
    
    
    

@auth.route("/expenses", methods=["POST"])
@token_required  # Assuming this decorator verifies the JWT and provides current_user
def createExpense(current_user):
    data = request.get_json()  # Get the JSON data from the request body
    amount = data.get("amount")
    description = data.get("description")
    category = data.get("category")
    
    # Validate that all required fields are present
    if not amount or not description or not category:
        return jsonify({"error": "Amount, description, and category are required"}), 400

    # Create a new expense
    expense = Expense(
        amount=amount,  # Get amount from request data
        userId=current_user.id,  # Use the authenticated user's ID from JWT
        description=description,  # Get description from request data
        category=category  # Get category from request data
    )

    # Add the expense to the database
    db.session.add(expense)
    db.session.commit()

    # Optionally, serialize the expense to return in the response
    return jsonify({
        "message": "Expense created successfully",
        "expense": {
            "id": expense.id,
            "amount": float(expense.amount),  # Make sure to convert amount to float
            "description": expense.description,
            "category": expense.category,
            "created_at": expense.created_at
        }
    }), 201




@auth.route("/expenses/<int:expense_id>", methods=["DELETE"])
@token_required
def delete_expense(current_user, expense_id):
    # Find the expense by ID and ensure it belongs to the current user
    expense = Expense.query.filter_by(id=expense_id, userId=current_user.id).first()

    if not expense:
        return jsonify({"error": "Expense not found or does not belong to the user"}), 404

    try:
        # Delete the expense from the database
        db.session.delete(expense)
        db.session.commit()
        return jsonify({"message": "Expense deleted successfully"}), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": str(e)}), 500










@auth.route("/expenses/<int:expense_id>", methods=["PUT"])
@token_required
def edit_expense(current_user, expense_id):
 
    data = request.get_json()
 

    # Validate input data
    if not data:
  
        return jsonify({"error": "No input data provided"}), 400

    # Find the existing expense for the authenticated user
 
    expense = Expense.query.filter_by(id=expense_id, userId=current_user.id).first()


    if not expense:

        return jsonify({"error": "Expense not found or does not belong to the user"}), 404



    # Update the fields if they are provided in the request
    if "amount" in data:
        expense.amount = data["amount"]

    if "description" in data:
        expense.description = data["description"]

    if "category" in data:
        expense.category = data["category"]


  

    try:
  
        db.session.commit()
        return jsonify({
            "message": "Expense updated successfully",
            "expense": {
                "id": expense.id,
                "amount": float(expense.amount),
                "description": expense.description,
                "category": expense.category,
                "created_at": expense.created_at
            }
        }), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": "An error occurred while updating the expense"}), 500

