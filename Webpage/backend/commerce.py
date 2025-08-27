from flask import Blueprint, request, jsonify
from backend import db
from backend.models import DeliveryMethods, PaymentMethods, Carts, CartProducts, Products, Transactions, TransactionStatus, TransactionProducts
from flask_jwt_extended import get_jwt_identity, jwt_required
from backend.utils import role_required
from sqlalchemy import func
from decimal import Decimal

commerce_bp = Blueprint('commerce', __name__, url_prefix='/api/commerce')

## ###################################################################### Metody dostawy ######################################################################

@commerce_bp.route('/add_delivery_method', methods=['POST'])
@jwt_required()
@role_required('admin')
def add_delivery_method():

    """-------------------------------Dodanie metody dostawy-------------------------------"""

    try:
        
        data = request.get_json()

        if not data.get('name'):
            return jsonify({'error': 'Name is required'}), 400
        
        if DeliveryMethods.query.filter_by(name=data.get('name')).first():
            return jsonify({"error": "Delivery method with this name already exists"}), 409

        new_delivery_method = DeliveryMethods(
            name=data.get('name'),
            fee=data.get('fee', 0.00),
            estimated_delivery_days=data.get('estimated_delivery_days', 3),
            is_active=data.get('is_active', True)
        )

        db.session.add(new_delivery_method)
        db.session.commit()

        return jsonify({'message': 'Delivery method added successfully',
                        'Delivery method': new_delivery_method.to_json()
                        }), 201

    except Exception as e:
            db.session.rollback()
            print(f"[ERROR]: {str(e)}")
            return jsonify({'error': 'Internal server error'}), 500
    

    
@commerce_bp.route('/get_all_delivery_methods', methods=['GET'])
@jwt_required()
@role_required('admin')
def get_all_delivery_methods():
     
    """-------------------------------Pobiera wszystkie wprowadzone Delivery methods-------------------------------"""

    all_delivery_methods = DeliveryMethods.query.all()
    return jsonify([method.to_json() for method in all_delivery_methods]), 200



@commerce_bp.route('/get_all_active_delivery_methods', methods=['GET'])
def get_all_active_delivery_methods():

    """-------------------------------Pobiera aktywne Delivery methods-------------------------------"""

    active_methods = DeliveryMethods.query.filter_by(is_active=True).all()

    return jsonify([method.to_json() for method in active_methods]), 200



@commerce_bp.route('/modify_delivery_method/<int:delivery_id>', methods=['PUT'])
@jwt_required()
@role_required('admin')
def modify_delivery_method(delivery_id):

    """-------------------------------modyfikujemy delivery method-------------------------------"""

    try:

        data = request.get_json() 
        delivery = DeliveryMethods.query.get(delivery_id)

        if not delivery:
            return jsonify({'error': 'There is no delivery method with such id'}), 404
        
        delivery.name = data.get('name', delivery.name)
        delivery.fee = data.get('fee', delivery.fee)
        delivery.estimated_delivery_days = data.get('estimated_delivery_days', delivery.estimated_delivery_days)
        delivery.is_active = data.get('is_active', delivery.is_active)

        db.session.commit()

        return jsonify({
            "message": "Delivery method data modified successfully",
            "product": delivery.to_json()
        }), 200

    except Exception as e:
        db.session.rollback()
        print(f"[ERROR]: {str(e)}")
        return jsonify({'error': 'Internal server error'}), 500
    
## brak metody usówanie ze względów bezpieczeństwa. Metodę można usunąć zpoziopmu bazy danych


## ###################################################################### Metody płatnośic ######################################################################


@commerce_bp.route('/add_payment_method', methods=['POST'])
@jwt_required()
@role_required('admin')
def add_payment_method():

    """-------------------------------Dodanie metody płatności-------------------------------"""

    try:
        
        data = request.get_json()

        if not data.get('name'):
            return jsonify({'error': 'Name is required'}), 400
        
        if PaymentMethods.query.filter_by(name=data.get('name')).first():
            return jsonify({"error": "Delivery method with this name already exists"}), 409

        new_payment_method = PaymentMethods(
            name=data.get('name'),
            image=data.get('image'),
            fee=data.get('fee', 0.00),
            is_active=data.get('is_active', True)
        )

        db.session.add(new_payment_method)
        db.session.commit()

        return jsonify({'message': 'Payment method added successfully',
                        'Payment method': new_payment_method.to_json()
                        }), 201

    except Exception as e:
            db.session.rollback()
            print(f"[ERROR]: {str(e)}")
            return jsonify({'error': 'Internal server error'}), 500
    

    
@commerce_bp.route('/get_all_payment_methods', methods=['GET'])
@jwt_required()
@role_required('admin')
def get_all_payment_methods():
     
    """-------------------------------Pobiera wszystkie wprowadzone payment methods-------------------------------"""

    all_payment_methods = PaymentMethods.query.all()
    return jsonify([method.to_json() for method in all_payment_methods]), 200



@commerce_bp.route('/get_all_active_payment_methods', methods=['GET'])
def get_all_active_payment_methods():

    """-------------------------------Pobiera aktywne payment methods-------------------------------"""

    active_methods = PaymentMethods.query.filter_by(is_active=True).all()

    return jsonify([method.to_json() for method in active_methods]), 200



@commerce_bp.route('/modify_payment_method/<int:payment_id>', methods=['PUT'])
@jwt_required()
@role_required('admin')
def modify_payment_method(payment_id):

    """-------------------------------Modyfikujemy payment method-------------------------------"""

    try:

        data = request.get_json() 
        payment = PaymentMethods.query.get(payment_id)

        if not payment:
            return jsonify({'error': 'There is no payment method with such id'}), 404
        
        payment.name = data.get('name', payment.name)
        payment.image = data.get('image', payment.image)
        payment.fee = data.get('fee', payment.fee)
        payment.is_active = data.get('is_active', payment.is_active)

        db.session.commit()

        return jsonify({
            "message": "Payment method data modified successfully",
            "product": payment.to_json()
        }), 200

    except Exception as e:
        db.session.rollback()
        print(f"[ERROR]: {str(e)}")
        return jsonify({'error': 'Internal server error'}), 500
    
    
## brak metody usówanie ze względów spójności danych o transakcjach. Metodę można usunąć z poziopu bazy danych


## ###################################################################### Koszyk i produkty w koszyku ######################################################################

@commerce_bp.route('/add_product_to_cart', methods=['POST'])
@jwt_required()
def add_product_to_cart():

    """---------------------Dodanie produktu do koszyka użytkownika---------------------"""
## zastosowanie dla przycisku na liście produktów jako +1 oraz w samym koszyku przy + aby zwiększyć ilość lub pole textowe gdzie podaje ile
## dla przycisku "do koszyka"
    try:
        user_id = get_jwt_identity()
        data = request.get_json()
        quantity = data.get('quantity')
        product_id = data.get('product_id')

        if not product_id or not quantity:
            return jsonify({'error': 'Product ID and quantity are required'}), 400

        if CartProducts.validate_quantity(data.get('quantity')) is None:
            return jsonify({'error': 'Ilość musi być większa od 0'}), 400

        product = Products.query.get(product_id)
        if not product:
            return jsonify({'error': 'Product not found'}), 404
        
        if quantity > product.quantity:
            return jsonify({'error': 'Not enough stock available'}), 400

        cart = Carts.query.filter_by(user_id=user_id).first()
        if not cart:
            cart = Carts(
                user_id=user_id
            )
            db.session.add(cart)
            db.session.flush()  # potrzebne, by mieć cart.id

        product_in_cart = CartProducts.query.filter(
            CartProducts.cart_id == cart.id,
            CartProducts.product_id == product_id
        ).first()

        price_with_discount = product.price_including_promotion()

        if product_in_cart:
            product_in_cart.quantity += quantity
        else:
            new_product_in_cart = CartProducts(
                cart_id=cart.id,
                product_id=product_id,
                quantity=quantity,
                unit_price_with_discount=price_with_discount
            )
            db.session.add(new_product_in_cart)

        product.quantity -= quantity

        # Aktualizujemy łączny koszt koszyka
        cart.total_products_cost = db.session.query(
            func.coalesce(
            db.func.sum(CartProducts.quantity * CartProducts.unit_price_with_discount),
            Decimal("0.00")
            )
        ).filter_by(cart_id=cart.id).scalar()

        db.session.commit()

        return jsonify({'message': 'Product added to cart successfully'}), 201

    except Exception as e:
        db.session.rollback()
        print(f"[ERROR]: {str(e)}")
        return jsonify({'error': 'Internal server error'}), 500
    

@commerce_bp.route('/remove_product_from_cart', methods=['PUT'])
@jwt_required()
def remove_product_from_cart():

    """---------------------usówanie produktu do koszyka użytkownika---------------------"""

    try:
        user_id = get_jwt_identity()
        data = request.get_json()
        quantity = data.get('quantity')
        product_id = data.get('product_id')

        if not product_id or not quantity:
            return jsonify({'error': 'Product ID and quantity are required'}), 400

        if CartProducts.validate_quantity(data.get('quantity')) is None:
            return jsonify({'error': 'Ilość musi być większa od 0'}), 400

        product = Products.query.get(product_id)
        if not product:
            return jsonify({'error': 'Nie znaleziono produktu'}), 404
        

        cart = Carts.query.filter_by(user_id=user_id).first()
        if not cart:
            return jsonify({'error': 'Nie znaleziono koszyka'}), 404
        
        product_in_cart = CartProducts.query.filter(
            CartProducts.cart_id == cart.id,
            CartProducts.product_id == product_id
        ).first()

        if not product_in_cart:
            return jsonify({'error': 'Produkt nie znajduje się w koszyku'}), 404
        
        if quantity > product_in_cart.quantity:
            return jsonify({'error': 'Quantity to remove exceeds quantity in cart'}), 400
      
        product_in_cart.quantity -= quantity
        
        if product_in_cart.quantity == 0:
            db.session.delete(product_in_cart)

        product.quantity += quantity

        # Aktualizujemy łączny koszt koszyka
        cart.total_products_cost = db.session.query(
            func.coalesce(
            db.func.sum(CartProducts.quantity * CartProducts.unit_price_with_discount),
            Decimal("0.00")
            )
        ).filter_by(cart_id=cart.id).scalar()

        db.session.commit()

        return jsonify({'message': 'Product removed from cart successfully'}), 201

    except Exception as e:
        db.session.rollback()
        print(f"[ERROR]: {str(e)}")
        return jsonify({'error': 'Internal server error'}), 500
    

    
@commerce_bp.route('/get_cart', methods=['GET'])
@jwt_required()
def get_cart():

    """---------------------Pobranie informacji i zawartości koszyka---------------------"""

    try:
        user_id = get_jwt_identity()

        cart = Carts.query.filter_by(user_id=user_id).first()
        if not cart:
            return jsonify({'error': 'Nie znaleziono koszyka'}), 404

        products_in_cart = CartProducts.query.filter_by(cart_id=cart.id).all()

        if not products_in_cart:
            return jsonify({'message': 'Koszyk jest pusty'}), 200


        cart_data = {
            'total_products_cost': str(cart.total_products_cost),
            'products': [product.to_json() for product in products_in_cart]
        }

        return jsonify(cart_data), 200

    except Exception as e:
        print(f"[ERROR]: {str(e)}")
        return jsonify({'error': 'Internal server error'}), 500
    

## ###################################################################### Transakcje i produkty w nich ######################################################################

@commerce_bp.route('/closing_purchase', methods=['POST'])
@jwt_required()
def closing_purchase():

    """---------------------Zamknięcie zakupu---------------------"""

    try:
        user_id = get_jwt_identity()
        data = request.get_json()

        required_fields = ['billing_address_id', 'shipping_address_id', 'delivery_method_id', 'payment_method_id']
        for field in required_fields:
            if not data.get(field):
                return jsonify({'error': f'{field} is required'}), 400

        cart = Carts.query.filter_by(user_id=user_id).first()
        if not cart:
            return jsonify({'error': 'Nie znaleziono koszyka'}), 404

        if cart.total_products_cost == 0:
            return jsonify({'error': 'Koszyk jest pusty'}), 400

        delivery_method = DeliveryMethods.query.filter_by(id=data.get('delivery_method_id'), is_active=True).first()
        payment_method = PaymentMethods.query.filter_by(id=data.get('payment_method_id'), is_active=True).first()

        # Tworzenie nowej transakcji
        new_transaction = Transactions(
            user_id=user_id,
            total_transaction_value=cart.total_products_cost + delivery_method.fee + payment_method.fee,
            billing_address_id=data.get('billing_address_id'),
            shipping_address_id=data.get('shipping_address_id'),
            delivery_method_id=delivery_method.id,
            payment_method_id=payment_method.id,
            delivery_deadline=DeliveryMethods.delivery_date(delivery_method),
            notes=data.get('notes')
        )
        db.session.add(new_transaction)
        db.session.flush()  # potrzebne, by mieć transaction.id

        # Przeniesienie produktów z koszyka do transakcji
        cart_products = CartProducts.query.filter_by(cart_id=cart.id).all()
        for cart_product in cart_products:
            new_transaction_product = TransactionProducts(
                transaction_id=new_transaction.id,
                product_id=cart_product.product_id,
                quantity=cart_product.quantity,
                unit_price_with_discount=cart_product.unit_price_with_discount
            )
            db.session.add(new_transaction_product)

        # Usunięcie koszyka
        db.session.delete(cart)

        db.session.commit()

        return jsonify({'message': 'Zakup zakończony pomyślnie'}), 201

    except Exception as e:
        db.session.rollback()
        print(f"[ERROR]: {str(e)}")
        return jsonify({'error': 'Internal server error'}), 500
    

@commerce_bp.route('/update_transaction_status/<int:transaction_id>', methods=['PUT'])
@jwt_required()
@role_required('admin')
def modify_transaction_status(transaction_id):

    """-------------------------------Zmiana statusy transakcji-------------------------------"""

    try:
        # tutaj należało by dodać możliwośc logowania zmian w bazie dancyh ze względu na audyty i zasady RODO. Na tę chwile pomijamy ze względów czasowych
        data = request.get_json()
        new_status = data.get('status')
        new_notes = data.get('notes')
        transaction = Transactions.query.get(transaction_id)

        changes = []

        if new_status and new_status != transaction.status.value:
            changes.append(f"Status zmieniony z {transaction.status.value} na {new_status}")
            transaction.status = TransactionStatus(new_status)

            if transaction.status == TransactionStatus.Cancelled:

                products_associated_with_transaction = TransactionProducts.query.filter_by(transaction_id=transaction.id).all()
                for transaction_product in products_associated_with_transaction:
                    product = Products.query.get(transaction_product.product_id)
                    if product:
                        product.quantity += transaction_product.quantity  # zwracamy produkty na stan magazynowy

                db.session.delete(transaction)
                db.session.commit()
                return jsonify({'message': 'Transakcja anulowana i usunięta pomyślnie'}), 200

        if new_notes and new_notes != transaction.notes:
            changes.append("Dodano notatkę")
            transaction.notes += f" Admin: {new_notes}"

        if not changes:
            return jsonify({'error': 'Nie wprowadzono żadnych zmian'}), 409
        
        

        db.session.commit()

        return jsonify({
            "message": "Transaction data modified successfully",
            "changes": changes
        }), 200

    except Exception as e:
        db.session.rollback()
        print(f"[ERROR]: {str(e)}")
        return jsonify({'error': 'Internal server error'}), 500
    

@commerce_bp.route('/get_all_user_transactions', methods=['GET'])
@jwt_required()
def get_all_user_transactions():

    """-------------------------------Zwraca wszystkie transakcje użytkownika-------------------------------"""  

    try:

        user_id = get_jwt_identity()
        tranzacje = Transactions.query.filter_by(user_id=user_id).all()

        if not tranzacje:
            return jsonify({"error": "Brak transakcji dla konta użytkownika"}), 400

        response_data = []
        for tranzakcja in tranzacje:
            data = tranzakcja.to_user_view_json()
            produkty = TransactionProducts.query.filter_by(transaction_id=tranzakcja.id).all()
            data["producty"] = [p.to_user_view_json() for p in produkty]
            response_data.append(data)

        return jsonify(response_data), 200
        

    except Exception as e:
        print(f"[ERROR]: {str(e)}")
        return jsonify({'error': 'Internal server error'}), 500