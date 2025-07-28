from flask import Blueprint, request, jsonify
from backend import db
from backend.models import Categories
from flask_jwt_extended import get_jwt_identity, jwt_required
from backend.utils import role_required

catalog_bp = Blueprint('catalog', __name__, url_prefix='/api/catalog')

## ###################################################################### Kategorie ######################################################################

@catalog_bp.route('/categories', methods=['GET']) # przy ładowaniu strony głównej pobieramy kategorie główne
def get_root_categories():
    categories = Categories.query.filter_by(parent_id=None).all()
    return jsonify([category.to_json() for category in categories])

@catalog_bp.route('/categories/<int:parent_id>/children', methods=['GET']) # pobieramy kategorie podrzędne dla danej kategorii głównej
def get_child_categories(parent_id):
    children = Categories.query.filter_by(parent_id=parent_id).all()
    return jsonify([child.to_json() for child in children])

@catalog_bp.route('/add_category', methods=['POST'])
@jwt_required()
@role_required('admin')
def add_category():

    """-------------------------------Dodanie nowej kategorii-------------------------------"""

    try:
        
        data = request.get_json()

        if not data.get('name') or Categories.query.filter_by(name=data['name']).first():
            return jsonify({"error": "Name is required and must be unique"}), 400

        new_category = Categories(
            name=data.get('name'), 
            parent_id=data.get('parent_id')
        
        )
        db.session.add(new_category)
        db.session.commit()

        return jsonify({'message': 'Category created successfully',
                        'category': new_category.to_json()
                        }), 201

    except Exception as e:
            db.session.rollback()
            print(f"[ERROR]: {str(e)}")
            return jsonify({'error': 'Internal server error'}), 500

@catalog_bp.route('/delete_category/<int:category_id>', methods=['DELETE'])
@jwt_required()
@role_required('admin')
def delete_category(category_id):

    """-------------------------------Usunięcie kategorii-------------------------------"""

    try:

        category = Categories.query.get(category_id)
  
        if not category:
            return jsonify({"error": "Category not found"}), 404
        
        category_name = {
            'name': category.name,
        }

        db.session.delete(category)
        db.session.commit()

        return jsonify({
            "message": "Category deleted successfully",
            "category": category_name
        }), 200

    except Exception as e:
        db.session.rollback()
        print(f"[ERROR]: {str(e)}")
        return jsonify({'error': 'Internal server error'}), 500


## ###################################################################### Atrybuty ######################################################################