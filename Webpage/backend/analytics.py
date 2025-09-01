from flask import Blueprint, request, jsonify
from backend import db
from backend.models import UserProductInteractions, ProductReviews, Products
from flask_jwt_extended import get_jwt_identity, jwt_required
from backend.utils import role_required

analytics_bp = Blueprint('analytics', __name__, url_prefix='/api/analytics')


## ###################################################################### Interakcje z produktami ######################################################################

@analytics_bp.route('/add_product_interaction', methods=['POST'])
@jwt_required(optional=True)
def add_product_interaction():

    """-------------------------------Dodawanie informacji o interakcji z produktem-------------------------------"""

    try:

## endpoint nie ma zwracać żadnych informacji tylko działać cicho w tle. 
## działą również dla niezalogowanych użytkowników 
      
        user_id = get_jwt_identity()
        data = request.get_json()

        if not data:
            return '', 204

        interaction_type = data.get('type')
        product_id = data.get('product_id')
        session_id = data.get('session_id')

        if not product_id or not interaction_type or not session_id:
            return '', 204
        
        if interaction_type not in ['View', 'AddToCart', 'Purchase', 'Review', 'AddToWishlist']:
            return '', 204

        new_interaction = UserProductInteractions(
            user_id=user_id,
            product_id=product_id,
            type=interaction_type,
            session_id=session_id
        )

        db.session.add(new_interaction)
        db.session.commit()

        return '', 204 

    except Exception as e:
            db.session.rollback()
            print(f"[ERROR]: {str(e)}")
            return jsonify({'error': 'Internal server error'}), 500


## ###################################################################### Review ######################################################################

@analytics_bp.route('/add_product_review', methods=['POST'])
@jwt_required()
def add_product_review():

    """-------------------------------Dodawanie recenzji produktu-------------------------------"""

    try:
      
        user_id = get_jwt_identity()
        data = request.get_json()
        product_id = data.get('product_id')
        rating = data.get('rating')

        if not product_id:
            return jsonify({'message': 'Review nie jest powiązane z żadnym produkem'}), 400
        
        if not rating:
            return jsonify({'message': 'Nie odano wartości oceny produktu'}), 400
        
        produkt = Products.query.filter_by(id=product_id).first()
        
        if not produkt:
            return jsonify({'message': 'Produkt nie istnieje'}), 404

        if not (1.0 <= rating <= 5.0):
            return jsonify({'message': 'Ocena musi być liczbą z zakresu od 1 do 5'}), 422

        new_review = ProductReviews(
            user_id=user_id,
            product_id=product_id,
            rating = rating,
            review = data.get('review'),
            is_verified_purchase = data.get('is_verified_purchase', False),
            is_approved = data.get('is_approved', False)
        )

        db.session.add(new_review)
        db.session.commit()

        return jsonify({'message': 'Recenzja produktu została dodana pomyślnie'}), 201

    except Exception as e:
            db.session.rollback()
            print(f"[ERROR]: {str(e)}")
            return jsonify({'error': 'Internal server error'}), 500