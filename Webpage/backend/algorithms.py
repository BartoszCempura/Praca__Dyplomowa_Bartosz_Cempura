from flask import Blueprint, request, jsonify
from backend import db
from backend.models import Products, UserProductInteractions
from flask_jwt_extended import get_jwt_identity, jwt_required
from backend.utils import role_required, str_date
from sqlalchemy import func, desc, desc, case
from datetime import datetime, timedelta, timezone
from decimal import Decimal

algorithms_bp = Blueprint('algorithms', __name__, url_prefix='/api/algorithms')


@algorithms_bp.route('/top-products', methods=['GET'])
def get_top_products():

    """-------------------------------Pobranie produktów cieszących się największą popularnością-------------------------------"""

    try:
        # 1️⃣ Data sprzed tygodnia
        one_week_ago = datetime.now(timezone.utc) - timedelta(days=7)

        # 2️⃣ Wagi dla typów interakcji
        interaction_weights = {
            'View': 1,
            'AddToCart': 3,
            'Purchase': 5,
            'Review': 2,
            'AddToWishlist': 2
        }

        # 3️⃣ CASE WHEN do liczenia punktów popularności
        weighted_score = func.sum(
            case(
                [(UserProductInteractions.type == key, value) for key, value in interaction_weights.items()],
                else_=0
            )
        ).label('popularity_score')

        # 4️⃣ Zapytanie agregujące TOP 10 produktów
        product_scores = (
            UserProductInteractions.query
            .with_entities(
                UserProductInteractions.product_id,
                weighted_score
            )
            .filter(UserProductInteractions.created_at >= one_week_ago)
            .group_by(UserProductInteractions.product_id)
            .order_by(desc('popularity_score'))
            .limit(10)
            .all()
        )

        # 5️⃣ Pobranie podstawowych danych produktów
        top_products = []
        for product_id, score in product_scores:
            product = Products.query.get(product_id)
            if product:
                top_products.append({
                    "product": product.to_json_user_view(),
                    "popularity_score": score
                })

        return jsonify(top_products), 200

    except Exception as e:
        db.session.rollback()
        print(f"[ERROR]: {str(e)}")
        return jsonify({'error': 'Internal server error'}), 500