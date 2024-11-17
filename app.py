from flask import Flask, request, jsonify
import os
from dotenv import load_dotenv
import jwt
import bcrypt
from datetime import datetime, timedelta
from flask_cors import CORS
from pymongo import MongoClient

# Charger les variables d'environnement à partir de .env
load_dotenv()

# Configuration MongoDB
MONGODB_URI = os.getenv('MONGODB_URI')
SECRET_KEY = os.getenv('SECRET_KEY', 'your_jwt_secret_key')

# Connecter à MongoDB
client = MongoClient(MONGODB_URI)
db = client['SantePro']  # Nom de la base de données
users_collection = db['users']  # Nom de la collection

app = Flask(__name__)
CORS(app)  # Autoriser toutes les requêtes CORS par défaut

# Génération d'un token JWT
def generate_jwt(user_email, nom, prenom):
    expiration = datetime.utcnow() + timedelta(hours=24)  # Expiration dans 24 heures
    token = jwt.encode({
        'email': user_email,
        'nom': nom,
        'prenom': prenom,
        'exp': expiration
    }, SECRET_KEY, algorithm='HS256')
    return token

# Vérification d'un token JWT
def verify_jwt(token):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=['HS256'])
        return payload['email'], payload['nom'], payload['prenom']
    except jwt.ExpiredSignatureError:
        return None  # Token expiré
    except jwt.InvalidTokenError:
        return None  # Token invalide

# Route d'accueil (GET /)
@app.route('/', methods=['GET'])
def index():
    return jsonify({"message": "Bienvenue sur l'API Santé Pro"}), 200

# Route d'inscription (Sign Up)
@app.route('/signup', methods=['POST'])
def signup():
    data = request.get_json()
    email = data.get('email')
    password = data.get('password')
    nom = data.get('nom')
    prenom = data.get('prenom')

    if not email or not password or not nom or not prenom:
        return jsonify({'error': 'Nom, prénom, email et mot de passe sont requis'}), 400

    # Hacher le mot de passe
    hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())

    # Vérifier si l'utilisateur existe déjà
    if users_collection.find_one({"email": email}):
        return jsonify({'error': 'Un utilisateur avec cet email existe déjà'}), 409

    # Créer un nouvel utilisateur
    user = {
        'email': email,
        'password': hashed_password.decode('utf-8'),
        'nom': nom,
        'prenom': prenom
    }
    users_collection.insert_one(user)

    # Générer un token JWT
    token = generate_jwt(email, nom, prenom)
    return jsonify({"message": "User created successfully", "token": token}), 200

# Route de connexion (Sign In)
@app.route('/signin', methods=['POST'])
def signin():
    data = request.get_json()
    email = data.get('email')
    password = data.get('password')

    if not email or not password:
        return jsonify({'error': 'Email et mot de passe sont requis'}), 400

    # Vérifier si l'utilisateur existe et récupérer ses informations
    user = users_collection.find_one({"email": email})
    if not user or not bcrypt.checkpw(password.encode('utf-8'), user['password'].encode('utf-8')):
        return jsonify({'error': 'Email ou mot de passe incorrect'}), 401

    # Générer un token JWT
    token = generate_jwt(email, user['nom'], user['prenom'])
    return jsonify({"message": "Login successful", "token": token}), 200

if __name__ == '__main__':
    app.run(debug=True)
