from flask import Blueprint, request, jsonify
from backend import db
from backend.models import DeliveryMethods, PaymentMethods, Carts, CartProducts, Products, ProductPromotions, Promotions
from flask_jwt_extended import get_jwt_identity, jwt_required
from backend.utils import role_required
from sqlalchemy import func

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
            db.func.sum(CartProducts.quantity * CartProducts.unit_price_with_discount)
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
            db.func.sum(CartProducts.quantity * CartProducts.unit_price_with_discount)
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

