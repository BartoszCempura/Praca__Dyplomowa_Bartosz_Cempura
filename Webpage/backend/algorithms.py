from flask import Blueprint, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from backend.models import User, Products, UserProductInteractions, ProductAccessories, ProductRecommendations
from sqlalchemy import func, desc, desc, case
from datetime import datetime, timedelta, timezone
from backend.utils import load_product_map


algorithms_bp = Blueprint('algorithms', __name__, url_prefix='/api/algorithms')


## ############################################################### Popular Products Algorithm ######################################################################


@algorithms_bp.route('/top-products', methods=['GET']) ## used - used - bestseller, topProducts, adminDashboard
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

#________________________________________Most popular products na podstawie interakcji________________________________________

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
        ).label('score')

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
            .limit(20)
            .all()
        )

        # pobieranie danych o produkcie. 
        most_popular_products = []

        most_popular_products_dict = load_product_map([product_id for product_id, _ in product_scores])

        for product_id, score in product_scores:
            product = most_popular_products_dict.get(product_id)

            if not product:
                continue

            if user and user.role == 'admin':
                product_data = product.to_json()
                product_data['popularity_score'] = float(score)
                most_popular_products.append(product_data)
            else:
                most_popular_products.append(product.to_json_user_view())


#_______________________________________Obliczanie liczby zakupów produktu w ostatnim tygodniu_________________________________________


        purchase_calculation = (
            UserProductInteractions.query.with_entities(
                UserProductInteractions.product_id,
                func.count(UserProductInteractions.id).label('purchase_count')
        ).filter(
            UserProductInteractions.type == 'Purchase',
            UserProductInteractions.created_at >= one_week_ago 
        )
        .group_by(UserProductInteractions.product_id)
        .order_by(desc('purchase_count'))
        ).all()
   
        number_of_product_purchases_dict = load_product_map([product_id for product_id, _ in purchase_calculation])

        # produkt o największej liczbie zakupów w ostatnim tygodniu
        top_purchase_product = None
        top_purchase = purchase_calculation[0] if purchase_calculation else None

        if top_purchase:
            product_id, purchase_count = top_purchase
            product = number_of_product_purchases_dict.get(product_id)

            top_purchase_product =  product.to_json_user_view()
            top_purchase_product['purchase_count'] = purchase_count

        # lista produktów z liczbą zakupów w ostatnim tygodniu
        products_purchased_this_week = []
        for product_id, purchase_count in purchase_calculation:
            product = number_of_product_purchases_dict.get(product_id)

            if not product:
                continue

            single_product_data =  product.to_json_user_view()
            single_product_data['purchase_count'] = purchase_count
            products_purchased_this_week.append(single_product_data)


        daily_purchases = (
            UserProductInteractions.query.with_entities(
                UserProductInteractions.product_id,
                func.date(UserProductInteractions.created_at).label('purchase_date'),
                func.count(UserProductInteractions.id).label('daily_count')
            )
            .filter(
                UserProductInteractions.type == 'Purchase',
                UserProductInteractions.created_at >= one_week_ago
            )
            .group_by (
                UserProductInteractions.product_id,
                func.date(UserProductInteractions.created_at)
            )
            .order_by('purchase_date')
            .all()
        )

        # lista produktów z liczbą zakupów w poszczególne dni w ostatnim tygodniu
        product_purchase_history = []
        product_purchase_history_dict = load_product_map([product_id for product_id, _, _ in daily_purchases])

        for product_id, purchase_date, daily_count in daily_purchases:
            product = product_purchase_history_dict.get(product_id)

            if not product:
                continue

            product_data = product.to_json_user_view()
            product_data['date'] = purchase_date.strftime('%Y-%m-%d')
            product_data['count'] = daily_count
            product_purchase_history.append(product_data)


#_______________________________________Najczęściej oglądany produkt_________________________________________


        top_viewed = (
            UserProductInteractions.query.with_entities(
                UserProductInteractions.product_id,
                func.count(UserProductInteractions.id).label('view_count')
        ).filter(
            UserProductInteractions.type == 'View',
            UserProductInteractions.created_at >= one_week_ago 
        )
        .group_by(UserProductInteractions.product_id)
        .order_by(desc('view_count'))
        .first()
        )
        
        top_viewed_product = None
        if top_viewed:
            product_id, view_count = top_viewed
            product = Products.query.get(product_id)

            if product:
                top_viewed_product =  product.to_json_user_view()
                top_viewed_product['view_count'] = view_count


        return jsonify({
            'top_products': most_popular_products,
            'most_purchased_product': top_purchase_product,
            'product_purchase_history': product_purchase_history,
            'products_purchased_this_week': products_purchased_this_week,
            'top_viewed_product': top_viewed_product
        }), 200

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

@algorithms_bp.route('/products-similar/<string:slug>', methods=['GET']) ## used - productDetails
def get_similar_products(slug):

    """-------------------------------Zwraca 5 produktów podobnych do przeglądanego-------------------------------"""

    try:
        product = Products.query.filter_by(slug=slug).first()
        if not product:
            return jsonify({"error": "Brak produktu o tym slugu"}), 400

        recommendations = (
            ProductRecommendations.query
            .filter(
                (ProductRecommendations.product_id == product.id) | 
                (ProductRecommendations.recommended_product_id == product.id)
            )
            .order_by(ProductRecommendations.score.desc())
            .limit(5)
            .all()
        )

        if not recommendations:
            return '', 204

        result = []
        for recommendation in recommendations:

            if recommendation.product_id == product.id:
                other_product_id = recommendation.recommended_product_id  
            else:
                other_product_id = recommendation.product_id 
            
            recommended_product = Products.query.get(other_product_id)
            if recommended_product:
                result.append(recommended_product.to_json_user_view())


        return jsonify(result), 200

    except Exception as e:
        print(f"[ERROR]: {str(e)}")
        return jsonify({'error': 'Internal server error'}), 500