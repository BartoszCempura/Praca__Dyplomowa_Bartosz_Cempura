## Przechowujemy tutaj endpointy powiązane z schematem user_management

from flask import Blueprint, request, jsonify
from backend import db
from backend.models import User, UserAddress, AddressType
from flask_jwt_extended import get_jwt_identity, jwt_required
from backend.utils import role_required

user_management_bp = Blueprint('user_management', __name__, url_prefix='/api/user_management')

## ###################################################################### Użytkownicy ######################################################################

@user_management_bp.route('/user', methods=['POST']) ## used - createAccountPage
def register():

    """-------------------------------Tworzenie konta nowego użytkownika-------------------------------"""

    try:
        data = request.get_json()
        
        # Sprawdzenie czy mamy wszystkie wymagane pola
        required_fields = ['login', 'password', 'first_name', 'last_name', 'email', 'phone_number']
        for field in required_fields:
            if not data.get(field):
                return jsonify({'error': f'Pole {field} jest wymagane'}), 400

        # Sprawdzenie formatu email
        if not User.validate_email(data['email']):
            return jsonify({'error': 'Nieprawidłowy format adresu email'}), 400

        # Sprawdzenie formatu numeru telefonu
        if not User.validate_phone(data['phone_number']):
            return jsonify({'error': 'Nieprawidłowy format numeru telefonu'}), 400

        # Sprawdzenie czy login, email lub numer telefonu są już w bazie danych
        if User.query.filter_by(login=data['login']).first(): # automatycznie połaczone do modelu. Zapytanie do bazy na bazie modelu User
            return jsonify({'error': 'Login już istnieje'}), 409

        if User.query.filter_by(email=data['email']).first():
            return jsonify({'error': 'Email już istnieje'}), 409

        if User.query.filter_by(phone_number=data['phone_number']).first():
            return jsonify({'error': 'Numer telefonu już istnieje'}), 409

        # do zmiennej przypisujemy obiekt User z danymi z requesta
        user = User(
            login=data['login'],
            first_name=data['first_name'],
            last_name=data['last_name'],
            email=data['email'],
            phone_number=data['phone_number']
        )
        user.set_password(data['password']) # i hashujemy hasło
        
        db.session.add(user)
        db.session.commit()
        
        return jsonify({
            'message': f'Konto użytkownika "{user.login}" zostało utworzone pomyślnie.'
        }), 201
        
    except Exception as e:
        db.session.rollback()
        print(f"[ERROR]: {str(e)}")
        return jsonify({'error': 'Internal server error'}), 500
    
@user_management_bp.route('/user', methods=['PUT']) ## used - userProfile
@jwt_required()
def change_password():

    """-------------------------------Zmiana hasła przez użytkownika-------------------------------"""

    # można dodać jeszce możliwośc zmiany pozostałych danych użytkownika, ale to już nie jest priorytetem
    data = request.get_json()
    current_user_id = get_jwt_identity()
    user = User.query.filter_by(id=current_user_id).first()

    if not user:
        return jsonify({'error': 'Nie znaleziono użytkownika'}), 404
 
    if not data.get('old_password') or not data.get('new_password'):
        return jsonify({'error': 'Oba pola są wymagane'}), 400

    if not user.check_password(data['old_password']):
        return jsonify({'error': 'Stare hasło jest nieprawidłowe'}), 401
       
    if data.get('old_password') == data.get('new_password'):
        return jsonify({'error': 'Nowe hasło musi różnić się od starego hasła'}), 400

    user.set_password(data['new_password'])
    db.session.commit()

    return jsonify({'message': 'Hasło zostało zmienione pomyślnie'}), 200

@user_management_bp.route('/user', methods=['GET']) ## used - userProfile
@jwt_required()
def get_current_user():

    """-------------------------------Pobranie danych aktualnego użytkownika-------------------------------"""

    try:
        current_user_id = get_jwt_identity()
        user = User.query.get(current_user_id)

        if not user:
            return jsonify({'error': 'Nie znaleziono użytkownika'}), 404

        return jsonify(user.to_json()), 200

    except Exception as e:
        print(f"[ERROR]: {str(e)}")
        return jsonify({'error': 'Internal server error'}), 500
    
@user_management_bp.route('/user', methods=['DELETE']) ## used - userProfile
@jwt_required()
def delete_user():

    """-------------------------------Usunięcie konta użytkownika przez użytkownika-------------------------------"""

    try:

        data = request.get_json()
        current_user_id = get_jwt_identity()
        user = User.query.filter_by(id=current_user_id).first()

        if not user:
            return jsonify({'error': 'Nie znaleziono użytkownika'}), 404
        
        if not data.get('password'):
            return jsonify({'error': 'Wymagane podanie hasła'}), 400
        
        if not user.check_password(data['password']):
            return jsonify({'error': 'Nieprawidłowe hasło'}), 401

        # Przechowujemy informacje o użytkowniku przed usunięciem
        # aby móc zwrócić ją w odpowiedzi
        user_info = {
            'login': user.login
        }
        
        db.session.delete(user)
        db.session.commit()
        
        return jsonify({
            'message': f'User {user_info} deleted successfully'
        }), 200
        
    except Exception as e:
        db.session.rollback()
        print(f"[ERROR]: {str(e)}")
        return jsonify({'error': 'Internal server error'}), 500
    

## ###################################################################### Adresy dostawy ######################################################################


@user_management_bp.route('/addresses', methods=['POST']) ## used - daneDoZamowien
@jwt_required()
def register_address():

    """-------------------------------Rejestracja nowego adresu-------------------------------"""

    try:
        current_user_id = get_jwt_identity()
        data = request.get_json()

        required_fields = ['street_name', 'building_number', 'zip_code', 'city']

        field_labels = {
            'street_name': 'Nazwa ulicy',
            'building_number': 'Numer budynku',
            'zip_code': 'Kod pocztowy',
            'city': 'Miasto'
        }
        for field in required_fields:
            if not data.get(field):
                return jsonify({'error': f'Pole "{field_labels[field]}" jest wymagane'}), 400

        if not UserAddress.validate_zip_code(data['zip_code']): 
            return jsonify({'error': 'Nieprawidłowy format kodu pocztowego'}), 400
        
        nip = data.get('nip')

        if nip and not UserAddress.validate_nip(nip): # sprawdzamy czy nip w ogóle został podany i jak tak to go walidujemy
            return jsonify({'error': 'Nieprawidłowy format NIP'}), 400
        
        if nip:
            exists = UserAddress.query.filter_by(nip=nip).first()
            if exists:
                return jsonify({'error': 'Adres z takim NIP już istnieje'}), 400

        type_str = data.get('type', 'Shipping')  # default 'shipping', dodatkowe wyłapanie błedu aby ten się w ogóle wyświetlił
        try:
            address_type = AddressType(type_str)
        except ValueError:
            return jsonify({'error': f'Nieprawidłowy typ adresu: {type_str}'}), 400
        # w frontendzie nie ma możliwości dodania ponownie Default więc ten błąd raczej się nie pojawi, ale dla pewności lepiej go obsłużyć, żeby nie było sytuacji że mamy dwa adresy default
        if address_type == AddressType.Default:
            if_default_check = UserAddress.query.filter(
                UserAddress.type == 'Default',
                UserAddress.user_id == current_user_id
            ).first()
            if if_default_check:
                return jsonify({'error': 'Domyślny adres już istnieje'}), 400

        # Create address instance
        address = UserAddress(
            user_id=current_user_id,
            title=data.get('title'),
            company_name=data.get('company_name'),
            first_name=data.get('first_name'),
            last_name=data.get('last_name'),
            nip=data.get('nip') or None,
            street_name=data['street_name'],
            building_number=data['building_number'],
            flat_number=data.get('flat_number') or None,
            zip_code=data['zip_code'],
            city=data['city'],
            type=address_type.value # używamy .value aby uzyskać wartość enum
        )

        db.session.add(address)
        db.session.commit()

        return jsonify({'message': 'Adres został pomyślnie zarejestrowany'}), 200

    except Exception as e:
        db.session.rollback()
        print(f"[ERROR]: {str(e)}")
        return jsonify({'error': f'Internal server error: {str(e)}'}), 500
    
@user_management_bp.route('/addresses', methods=['GET']) ## used - daneDoZamowien, cartPartTwo
@jwt_required()
def get_all_addresses():

    """-------------------------------Pobranie wszystkich adresów użytkownika-------------------------------"""

    try:
        current_user_id = get_jwt_identity()
        addresses = UserAddress.query.filter_by(user_id=current_user_id).order_by(UserAddress.id.asc()).all()

        if not addresses:
            return '', 200

        return jsonify([address.to_json() for address in addresses]), 200

    except Exception as e:
        print(f"[ERROR]: {str(e)}")
        return jsonify({'error': 'Internal server error'}), 500

@user_management_bp.route('/addresses/<int:address_id>/type', methods=['PATCH']) ## used - daneDoZamowien - ustawianie domyślnego adresu - nie pełne zastosowanie - powinno być dla dowolnej zmiany
@jwt_required()
def update_address_type(address_id):

    """-------------------------------Zmiana typu adresu z wysyłkowego na domyślny-------------------------------"""
    
    try:
        current_user_id = get_jwt_identity()
        data = request.get_json()

        # szukam adresu użytkownika
        address = UserAddress.query.filter_by(
            id=address_id,
            user_id=current_user_id
        ).first()

        if not address:
            return jsonify({'error': 'Adres nie został znaleziony'}), 404

        type_str = data.get('type')
        if not type_str:
            return jsonify({'error': 'Pole "type" jest wymagane'}), 400

        # sprawdzam czy podano prawidłowy
        try:
            address_type = AddressType(type_str)
        except ValueError:
            return jsonify({'error': f'Nieprawidłowy typ adresu: {type_str}'}), 400

        # zmieniam poprzedni default na shipping
        if address_type == AddressType.Default:
            current_default = UserAddress.query.filter(
                UserAddress.user_id == current_user_id,
                UserAddress.type == 'Default',
                UserAddress.id != address_id
            ).first()

            if current_default:
                current_default.type = 'Shipping'

        address.type = address_type.value
        db.session.commit()

        return jsonify({'message': 'Typ adresu został zaktualizowany'}), 200

    except Exception as e:
        db.session.rollback()
        print(f"[ERROR]: {str(e)}")
        return jsonify({'error': f'Internal server error: {str(e)}'}), 500    

@user_management_bp.route('/addresses/<int:address_id>', methods=['DELETE']) ## used - daneDoZamowien - addressCard
@jwt_required()
def delete_address(address_id):

    """-------------------------------Usunięcie adresu użytkownika przez użytkownika-------------------------------"""

    try:

        current_user_id = get_jwt_identity()

        address = UserAddress.query.filter(
            UserAddress.id == address_id,
            UserAddress.user_id == current_user_id
        ).first() # po stronie frontend numer ID adresu musi być przekazany do przycisku x

        if not address:
            return jsonify({'error': 'Brak takiego adresu'}), 404

        db.session.delete(address)
        db.session.commit()

        return jsonify({'message': 'Adres został pomyślnie usunięty'}), 200

    except Exception as e:
        db.session.rollback()
        print(f"[ERROR]: {str(e)}")
        return jsonify({'error': f'Internal server error: {str(e)}'}), 500
    

###################################################### endpointy dla administaratora ###########################################################


@user_management_bp.route('/admin/user/<int:user_id>', methods=['DELETE'])
@jwt_required()
@role_required('admin')
def delete_user_by_id(user_id):

    """-------------------------------Usunięcie konta użytkownika przez administratora-------------------------------"""
# trzeba tutaj dodać sprawdzenie czy użytkownik jest administratorem !!
    try:
        user = User.query.get(user_id)
        data = request.get_json()

        if not user:
            return jsonify({'error': 'Nie znaleziono użytkownika'}), 404
        
        if not data.get('password'):
            return jsonify({'error': 'Wymagane podanie hasła'}), 400
        
        if not user.check_password(data['password']):
            return jsonify({'error': 'Nieprawidłowe hasło'}), 401
        
        # Przechowujemy informacje o użytkowniku przed usunięciem
        # aby móc zwrócić ją w odpowiedzi
        user_info = {
            'login': user.login,
        }
        
        db.session.delete(user)
        db.session.commit()
        
        return jsonify({'message': f'Użytkownik {user_info["login"]} został pomyślnie usunięty'}), 200
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': 'Internal server error'}), 500
    
@user_management_bp.route('/admin/user', methods=['GET'])
@jwt_required()
@role_required('admin')
def get_all_users():

    """-------------------------------Pobranie wszystkich użytkowników przez administratora-------------------------------"""

    try:
        users = User.query.all()        
        return jsonify([user.to_json() for user in users]), 200
    except Exception as e:
        print(f"[ERROR]: {str(e)}")
        return jsonify({'error': 'Internal server error'}), 500
    
## TODO: trzeba dodać endpoint dla admina pozwalający na nadawanie admina innym użytkownikom, albo inny statuskonta dla innych zadań np dodawania produktów itp