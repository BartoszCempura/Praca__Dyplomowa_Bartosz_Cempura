from flask import Blueprint, request, jsonify
from backend import db
from backend.models import DeliveryMethods, PaymentMethods, Carts, CartProducts, Products, Transactions, TransactionStatus, TransactionProducts, User, Wishlists, UserAddress
from flask_jwt_extended import get_jwt_identity, jwt_required
from backend.utils import role_required, str_date
from sqlalchemy import func
from sqlalchemy.orm import joinedload 
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



@commerce_bp.route('/delivery-methods', methods=['GET']) # used - cartPartTwo
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



@commerce_bp.route('/payment-methods', methods=['GET']) # used - cartPartTwo
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

@commerce_bp.route('/carts', methods=['PUT']) ## used - addToCart 
@jwt_required()
def add_product_to_cart():

    try:
        user_id = get_jwt_identity()
        data = request.get_json()
        product_id = data.get('product_id')
        quantity = data.get('quantity')  # np. +1, -1, +3, -2

        if not product_id or quantity is None: # endpoint wymaga 2 pól
            return '', 400

        product = Products.query.get(product_id) # zabespieczenie jak by dane przekazane do endpointu były niekompletne - niepoprawne product id
        if not product:
            return '', 404

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

        if quantity > 0:
            if product.quantity < quantity: # weryfikowane po stronie frontend - przekroczono stan magazynowy
                return '', 409

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

        elif quantity < 0:
            if not product_in_cart: # zabespieczenie jak by próbowano przekazać wartośc ujemną dla produktu którego nie ma wkoszyku tz nie była zajęty stan magazynowy
                return '', 409

            new_quantity = product_in_cart.quantity + quantity  # quantity jest ujemne

            if new_quantity <= 0:
                db.session.delete(product_in_cart)
            else:
                product_in_cart.quantity = new_quantity

            product.quantity -= quantity  # odejmujemy ujemną -> dodajemy do magazynu

        db.session.commit()

        return '', 204

    except Exception as e:
        db.session.rollback()
        print(f"[ERROR]: {str(e)}")
        return jsonify({'error': 'Błąd serwera'}), 500
       
@commerce_bp.route('/carts', methods=['GET']) ## used - Cart , productCard
@jwt_required(optional=True)
def get_cart():

    """---------------------Pobranie informacji i zawartości koszyka---------------------"""

    try:
        user_id = get_jwt_identity()

        cart = Carts.query.filter_by(user_id=user_id).first()
        if not cart: # brak koszyka - jak dodaje produkty jest automatycznie tworzony
            return '', 200

        products_in_cart = (
            CartProducts.query
            .filter_by(cart_id=cart.id)
            .order_by(CartProducts.id.asc())  # bez tego produkty zmieniają kolejnośc przy modyfikacji ich ilości w koszyku
            .all()
            )


        if not products_in_cart: # brak produktów w koszyku
            return '', 204


        cart_data = {
            'products': [product.to_json_user_view() for product in products_in_cart]
        }

        return jsonify(cart_data), 200

    except Exception as e:
        print(f"[ERROR]: {str(e)}")
        return jsonify({'error': 'Internal server error'}), 500
    

## ###################################################################### Transakcje i produkty w nich ######################################################################


@commerce_bp.route('/transactions', methods=['POST']) ## used - finalizacja transakcji
@jwt_required()
def closing_purchase():

    """---------------------Zamknięcie zakupu---------------------"""

    try:
        user_id = int(get_jwt_identity())
        data = request.get_json()

        required_fields = ['billing_address_id', 'shipping_address_id', 'delivery_method_id', 'payment_method_id', 'products']
        for field in required_fields:
            if not data.get(field):
                return jsonify({'error': f'{field} is required'}), 400

        cart = Carts.query.filter_by(user_id=user_id).first()
        if not cart:
            return jsonify({'error': 'Nie znaleziono koszyka'}), 404
        
        products = data.get('products')
        if not products:
            return jsonify({'error': 'Koszyk jest pusty'}), 400

        delivery_method = DeliveryMethods.query.filter_by(id=data.get('delivery_method_id'), is_active=True).first()
        if not delivery_method:
            return jsonify({'error': 'Nieprawidłowa metoda dostawy'}), 400
        
        payment_method = PaymentMethods.query.filter_by(id=data.get('payment_method_id'), is_active=True).first()
        if not payment_method:
            return jsonify({'error': 'Nieprawidłowa metoda płatności'}), 400
        
        billing_address = UserAddress.query.get(data.get('billing_address_id'))
        shipping_address = UserAddress.query.get(data.get('shipping_address_id'))
        if not billing_address or not shipping_address:
            return jsonify({'error': 'Adress nie istnieje'}), 400
        if billing_address.user_id != user_id or shipping_address.user_id != user_id:
            return jsonify({'error': 'Nieprawidłowy adres użytkownika'}), 403

        products_value_sum = 0
        for product in products:
            products_value_sum += (product["quantity"] * Decimal(product["unit_price_with_discount"]))

        # Tworzenie nowej transakcji
        new_transaction = Transactions(
            user_id=user_id,
            total_transaction_value=(products_value_sum + delivery_method.fee + payment_method.fee),
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

        
        for product in products:
            db_product_data = Products.query.filter_by(id=product["product_id"]).with_for_update().first()

            if not db_product_data:
                return jsonify({'error': 'Produkt nie istnieje'}), 404

            if product["quantity"] <= 0:
                return jsonify({'error': 'Nieprawidłowa ilość produktu'}), 400
            
            if db_product_data.quantity < product["quantity"]:
                return jsonify({'error': f'Brak produktu {db_product_data.name} na stanie'}), 400
            
            db_product_data.quantity -= (product["quantity"] - 1) # odejmujemy quantity - 1, bo 1 sztuka została zarezerwowana przy dodaniu do koszyka

            new_transaction_product = TransactionProducts(
                transaction_id=new_transaction.id,
                product_id=product["product_id"],
                quantity=product["quantity"],
                unit_price_with_discount=db_product_data.price_including_promotion(),
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
    

@commerce_bp.route('/admin/transactions/<int:transaction_id>', methods=['PUT']) ## used - kokpit modyfiacja statusu transakcji
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

                return jsonify({'message': 'Transakcja anulowana pomyślnie'}), 200
            
        
        # nie zaimplementowano
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
    

@commerce_bp.route('/transactions', methods=['GET']) ## used - kokpit transakcje
@jwt_required()
def get_all_user_transactions():

    """-------------------------------Zwraca wszystkie transakcje użytkownika-------------------------------"""  

    try:
        user_id = get_jwt_identity()
        user = User.query.get(user_id) # tę sama funkcjonalnośc może używać admin ale dla wszystkich tranzakcji w bazie danych
        if not user:
            return jsonify({"error": "User not found"}), 404
        
        status = request.args.get('status')
        raw_date_from = request.args.get('date_from')
        raw_date_to = request.args.get('date_to')
        page = request.args.get('page', 1, type=int)
        per_page = request.args.get('limit', 20, type=int)

        transakcje = Transactions.query.options(
            joinedload(Transactions.user),
            joinedload(Transactions.delivery_method),
            joinedload(Transactions.payment_method)
        )
        if user.role != 'admin':
            transakcje = transakcje.filter_by(user_id=user_id)

        if status:
            try:
                status_enum = TransactionStatus[status]
                transakcje = transakcje.filter_by(status=status_enum)
            except KeyError:
                return jsonify({'error': 'Nieprawidłowy status'}), 400
            
        if raw_date_from:
            date_from = str_date(raw_date_from)
            if date_from:       
                transakcje = transakcje.filter(Transactions.created_at >= date_from)
            else:
                return jsonify({"error": "Invalid date_from format"}), 400
            
        if raw_date_to:
            date_to = str_date(raw_date_to)
            if date_to:    
                date_to = date_to.replace(hour=23, minute=59, second=59)
                transakcje = transakcje.filter(Transactions.created_at <= date_to)
            else:
                return jsonify({"error": "Invalid date_to format"}), 400
            
        transakcje = transakcje.order_by(Transactions.created_at.desc())

        pagination = transakcje.paginate(page=page, per_page=per_page, error_out=False)

        transakcje = pagination.items

        if not transakcje:
            return jsonify({
                "transakcje": [],
                "pagination": {
                    "total": 0,
                    "page": page,
                    "pages": 0,
                    "per_page": per_page,
                    "has_next": False,
                    "has_prev": False
                },
                "message": "Brak transakcji"
            }), 200

        response_data = []
        for transakcja in transakcje:
            if user.role != 'admin':
                data = transakcja.to_json_user_view()
                data["producty"] = [p.to_json_user_view() for p in transakcja.products]
            else:
                data = transakcja.to_json()
                data["producty"] = [p.to_json() for p in transakcja.products]

            response_data.append(data)

        return jsonify({
            "transakcje": response_data,
            "pagination": {
                "total": pagination.total,
                "page": pagination.page,
                "pages": pagination.pages,
                "per_page": per_page,
                "has_next": pagination.has_next,
                "has_prev": pagination.has_prev,
                "next_page": pagination.next_num if pagination.has_next else None,
                "prev_page": pagination.prev_num if pagination.has_prev else None
            }
        }), 200
        

    except Exception as e:
        print(f"[ERROR]: {str(e)}")
        return jsonify({'error': 'Internal server error'}), 500

## ###################################################################### Whishlist ######################################################################


@commerce_bp.route('/wishlists', methods=['POST']) ## used - productCard
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

        return '', 201

    except Exception as e:
        db.session.rollback()
        print(f"[ERROR]: {str(e)}")
        return jsonify({'error': 'Internal server error'}), 500
    

@commerce_bp.route('/wishlists/<int:product_id>', methods=['DELETE']) ## used - productCard
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

        return '', 200

    except Exception as e:
        db.session.rollback()
        print(f"[ERROR]: {str(e)}")
        return jsonify({'error': 'Internal server error'}), 500


@commerce_bp.route('/wishlists', methods=['GET']) ## used - wishlist
@jwt_required(optional=True)
def get_wishlist():

    """-------------------------------Pobieramy listę wszystkich ulubionych produktów użytkownika-------------------------------"""

    user_id = get_jwt_identity()

    try:
        products = Wishlists.query.filter_by(user_id=user_id).all()

        product_list = [wish.product.to_json_user_view() for wish in products if wish.product is not None]

        return jsonify(product_list), 200
    
    except Exception as e:
        print(f"[ERROR]: {str(e)}")
        return jsonify({'error': 'Internal server error'}), 500