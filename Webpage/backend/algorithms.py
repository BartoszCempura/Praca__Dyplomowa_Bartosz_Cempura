from flask import Blueprint, jsonify
from backend import db
from flask_jwt_extended import get_jwt_identity, jwt_required
from backend.utils import role_required
from backend.models import Products, UserProductInteractions
from sqlalchemy import func, desc, desc, case
from datetime import datetime, timedelta, timezone
from decimal import Decimal

algorithms_bp = Blueprint('algorithms', __name__, url_prefix='/api/algorithms')


@algorithms_bp.route('/top-products', methods=['GET'])
def get_top_products():

    """-------------------------------Pobranie produktów cieszących się największą popularnością-------------------------------"""

    try:
        # Jaka data była 7 dni temuj
        one_week_ago = datetime.now(timezone.utc) - timedelta(days=7)

        # przypisanie wartości wagi dla interakcji z produktem
        weighted_score = func.sum(
            case(
                [
                    (UserProductInteractions.type == 'View', 1),
                    (UserProductInteractions.type == 'AddToCart', 3),
                    (UserProductInteractions.type == 'Purchase', 5),
                    (UserProductInteractions.type == 'Review', 2),
                    (UserProductInteractions.type == 'AddToWishlist', 2)
                ],
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
        for product_id, _ in product_scores:
            product = Products.query.get(product_id)
            if product:
                top_products.append({"product": product.to_json_user_view()})

        return jsonify(top_products), 200

    except Exception as e:
        print(f"[ERROR]: {str(e)}")
        return jsonify({'error': 'Internal server error'}), 500
    


@algorithms_bp.route('/admin/top-products', methods=['GET'])
@jwt_required()
@role_required('admin')
def get_top_products_for_admin():

    """-------------------------------Pobranie produktów cieszących się największą popularnością przez administratora-------------------------------"""

    try:

        one_week_ago = datetime.now(timezone.utc) - timedelta(days=7)

        weighted_score = func.sum(
            case(
                [
                    (UserProductInteractions.type == 'View', 1),
                    (UserProductInteractions.type == 'AddToCart', 3),
                    (UserProductInteractions.type == 'Purchase', 5),
                    (UserProductInteractions.type == 'Review', 2),
                    (UserProductInteractions.type == 'AddToWishlist', 2)
                ],
                else_=0
            )
        )

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
        # Pobieranie danych o produkcie wraz z wartością score dla administratora
        top_products = []
        for product_id, score in product_scores:
            product = Products.query.get(product_id)
            if product:
                top_products.append({
                    "product": product.to_json(),
                    "popularity_score": score
                })

        return jsonify(top_products), 200

    except Exception as e:
        print(f"[ERROR]: {str(e)}")
        return jsonify({'error': 'Internal server error'}), 500