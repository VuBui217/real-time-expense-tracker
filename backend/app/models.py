from app import db
from sqlalchemy.sql import func


class Users(db.Model):
    __tablename__ = "users"
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(150), unique=True, nullable=False)
    email = db.Column(db.String(150), unique=True, nullable=False)
    password = db.Column(db.String(200), nullable=False)
    created_at = db.Column(db.DateTime(timezone=True),
                           server_default=func.now())
    
    expense = db.relationship('Expense', backref='Users', lazy=True)

    def __repr__(self):
        return f'<users {self.id}>'


# UserExpense model
class Expense(db.Model):
    __tablename__ = "expense"
    id = db.Column(db.Integer, primary_key=True)
    amount = db.Column(db.Numeric(10,2), nullable=False)  # Corrected db.Integer
    userId = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    description = db.Column(db.String(255), nullable=False)
    category = db.Column(db.String(150), nullable=False)
    created_at = db.Column(db.DateTime(timezone=True), server_default=func.now())
    
    
    @property
    def serialize(self):
        
        return{
            "id": self.id,
            "amount": self.amount,
            "description" : self.description,
            "category": self.category,
            "created_at" : self.created_at
        }

    def __repr__(self):
        return f'<expense {self.category} - {self.amount}>'
    
