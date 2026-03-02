from flask import Blueprint, request, jsonify
from datetime import datetime, timezone, timedelta
from backend import db
from backend.models import UserProductInteractions, ProductReviews, Products
from flask_jwt_extended import get_jwt_identity, jwt_required
from backend.utils import role_required, str_date

analytics_bp = Blueprint('analytics', __name__, url_prefix='/api/analytics')


## ###################################################################### Interakcje z produktami ######################################################################


@analytics_bp.route('/user-product-interactions', methods=['POST']) ## used - trackInteraction -> cartPartTwo, productCard, productDetails
@jwt_required(optional=True)
def add_product_interaction():

    """-------------------------------Dodawanie informacji o interakcji z produktem (cicho w tle).-------------------------------"""

    try:

        user_id = get_jwt_identity()
        data = request.get_json()

        if not data:
            return '', 204

        interaction_type = data.get('type')
        product_id = data.get('product_id')
        session_id = data.get('session_id')

        # Wymagane minimum
        if not product_id or not interaction_type or not session_id:
            return '', 400
        
        if interaction_type not in ['View', 'AddToCart', 'Purchase', 'Review', 'AddToWishlist']:
            return '', 400
        
        # Zapobiega duplikatom w krótkim czasie z pominięciem dla purchase ( pętla w cartPartTwo)   
        if session_id and interaction_type != 'Purchase':
            five_seconds_ago = datetime.now(timezone.utc) - timedelta(seconds=5)
            duplicate = UserProductInteractions.query.filter(
                UserProductInteractions.session_id == session_id,
                UserProductInteractions.product_id == product_id,
                UserProductInteractions.type == interaction_type,
                UserProductInteractions.created_at > five_seconds_ago
            ).first()
            if duplicate:
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


@analytics_bp.route('/product-reviews', methods=['POST'])
@jwt_required()
def add_product_review():

    """-------------------------------Dodawanie recenzji produktu przez użytkownika-------------------------------"""

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
    

@analytics_bp.route('/product-reviews/<int:product_id>', methods=['PUT'])
@jwt_required()
def modify_product_review(product_id):

    """-------------------------------Modyfikowanie recencji przez użytkownika-------------------------------"""

    try:
      
        user_id = get_jwt_identity()
        data = request.get_json()        

        if not product_id:
            return jsonify({'error': 'Brak id produktu'}), 400
        
        review_old = ProductReviews.query.filter(
            ProductReviews.user_id == user_id,
            ProductReviews.product_id == product_id
        ).first()

        if not review_old:
            return jsonify({'message': 'Brak recenzji dla tego produktu'}), 404
        
        if 'rating' in data:
            try:
                rating = float(data['rating']) # bezpośredni dostęp do klucza. Brak oznacza KeyError
            except (TypeError, ValueError):
                return jsonify({'error': 'Ocena musi być liczbą'}), 400

            if not (1.0 <= rating <= 5.0):
                return jsonify({'error': 'Ocena musi mieć wartość z przedziału 1.0 do 5.0'}), 400
            review_old.rating = rating


        review = data.get('review')
        if review:
            review_old.review = review

        db.session.commit()

        return jsonify({"message": "Recenzja zmodyfikowana poprawnie"}), 200

    except Exception as e:
            db.session.rollback()
            print(f"[ERROR]: {str(e)}")
            return jsonify({'error': 'Internal server error'}), 500
    
  
@analytics_bp.route('/product-reviews/<int:product_id>', methods=['DELETE'])
@jwt_required()
def delete_product_review(product_id):

    """-------------------------------Usuwanie recenzji przez użytkownika-------------------------------"""

    try:

        user_id = get_jwt_identity()

        if not product_id:
            return jsonify({'error': 'Brak id produktu'}), 400

        review_for_delete = ProductReviews.query.filter(
            ProductReviews.user_id == user_id,
            ProductReviews.product_id == product_id
        ).first()

        if not review_for_delete:
            return jsonify({'message': 'Brak recenzji dla tego produktu'}), 404

        db.session.delete(review_for_delete)
        db.session.commit()

        return jsonify({"message": "Recenzja usunięta poprawnie"}), 200

    except Exception as e:
        db.session.rollback()
        print(f"[ERROR]: {str(e)}")
        return jsonify({'error': 'Internal server error'}), 500
    

@analytics_bp.route('/admin/product-reviews/<int:review_id>', methods=['PUT'])
@jwt_required()
@role_required('admin')
def admin_set_verified_and_approved(review_id):

    """-------------------------------Modyfikacja statusu review przez administratora-------------------------------"""

    try:
   
        review = ProductReviews.query.filter_by(id=review_id).first()

        if not review:
            return jsonify({"error": "Brak recenzji"}), 404

        data = request.get_json()

        review.is_verified_purchase = data.get('is_verified_purchase', review.is_verified_purchase)
        review.is_approved = data.get('is_approved', review.is_approved)

        db.session.commit()

        return jsonify({
            "message": "Recęzja zmodyfikowana poprawnie",
            "review": review.to_json()
        }), 200

    except Exception as e:
        db.session.rollback()
        print(f"[ERROR]: {str(e)}")
        return jsonify({'error': 'Internal server error'}), 500

    
@analytics_bp.route('/admin/product-reviews/<int:review_id>', methods=['DELETE'])
@jwt_required()
@role_required('admin')
def admin_delete_product_review(review_id):

    """-------------------------------Usuwanie recenzji przez administratora-------------------------------"""

    try:

        if not review_id:
            return jsonify({'error': 'Brak id recenzji'}), 400

        review_for_delete = ProductReviews.query.filter_by(id=review_id).first()

        if not review_for_delete:
            return jsonify({'message': 'Brak recenzji o tym id'}), 404

        db.session.delete(review_for_delete)
        db.session.commit()

        return jsonify({"message": "Recenzja usunięta poprawnie"}), 200

    except Exception as e:
        db.session.rollback()
        print(f"[ERROR]: {str(e)}")
        return jsonify({'error': 'Internal server error'}), 500
    
    
@analytics_bp.route('/admin/product-reviews', methods=['GET'])
@jwt_required()
@role_required('admin')
def get_all_reviews():
     
    """-------------------------------Pobiera reviews i zwraca filtrowaną odpowiedź dla administratora-------------------------------"""

    try:

        verified = request.args.get('verified')
        approved = request.args.get('approved')
        raw_date_from = request.args.get('date_from')
        raw_date_to = request.args.get('date_to')
        page = request.args.get('page', 1, type=int)
        per_page = request.args.get('limit', 20, type=int)

        all_reviews = ProductReviews.query

        if verified is not None:
            is_verified = verified.lower() == 'true'
            all_reviews = all_reviews.filter_by(is_verified_purchase=is_verified)

        if approved is not None:
            is_approved = approved.lower() == 'true'
            all_reviews = all_reviews.filter_by(is_approved=is_approved)
        
        if raw_date_from:
            date_from = str_date(raw_date_from)
            if date_from:
                all_reviews = all_reviews.filter(ProductReviews.updated_at >= date_from)
        if raw_date_to:
            date_to = str_date(raw_date_to)
            if date_to:
                date_to = date_to.replace(hour=23, minute=59, second=59)
                all_reviews = all_reviews.filter(ProductReviews.updated_at <= date_to)

        pagination = all_reviews.order_by(ProductReviews.updated_at.desc()).paginate(
            page=page, per_page=per_page, error_out=False
        )

        all_reviews = pagination.items

        if not all_reviews:
            return jsonify([]), 200
        
        response_data = []
        for review in all_reviews:
            data = review.to_json()
            response_data.append(data)

        return jsonify({
            "reviews": response_data,
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


@analytics_bp.route('/product-reviews', methods=['GET'])
def get_all_active_reviews():
     
    """-------------------------------Pobiera wszystkie zatwierdzone reviews-------------------------------"""
    
    all_active_reviews = ProductReviews.query.filter_by(is_approved=True).all()
    return jsonify([review.to_json_user_view() for review in all_active_reviews]), 200