## tutaj będziemy endpointy powiązane z logowaniemi uywierzytelnianiem
from flask import Blueprint, request, jsonify
from backend import db
from backend.models import User
from flask_jwt_extended import create_access_token, create_refresh_token, set_refresh_cookies, unset_jwt_cookies, get_jwt_identity, jwt_required

auth_bp = Blueprint('auth', __name__, url_prefix='/api/auth')


@auth_bp.route('/login', methods=['POST'])
def login():

    """-------------------------------Weryfikacja użytkownika i generowanie tokenu JWT-------------------------------"""

    try:
        data = request.get_json()
        
        if not data.get('login') or not data.get('password'):
            return jsonify({'error': 'Podaj login i hasło'}), 400
        
        user = User.query.filter_by(login=data['login']).first()
        if not user :
            return jsonify({'error': 'Brak użytkownika o tym loginie'}), 401
               
        if not user or not user.check_password(data['password']):
            return jsonify({'error': 'Hasło jest niepoprawne'}), 401

        access_token = create_access_token(identity=str(user.id)) # Tworzymy token JWT dla użytkownika
        refresh_token = create_refresh_token(identity=str(user.id)) # Tworzymy token odświeżający dla użytkownika

        response = jsonify({
            'access_token': access_token
        })
        set_refresh_cookies(response, refresh_token) # tworzymy cookie z tokenem odświeżającym
        return response, 200
        
    except Exception as e:
        print(f"[ERROR]: {str(e)}")
        return jsonify({'error': 'Internal server error'}), 500
    
    
@auth_bp.route("/refresh", methods=["POST"])
@jwt_required(refresh=True)  # musi być refresh w nagłówku
def refresh():

    """-------------------------------Odświeżanie tokenu JWT-------------------------------"""

    identity = get_jwt_identity()
    access_token = create_access_token(identity=identity) # Tworzymy nowy token dostępu
    return jsonify(access_token=access_token), 200



@auth_bp.route('/logout', methods=['POST'])
def logout():

    """-------------------------------Przy Logout usuwamy cookie z refresh tokenem-------------------------------"""

    try:
        response = jsonify({})
        unset_jwt_cookies(response)  # Usuwamy ciasteczka z refresh tokenem      
        return response, 200
          
    except Exception as e:
        print(f"[ERROR]: {str(e)}")
        return jsonify({'error': 'Internal server error'}), 500
    
    

