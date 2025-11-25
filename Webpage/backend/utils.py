## tutaj będziemy deklarowac endpointy - czyli co się wyświetla nam na 

from flask import Blueprint, jsonify
from functools import wraps
from flask_jwt_extended import get_jwt_identity
from datetime import datetime


utils_bp = Blueprint('utils', __name__, url_prefix='/api/utils')

""" Endpoint do sprawdzenia stanu aplikacji - czy działa poprawnie """

@utils_bp.route('/health', methods=['GET'])
def health_check():
    return {'status': 'healthy'}, 200

""" _____________________________________________________________________________________________________________________"""

## Dekorator do sprawdzania roli użytkownika
## Używany do zabezpieczenia endpointów, które powinny być dostępne tylko dla użytkowników o danej roli
def role_required(required_role):
    from backend.models import User
    def wrapper(fn):
        @wraps(fn)
        def decorator(*args, **kwargs):
            user_id = get_jwt_identity()
            user = User.query.get(user_id)
            if user.role != required_role:
                return jsonify({"error": "Forbidden"}), 403
            return fn(*args, **kwargs)
        return decorator
    return wrapper


def str_date(date):
    try:
        return datetime.strptime(date, '%Y-%m-%d')
    except ValueError:
        return None
    

def _money(value):

        """ 
        Funkcja pomocnicza, która zwraca wartość zaokrągloną 
        do dwóch miejsc po przecinku jako float.
        """
        return float(round(value, 2))