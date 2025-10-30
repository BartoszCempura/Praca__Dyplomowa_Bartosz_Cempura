## tutaj będziemy endpointy powiązane z logowaniemi uywierzytelnianiem
## trzeba sprawdzić jak to będzie działało z tokenami
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
            return jsonify({'error': 'Login and password are required'}), 400
        
        # Find user by login
        user = User.query.filter_by(login=data['login']).first()
        
        if not user or not user.check_password(data['password']):
            return jsonify({'error': 'Invalid credentials'}), 401
        
        access_token = create_access_token(identity=str(user.id)) # Tworzymy token JWT dla użytkownika
        refresh_token = create_refresh_token(identity=str(user.id)) # Tworzymy token odświeżający dla użytkownika

        response = jsonify({
            'message': 'Login successful',
            'access_token': access_token,
        })
        set_refresh_cookies(response, refresh_token)
        print("✅ refresh cookie ustawione")
        return response, 200
        
    except Exception as e:
        print(f"[ERROR]: {str(e)}")
        return jsonify({'error': 'Internal server error'}), 500
    
    
@auth_bp.route("/refresh", methods=["POST"])
@jwt_required(refresh=True)
def refresh():
    identity = get_jwt_identity()
    print("Refresh cookie received, identity:", identity)
    if not identity:
        print("JWT error - no identity!")
    access_token = create_access_token(identity=identity)
    return jsonify(access_token=access_token), 200



@auth_bp.route('/logout', methods=['POST'])
def logout():

    """-------------------------------Potwierdzenie czy token jest wystawiony na konto użytkownika-------------------------------"""

    try:
        # Frontend usówa token z sessionStorage
        response = jsonify({'message': 'Logout successful'})
        unset_jwt_cookies(response)  # Usuwamy ciasteczka z refresh tokenem
        
        return response, 200
          
    except Exception as e:
        print(f"[ERROR]: {str(e)}")
        return jsonify({'error': 'Logout failed'}), 500
    
    

