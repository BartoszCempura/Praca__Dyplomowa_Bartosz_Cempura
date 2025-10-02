## tutaj będziemy endpointy powiązane z logowaniemi uywierzytelnianiem
## trzeba sprawdzić jak to będzie działało z tokenami
from flask import Blueprint, request, jsonify
from backend import db
from backend.models import User
from flask_jwt_extended import create_access_token, create_refresh_token, get_jwt_identity, jwt_required

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

        return jsonify({
            'message': 'Login successful',
            'access_token': access_token,
            'refresh_token': refresh_token,
            'user': user.to_json()
        }), 200
        
    except Exception as e:
        print(f"[ERROR]: {str(e)}")
        return jsonify({'error': 'Internal server error'}), 500
    
    
@auth_bp.route("/refresh", methods=["POST"])
@jwt_required(refresh=True)
def refresh():

    """-------------------------------Endpoint wywoływany przez frontend w celu odnowienia Access token-------------------------------"""

    identity = get_jwt_identity()
    access_token = create_access_token(identity=identity)
    return jsonify(access_token=access_token)



@auth_bp.route('/logout', methods=['POST'])
@jwt_required()
def logout():

    """-------------------------------Potwierdzenie czy token jest wystawiony na konto użytkownika-------------------------------"""

    try:
        # Frontend usówa token z localStorage
        current_user_id = get_jwt_identity()
        
        return jsonify({
            'message': 'Logout successful',
            'user_id': current_user_id
        }), 200
          
    except Exception as e:
        print(f"[ERROR]: {str(e)}")
        return jsonify({'error': 'Logout failed'}), 500
    
    

