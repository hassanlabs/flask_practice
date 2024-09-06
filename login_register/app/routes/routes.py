from flasgger import swag_from 
from flask import Blueprint, request, jsonify, current_app
from werkzeug.security import check_password_hash
from ..models.user import User
from ..extensions import db
import jwt, datetime

authentication = Blueprint('authentication', __name__)

@authentication.route('/', methods=['GET', 'POST'])
def home():
    return "Why are you here?"

@authentication.route('/login', methods=['POST'])
@swag_from({
    'responses': {
        200: {
            'description': 'Login successful',
            'schema': {
                'type': 'object',
                'properties': {
                    'message': {
                        'type': 'string',
                        'example': 'Login successful'
                    }
                }
            }
        },
        400: {
            'description': 'Username and password are required',
        },
        401: {
            'description': 'Invalid username or password',
        }
    },
    'parameters': [
        {
            'name': 'body',
            'in': 'body',
            'required': True,
            'schema': {
                'type': 'object',
                'properties': {
                    'username': {
                        'type': 'string',
                        'example': 'hassan'
                    },
                    'password': {
                        'type': 'string',
                        'example': 'yourpassword'
                    }
                }
            }
        }
    ]
})
def login():
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')

    if not username or not password:
        return jsonify({'error': 'Username and password are required'}), 400

    user = User.query.filter_by(username=username).first()

    if not user or not user.check_password(password):
        return jsonify({'error': 'Invalid username or password'}), 401
    
    # Create JWT token
    token = jwt.encode({
        'username': user.username,
        'exp': datetime.datetime.utcnow() + datetime.timedelta(hours=1)  # Use utcnow() here
    }, current_app.config['SECRET_KEY'], algorithm='HS256')
    return jsonify({'token': token})

# Protected route
@authentication.route('/protected', methods=['GET', 'POST'])
def protected():
    token = request.headers.get('Authorization')

    if not token:
        return jsonify({'error': 'Token is missing!'}), 401

    try:
        data = jwt.decode(token, current_app.config['SECRET_KEY'], algorithms=['HS256'])
        current_user = User.query.filter_by(username=data['username']).first()
    except jwt.ExpiredSignatureError:
        return jsonify({'error': 'Token has expired!'}), 401
    except jwt.InvalidTokenError:
        return jsonify({'error': 'Invalid token!'}), 401

    return jsonify({'message': f'Hello, {current_user.username}. You have accessed a protected route!'})

@authentication.route('/register', methods=['POST'])
@swag_from({
    'responses': {
        201: {
            'description': 'User registered successfully',
            'schema': {
                'type': 'object',
                'properties': {
                    'message': {
                        'type': 'string',
                        'example': 'User registered successfully'
                    }
                }
            }
        },
        400: {
            'description': 'All fields are required',
        },
        401: {
            'description': 'Passwords do not match or username already exists',
        }
    },
    'parameters': [
        {
            'name': 'body',
            'in': 'body',
            'required': True,
            'schema': {
                'type': 'object',
                'properties': {
                    'first_name': {
                        'type': 'string',
                        'example': 'Hassan'
                    },
                    'last_name': {
                        'type': 'string',
                        'example': 'Tariq'
                    },
                    'username': {
                        'type': 'string',
                        'example': 'hassan'
                    },
                    'email': {
                        'type': 'string',
                        'example': 'hassan@example.com'
                    },
                    'password': {
                        'type': 'string',
                        'example': 'yourpassword'
                    },
                    'confirm_password': {
                        'type': 'string',
                        'example': 'yourpassword'
                    },
                    'phone_number': {
                        'type': 'string',
                        'example': '1234567890'
                    },
                    'age': {
                        'type': 'integer',
                        'example': 25
                    }
                }
            }
        }
    ]
})
def register():
    data = request.get_json()

    first_name = data.get('first_name')
    last_name = data.get('last_name')
    username = data.get('username')
    email = data.get('email')
    password = data.get('password')
    confirm_password = data.get('confirm_password')
    phone_number = data.get('phone_number')
    age = data.get('age')

    if not all([first_name, last_name, username, email, password, confirm_password, phone_number, age]):
        return jsonify({'error': 'All fields are required'}), 400

    if password != confirm_password:
        return jsonify({'error': 'Passwords do not match'}), 400

    user = User.query.filter_by(username=username).first()
    if user:
        return jsonify({'error': 'Username already exists'}), 400

    user = User.query.filter_by(email=email).first()
    if user:
        return jsonify({'error': 'Email already registered'}), 400

    new_user = User(
        first_name=first_name,
        last_name=last_name,
        username=username,
        email=email,
        phone_number=phone_number,
        age=age
    )
    new_user.set_password(password)

    db.session.add(new_user)
    db.session.commit()

    return jsonify({'message': 'User registered successfully'}), 201
