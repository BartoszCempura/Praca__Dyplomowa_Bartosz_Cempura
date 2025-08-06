## to jest główny plik inicjalizujący aplikację Flask

from flask import Flask, app
import os
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from flask_jwt_extended import JWTManager
from datetime import timedelta

db = SQLAlchemy()
jwt = JWTManager() 

def create_app():
    
    app = Flask(__name__) ## inicjalizujemy aplikacje Flask
    
    secret_key = os.environ.get('SECRET_KEY') ## pobieramy zmienną środowiskową SECRET_KEY - nie podajemy jej bezpośrednio w kodzie
    # jest to klucz używany do podpisywania sesji i innych danych w aplikacji Flask
    # jest to ważne dla bezpieczeństwa aplikacji, ponieważ pozwala na weryfikację integralności danych
    # i zapobiega atakom typu tampering (manipulacja danymi)
    jwt_secret_key = os.environ.get('JWT_SECRET_KEY') ## pobieramy zmienną środowiskową JWT_SECRET_KEY - nie podajemy jej bezpośrednio w kodzie
    # jest to klucz używany do podpisywania tokenów JWT (JSON Web Tokens) w aplikacji Flask
    # jest to ważne dla bezpieczeństwa aplikacji, ponieważ pozwala na weryfikację integralności tokenów
    # i zapobiega atakom typu tampering (manipulacja tokenami)
    database_url = os.environ.get('DATABASE_URL') ## pobieramy zmienną środowiskową DATABASE_URL - nie podajemy jej bezpośrednio w kodzie
     # DATABASE_URL to zmienna środowiskowa zawierająca adres URL bazy danych, której aplikacja będzie używać
    # jest to ważne dla aplikacji, ponieważ pozwala na połączenie się z bazą danych i wykonywanie operacji na niej

    if not secret_key or not database_url or not jwt_secret_key:
        raise RuntimeError("Environment variables SECRET_KEY, JWT_SECRET_KEY and DATABASE_URL must be set")

    app.config['SECRET_KEY'] = secret_key
    app.config['JWT_SECRET_KEY'] = jwt_secret_key
    app.config['SQLALCHEMY_DATABASE_URI'] = database_url
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False ## wyłączamy sygnały z SQLAlchemy, takie jak model modified - lepsza wydajność
    app.config['JWT_TOKEN_LOCATION'] = ['headers'] ## ustawiamy lokalizację tokenów JWT - access w nagłówkach a refresh w ciasteczkach http
    app.config['JWT_ACCESS_TOKEN_EXPIRES'] = timedelta(minutes=15)
    app.config['JWT_REFRESH_TOKEN_EXPIRES'] = timedelta(days=30)


    db.init_app(app) ## inicjalizujemy bazę danych z aplikacją Flask
    jwt.init_app(app) ## inicjalizujemy JWTManager z aplikacją Flask
    CORS(app) ## włączamy CORS, aby aplikacja mogła obsługiwać żądania z innych domen

    from .auth import auth_bp ## importujemy moduł auth, który będzie zawierał endpointy związane z logowaniem i uwierzytelnianiem
    app.register_blueprint(auth_bp) 
    from .utils import utils_bp ## importujemy moduł utils, który będzie zawierał endpointy związane z innymi funkcjonalnościami aplikacji
    app.register_blueprint(utils_bp) 
    from .user_management import user_management_bp ## importujemy moduł user_management, który będzie zawierał endpointy związane z zarządzaniem kontem i adresami użytkownika
    app.register_blueprint(user_management_bp)
    from .catalog import catalog_bp ## importujemy moduł catalog, który będzie zawierał endpointy związane z katalogiem produktów
    app.register_blueprint(catalog_bp)
    from .commerce import commerce_bp ## importujemy moduł catalog, który będzie zawierał endpointy związane z katalogiem produktów
    app.register_blueprint(commerce_bp) 

    with app.app_context():
       from . import models ## importujemy modele z pliku models.py, aby były dostępne w kontekście aplikacji
       db.create_all() ## tworzymy wszystkie tabele w bazie danych, jeśli nie istnieją

    return app ## zwracamy aplikację Flask

