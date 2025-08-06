from flask import Blueprint, request, jsonify
from backend import db
from backend.models import DeliveryMethods
from flask_jwt_extended import jwt_required
from backend.utils import role_required
## from sqlalchemy import func

commerce_bp = Blueprint('commerce', __name__, url_prefix='/api/commerce')

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
def delete_promotion(delivery_id):

    """-------------------------------Usunięcie danej promocji-------------------------------"""

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
