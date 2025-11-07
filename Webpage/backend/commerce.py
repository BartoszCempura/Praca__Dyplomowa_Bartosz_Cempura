from flask import Blueprint, request, jsonify
from backend import db
from backend.models import DeliveryMethods, PaymentMethods, Carts, CartProducts, Products, Transactions, TransactionStatus, TransactionProducts, User, Wishlists, UserAddress
from flask_jwt_extended import get_jwt_identity, jwt_required
from backend.utils import role_required, str_date
from sqlalchemy import func
from decimal import Decimal

commerce_bp = Blueprint('commerce', __name__, url_prefix='/api/commerce')

## ###################################################################### Metody dostawy ######################################################################

@commerce_bp.route('/admin/delivery-methods', methods=['POST'])
@jwt_required()
@role_required('admin')
def add_delivery_method():

    """-------------------------------Dodanie metody dostawy przez administratora-------------------------------"""

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
    

    
@commerce_bp.route('/admin/delivery-methods', methods=['GET'])
@jwt_required()
@role_required('admin')
def get_all_delivery_methods():
     
    """-------------------------------Pobiera wszystkie wprowadzone Delivery methods dla administratora-------------------------------"""

    all_delivery_methods = DeliveryMethods.query.all()
    return jsonify([method.to_json() for method in all_delivery_methods]), 200



@commerce_bp.route('/delivery-methods', methods=['GET'])
def get_all_active_delivery_methods():

    """-------------------------------Pobiera aktywne Delivery methods dla procesu sprzedażowego-------------------------------"""

    active_methods = DeliveryMethods.query.filter_by(is_active=True).all()

    return jsonify([method.to_json() for method in active_methods]), 200



@commerce_bp.route('/admin/delivery-methods/<int:delivery_id>', methods=['PUT'])
@jwt_required()
@role_required('admin')
def modify_delivery_method(delivery_id):

    """-------------------------------modyfikujemy delivery method przez administratora-------------------------------"""

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


@commerce_bp.route('/admin/payment-methods', methods=['POST'])
@jwt_required()
@role_required('admin')
def add_payment_method():

    """-------------------------------Dodanie metody płatności przez administratora-------------------------------"""

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
    

    
@commerce_bp.route('/admin/payment-methods', methods=['GET'])
@jwt_required()
@role_required('admin')
def get_all_payment_methods():

    """-------------------------------Pobiera wszystkie wprowadzone payment methods dla administratora-------------------------------"""

    all_payment_methods = PaymentMethods.query.all()
    return jsonify([method.to_json() for method in all_payment_methods]), 200



@commerce_bp.route('/payment-methods', methods=['GET'])
def get_all_active_payment_methods():

    """-------------------------------Pobiera aktywne payment methods dla procesu zakupowego-------------------------------"""

    active_methods = PaymentMethods.query.filter_by(is_active=True).all()

    return jsonify([method.to_json() for method in active_methods]), 200



@commerce_bp.route('/admin/payment-methods/<int:payment_id>', methods=['PUT'])
@jwt_required()
@role_required('admin')
def modify_payment_method(payment_id):

    """-------------------------------Modyfikujemy payment method przez administratora------------------------------"""

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

"""
@commerce_bp.route('/carts', methods=['POST'])
@jwt_required()
def add_product_to_cart():

    try:
        user_id = get_jwt_identity()
        data = request.get_json()
        product_id = data.get('product_id')

        if not product_id:
            return jsonify({'error': 'ID produktu jest wymagane'}), 400

        product = Products.query.get(product_id)
        if not product:
            return jsonify({'error': 'Nie znaleziono produktu'}), 404

        if product.quantity <= 0:
            return jsonify({'error': 'Wyczerpano zapas produktu'}), 400

        # Znajdź lub utwórz koszyk użytkownika
        cart = Carts.query.filter_by(user_id=user_id).first()
        if not cart:
            cart = Carts(user_id=user_id)
            db.session.add(cart)
            db.session.flush()  # potrzebne, by mieć cart.id

        # Sprawdź, czy produkt jest już w koszyku
        product_in_cart = CartProducts.query.filter_by(
            cart_id=cart.id,
            product_id=product_id
        ).first()

        price_with_discount = product.price_including_promotion()

        if product_in_cart:
            # Zwiększ ilość w koszyku o 1
            product_in_cart.quantity += 1
        else:
            # Dodaj nowy produkt do koszyka
            new_product_in_cart = CartProducts(
                cart_id=cart.id,
                product_id=product_id,
                quantity=1,
                unit_price_with_discount=price_with_discount
            )
            db.session.add(new_product_in_cart)

        # Zmniejsz stan magazynowy o 1
        product.quantity -= 1

        # Przelicz koszt koszyka
        cart.total_products_cost = db.session.query(
            func.coalesce(
                db.func.sum(CartProducts.quantity * CartProducts.unit_price_with_discount),
                Decimal("0.00")
            )
        ).filter_by(cart_id=cart.id).scalar()

        db.session.commit()

        return jsonify({'message': 'Produkt dodano do koszyka'}), 201

    except Exception as e:
        db.session.rollback()
        print(f"[ERROR]: {str(e)}")
        return jsonify({'error': 'Błąd serwera'}), 500

"""

@commerce_bp.route('/carts', methods=['PUT'])
@jwt_required()
def add_product_to_cart():

    try:
        user_id = get_jwt_identity()
        data = request.get_json()
        product_id = data.get('product_id')
        quantity = data.get('quantity')  # np. +1, -1, +3, -2

        if not product_id or quantity is None:
            return jsonify({'error': 'ID produktu i ilość są wymagane'}), 400

        product = Products.query.get(product_id)
        if not product:
            return jsonify({'error': 'Nie znaleziono produktu'}), 404

        cart = Carts.query.filter_by(user_id=user_id).first()
        if not cart:
            cart = Carts(user_id=user_id)
            db.session.add(cart)
            db.session.flush()

        product_in_cart = CartProducts.query.filter_by(
            cart_id=cart.id,
            product_id=product_id
        ).first()

        price_with_discount = product.price_including_promotion()

        # 🔹 Jeżeli dodajemy (quantity > 0)
        if quantity > 0:
            if product.quantity < quantity:
                return jsonify({'error': 'Brak wystarczającej ilości w magazynie'}), 400

            if product_in_cart:
                product_in_cart.quantity += quantity
            else:
                product_in_cart = CartProducts(
                    cart_id=cart.id,
                    product_id=product_id,
                    quantity=quantity,
                    unit_price_with_discount=price_with_discount
                )
                db.session.add(product_in_cart)

            product.quantity -= quantity

        # 🔹 Jeżeli odejmujemy (quantity < 0)
        elif quantity < 0:
            if not product_in_cart:
                return jsonify({'error': 'Produkt nie znajduje się w koszyku'}), 400

            new_quantity = product_in_cart.quantity + quantity  # quantity jest ujemne

            if new_quantity <= 0:
                db.session.delete(product_in_cart)
            else:
                product_in_cart.quantity = new_quantity

            product.quantity -= quantity  # odejmujemy ujemną -> dodajemy do magazynu

        # 🔹 Aktualizacja kosztu koszyka
        cart.total_products_cost = db.session.query(
            func.coalesce(
                db.func.sum(CartProducts.quantity * CartProducts.unit_price_with_discount),
                Decimal("0.00")
            )
        ).filter_by(cart_id=cart.id).scalar()

        db.session.commit()

        return jsonify({'message': 'Koszyk zaktualizowany pomyślnie'}), 200

    except Exception as e:
        db.session.rollback()
        print(f"[ERROR]: {str(e)}")
        return jsonify({'error': 'Błąd serwera'}), 500
    
"""
@commerce_bp.route('/carts', methods=['PUT'])
@jwt_required()
def remove_product_from_cart():

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
    
"""
    
@commerce_bp.route('/carts', methods=['GET'])
@jwt_required()
def get_cart():

    """---------------------Pobranie informacji i zawartości koszyka---------------------"""

    try:
        user_id = get_jwt_identity()

        cart = Carts.query.filter_by(user_id=user_id).first()
        if not cart:
            return jsonify({'error': 'Nie znaleziono koszyka'}), 404

        products_in_cart = (
            CartProducts.query
            .filter_by(cart_id=cart.id)
            .order_by(CartProducts.id.asc())  # bez tego produkty zmieniają kolejnośc przy modyfikacji ich ilości w koszyku
            .all()
            )


        if not products_in_cart:
            return jsonify({'message': 'Koszyk jest pusty'}), 200


        cart_data = {
            'total_products_cost': str(cart.total_products_cost),
            'products': [product.to_json_user_view() for product in products_in_cart]
        }

        return jsonify(cart_data), 200

    except Exception as e:
        print(f"[ERROR]: {str(e)}")
        return jsonify({'error': 'Internal server error'}), 500
    

## ###################################################################### Transakcje i produkty w nich ######################################################################


@commerce_bp.route('/transactions', methods=['POST'])
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
        billing_address = UserAddress.query.get(data.get('billing_address_id'))
        shipping_address = UserAddress.query.get(data.get('shipping_address_id'))

        # Tworzenie nowej transakcji
        new_transaction = Transactions(
            user_id=user_id,
            total_transaction_value=cart.total_products_cost + delivery_method.fee + payment_method.fee,
            billing_address_id=billing_address.id,
            billing_address_data=billing_address.to_json(),
            shipping_address_id=shipping_address.id,
            shipping_address_data=shipping_address.to_json(),
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
    

@commerce_bp.route('/admin/transactions/<int:transaction_id>', methods=['PUT'])
@jwt_required()
@role_required('admin')
def modify_transaction_status(transaction_id):

    """-------------------------------Zmiana statusy transakcji przez administratora-------------------------------"""

    try:
        # tutaj należało by dodać możliwośc tworzenia logów zmian w bazie dancyh ze względu na audyty i zasady RODO. Na tę chwile pomijamy ze względów czasowych
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
    

@commerce_bp.route('/transactions', methods=['GET'])
@jwt_required()
def get_all_user_transactions():

    """-------------------------------Zwraca wszystkie transakcje użytkownika-------------------------------"""  

    try:
        user_id = get_jwt_identity()
        user = User.query.get(user_id) # tę sama funkcjonalnośc może używać admin ale dla wszystkich tranzakcji w bazie danych
        status = request.args.get('status')
        raw_date_from = request.args.get('date_from')
        raw_date_to = request.args.get('date_to')
        page = request.args.get('page', 1, type=int)
        per_page = request.args.get('limit', 20, type=int)

        transakcje = Transactions.query
        if user.role != 'admin':
            transakcje = transakcje.filter_by(user_id=user_id)

        if status:
            transakcje = transakcje.filter_by(status=status)
        if raw_date_from:
            date_from = str_date(raw_date_from)
            if date_from:       
                transakcje = transakcje.filter(Transactions.updated_at >= date_from)
        if raw_date_to:
            date_to = str_date(raw_date_to)
            if date_to:    
                date_to = date_to.replace(hour=23, minute=59, second=59)
                transakcje = transakcje.filter(Transactions.updated_at <= date_to)

        pagination = transakcje.order_by(Transactions.updated_at.desc()).paginate(
            page=page, per_page=per_page, error_out=False
        )

        transakcje = pagination.items

        if not transakcje:
            return jsonify({"error": "Brak transakcji dla konta użytkownika"}), 400

        response_data = []
        for transakcja in transakcje:
            produkty = TransactionProducts.query.filter_by(transaction_id=transakcja.id).all()
            if user.role != 'admin':
                data = transakcja.to_json_user_view()
                data["producty"] = [p.to_json_user_view() for p in produkty]
            else:
                data = transakcja.to_json()
                data["producty"] = [p.to_json() for p in produkty]
            response_data.append(data)

        return jsonify({
            "transakcje": response_data,
            "total": pagination.total,
            "page": pagination.page,
            "pages": pagination.pages,
            "has_next": pagination.has_next,
            "has_prev": pagination.has_prev,
            "next_page": pagination.next_num if pagination.has_next else None,
            "prev_page": pagination.prev_num if pagination.has_prev else None
        }), 200
        

    except Exception as e:
        print(f"[ERROR]: {str(e)}")
        return jsonify({'error': 'Internal server error'}), 500
    

## ###################################################################### Whishlist ######################################################################


@commerce_bp.route('/wishlists', methods=['POST'])
@jwt_required()
def add_to_whishlist():

    """-------------------------------Dodawanie produktu do listy ulubionych przez użytkownika-------------------------------"""

    user_id = get_jwt_identity()
    data = request.get_json()

    try:

        produkt = Products.query.get(data['product_id'])

        if not produkt:
            return jsonify({'error': 'Produkt nie istnieje'}), 404


        wishlist_item = Wishlists(
            user_id=user_id, 
            product_id=data['product_id']
        )

        db.session.add(wishlist_item)
        db.session.commit()

        return jsonify({'message': 'Produkt dodany do ulubionych'}), 201

    except Exception as e:
        db.session.rollback()
        print(f"[ERROR]: {str(e)}")
        return jsonify({'error': 'Internal server error'}), 500
    

@commerce_bp.route('/wishlists/<int:product_id>', methods=['DELETE'])
@jwt_required()
def remove_from_whishlist(product_id):

    """-------------------------------Usuwanie produktu z listy ulubionych przez użytkownika-------------------------------"""

    user_id = get_jwt_identity()

    try:
        wishlist_item = Wishlists.query.filter_by(user_id=user_id, product_id=product_id).first()

        if not wishlist_item:
            return jsonify({'error': 'Produkt nie znajduje się w ulubionych'}), 404

        db.session.delete(wishlist_item)
        db.session.commit()

        return jsonify({'message': 'Produkt usunięty z ulubionych'}), 200

    except Exception as e:
        db.session.rollback()
        print(f"[ERROR]: {str(e)}")
        return jsonify({'error': 'Internal server error'}), 500


@commerce_bp.route('/wishlists', methods=['GET'])
@jwt_required()
def get_wishlist():

    """-------------------------------Pobieramy listę wszystkich ulubionych produktów użytkownika-------------------------------"""

    user_id = get_jwt_identity()

    try:
        products = Wishlists.query.filter_by(user_id=user_id).all()
        if not products:
            return jsonify({'error': 'No products found in wishlist'}), 404

        return jsonify([product.to_json() for product in products]), 200
    
    except Exception as e:
        print(f"[ERROR]: {str(e)}")
        return jsonify({'error': 'Internal server error'}), 500