from flask import Blueprint, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from backend.models import User, Products, UserProductInteractions, ProductAccessories, ProductRecommendations
from sqlalchemy import func, desc, desc, case
from datetime import datetime, timedelta, timezone


algorithms_bp = Blueprint('algorithms', __name__, url_prefix='/api/algorithms')


## ############################################################### Popular Products Algorithm ######################################################################


@algorithms_bp.route('/top-products', methods=['GET'])
@jwt_required(optional=True)
def get_top_products():

    """-------------------------------Pobranie produktów cieszących się największą popularnością-------------------------------"""

    try:
        user_id = get_jwt_identity()
        if user_id:
            user = User.query.get(user_id)
        else:
            user = None
        # Jaka data była 7 dni temuj
        one_week_ago = datetime.now(timezone.utc) - timedelta(days=7)

        # przypisanie wartości wagi dla interakcji z produktem
        weighted_score = func.sum(
            case(
                (UserProductInteractions.type == 'View', 1),
                (UserProductInteractions.type == 'AddToCart', 3),
                (UserProductInteractions.type == 'Purchase', 5),
                (UserProductInteractions.type == 'Review', 2),
                (UserProductInteractions.type == 'AddToWishlist', 2),
                else_=0
            )
        )

        # z UserProductInteractions pobieral tylko product_id i wartość wagi dla typu interakcji
        # filtrowanie interakcji z ostatniego tygodnia
        # grupuje wyniki po product_id
        # sortuje wyniki malejąco według sumy wartości wag
        # określam ile ma być widocznych wyników
        # pobieram wyniki
        product_scores = (
            UserProductInteractions.query.with_entities(
                UserProductInteractions.product_id,
                weighted_score
            )
            .filter(UserProductInteractions.created_at >= one_week_ago)
            .group_by(UserProductInteractions.product_id)
            .order_by(desc(weighted_score))
            .limit(10)
            .all()
        )

        # pobieranie danych o produkcie. 
        # można zoptymalizowac tak aby proces wykonywany był w jednym zapytaniu do bazy danych
        # ale w tym przypadku jest to czytelniejsze i w kontekście projektu nie ma potrzeby na taką optymalizację
        top_products = []
        for product_id, score in product_scores:
            product = Products.query.get(product_id)
            if product:
                if user and user.role == 'admin':
                    top_products.append({
                        "product": product.to_json(),
                        "popularity_score": score
                    })
                else:
                    top_products.append({"product": product.to_json_user_view()})

        return jsonify(top_products), 200

    except Exception as e:
        print(f"[ERROR]: {str(e)}")
        return jsonify({'error': 'Internal server error'}), 500
    
    
## ############################################################### Accessory Recommendation  ######################################################################

@algorithms_bp.route('/product-accessories/<int:product_id>', methods=['GET'])
def get_top_accessories_for_product(product_id):

    """-------------------------------Zwraca 5 akcesoriów o najwyższej wadze dla produktu-------------------------------"""

    try:
        if not Products.query.get(product_id):
            return jsonify({"error": "Brak produktu o tym ID"}), 400

        accessories = (
            ProductAccessories.query
            .filter_by(product_id=product_id)
            .order_by(ProductAccessories.weight.desc())
            .limit(5)
            .all()
        )

        if not accessories:
            return '', 204

        # Pobierz dane produktów-akcesoriów
        result = []
        for accessory in accessories:
            accessory_product = Products.query.get(accessory.accessory_product_id)
            if accessory_product:
                result.append({"product": accessory_product.to_json_user_view()})

        return jsonify(result), 200

    except Exception as e:
        print(f"[ERROR]: {str(e)}")
        return jsonify({'error': 'Internal server error'}), 500
    

## ############################################################### Recommends similar products based on attributes/features  ######################################################################

@algorithms_bp.route('/products-similar/<int:product_id>', methods=['GET'])
def get_similar_products(product_id):

    """-------------------------------Zwraca 5 produktów podobnych do przeglądanego-------------------------------"""

    try:
        if not Products.query.get(product_id):
            return jsonify({"error": "Brak produktu o tym ID"}), 400

        recommendations = (
            ProductRecommendations.query
            .filter_by(product_id=product_id)
            .order_by(ProductRecommendations.score.desc())
            .limit(5)
            .all()
        )

        if not recommendations:
            return '', 204

        result = []
        for recommendation in recommendations:
            recommended_product = Products.query.get(recommendation.recommended_product_id)
            if recommended_product:
                result.append({"product": recommended_product.to_json_user_view()})

        return jsonify(result), 200

    except Exception as e:
        print(f"[ERROR]: {str(e)}")
        return jsonify({'error': 'Internal server error'}), 500