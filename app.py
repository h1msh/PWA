from flask import Flask, request, jsonify, render_template
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from datetime import datetime

app = Flask(__name__)
CORS(app)  # Allow cross-origin requests for development
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///reviews.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

# User model
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(100), nullable=False, unique=True)
    password = db.Column(db.String(100), nullable=False)

# Review model
class Review(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    review_date = db.Column(db.DateTime, default=datetime.utcnow)
    username = db.Column(db.String(100), nullable=False)
    rating = db.Column(db.Integer, nullable=False)
    review_text = db.Column(db.String(500), nullable=False)

# Create tables if they don't exist
with app.app_context():
    db.create_all()

# User registration route
@app.route('/register', methods=['POST'])
def register():
    data = request.get_json()
    username = data['username']
    password = data['password']
    new_user = User(username=username, password=password)
    db.session.add(new_user)
    db.session.commit()
    return jsonify({"message": "User registered successfully"}), 201

# User login route
@app.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    username = data['username']
    password = data['password']
    user = User.query.filter_by(username=username, password=password).first()
    if user:
        return jsonify({"message": "Login successful"}), 200
    return jsonify({"message": "Invalid credentials"}), 401

# Route to post and view reviews
@app.route('/reviews', methods=['GET', 'POST'])
def reviews():
    if request.method == 'GET':
        all_reviews = Review.query.all()
        reviews_data = [{
            "title": review.title,
            "review_date": review.review_date,
            "username": review.username,
            "rating": review.rating,
            "review_text": review.review_text
        } for review in all_reviews]
        return jsonify(reviews_data), 200

    if request.method == 'POST':
        data = request.get_json()
        title = data['title']
        rating = data['rating']
        review_text = data['review_text']
        username = data['username']
        new_review = Review(title=title, username=username, rating=rating, review_text=review_text)
        db.session.add(new_review)
        db.session.commit()
        return jsonify({"message": "Review posted successfully"}), 201

if __name__ == '__main__':
    app.run(debug=True)
