# SANTE PRO




### Fonctionnalités

1. Inscription des utilisateurs : Enregistrement de nouveaux utilisateurs avec un email et un mot de passe.
2. Connexion des utilisateurs : Authentification des utilisateurs enregistrés en générant un token JWT.
3. Validation JWT : Les routes protégées peuvent être accédées uniquement avec un JWT valide.

You are also able to undo a migration by running

```sh
$ pipenv run downgrade
```

### Technologies utilisées


- Supabase : Pour la gestion de l'authentification et de la base de données.
- Flask : Framework web utilisé pour le backend.
- JWT (JSON Web Tokens) : Pour la création de tokens d'authentification.
- CORS : Configuration de Cross-Origin Resource Sharing pour permettre des requêtes sécurisées à partir de différents domaines.




### Installation
1. Clonez ce dépôt :
    https://github.com/brainmachineconsensus/santeprobackend.git
    cd santeprobackend

2. Créez un environnement virtuel et l'Activez:

```sh
$ python3 -m venv env
$ source env/bin/activate

```

3. Installez les dépendances :

```sh
$ pip install -r requirements.txt

```

4. Créez un fichier .env avec vos clés Supabase et JWT (ou configurez-les dans votre code)

### Lancement de l'application

1. Exécutez le serveur
```sh
$ python3 app.py
```
2. L'API sera disponible à l'adresse : http://localhost:5000