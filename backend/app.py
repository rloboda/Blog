from flask import Flask, jsonify, request
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import create_engine
from sqlalchemy.exc import OperationalError
from werkzeug.security import generate_password_hash, check_password_hash
from flask_jwt_extended import JWTManager, create_access_token

import time, datetime
from os import environ

app = Flask(__name__)
CORS(app)

# Database Configuration
app.config['SQLALCHEMY_DATABASE_URI'] = environ.get('DB_URL')
app.config['JWT_SECRET_KEY'] = 'your_secret_key'
db = SQLAlchemy(app)
jwt = JWTManager(app) 

# Retry connecting to the database
retries = 5
while retries > 0:
    try:
        engine = create_engine('postgresql://postgres:1234@db:5432/blog')
        conn = engine.connect()
        print("✅ Database connected successfully!")
        conn.close()
        break
    except OperationalError:
        print("⏳ Database not ready, retrying in 5 seconds...")
        time.sleep(5)
        retries -= 1

if retries == 0:
    print("❌ Failed to connect to database after multiple attempts")

# Define a model
class Item(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), nullable=False)

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password_hash = db.Column(db.String(256), nullable=False)

with app.app_context():
    db.create_all()

#test route endpoint
@app.route('/', methods=['GET'])
def test():
    return jsonify({'message': 'Hello World!'})
    
@app.route('/register', methods=['POST'])
def register():
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')

    if User.query.filter_by(username=username).first():
        return jsonify({'message': 'User already exists'}), 400

    hashed_password = generate_password_hash(password)
    new_user = User(username=username, password_hash=hashed_password)
    db.session.add(new_user)
    db.session.commit()
    return jsonify({'message': 'User registered successfully'}), 201

@app.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')
    user = User.query.filter_by(username=username).first()

    if not user or not check_password_hash(user.password_hash, password):
        return jsonify({'message': 'Invalid credentials'}), 401

    access_token = create_access_token(identity=username, expires_delta=datetime.timedelta(days=1))
    return jsonify({'access_token': access_token}), 200

#get user 
@app.route('/user', methods=['GET'])
def user():
    users = User.query.all()
    return jsonify([{'id': user.id, 'username': user.username, 'password': user.password_hash} for user in users])

# API Routes
@app.route('/items', methods=['GET'])
def get_items():
    items = Item.query.all()
    return jsonify([{'id': item.id, 'name': item.name} for item in items])

@app.route('/items', methods=['POST'])
def add_item():
    data = request.json
    new_item = Item(name=data['name'])
    db.session.add(new_item)
    db.session.commit()
    return jsonify({'message': 'Item added'}), 201

if __name__ == '__main__':
    app.run(debug=True)
