from flask import Blueprint, request, jsonify
from backend import db
from backend.models import Categories, Attributes, Products
from flask_jwt_extended import get_jwt_identity, jwt_required
from backend.utils import role_required

catalog_bp = Blueprint('catalog', __name__, url_prefix='/api/catalog')

## ###################################################################### Kategorie ######################################################################


@catalog_bp.route('/all_categories', methods=['GET'])
@jwt_required()
@role_required('admin')
def get_all_categories():

    """-----------------------------Pobranie wszystkich kategorii-------------------------------"""

    categories = Categories.query.all()
    return jsonify([category.to_json() for category in categories])


@catalog_bp.route('/root_categories', methods=['GET']) # przy ładowaniu strony głównej pobieramy kategorie główne
def get_root_categories():

    """-------------------------------Pobranie kategorii głównych-------------------------------"""

    categories = Categories.query.filter(
        Categories.parent_id == None,
        Categories.isused == True
    ).all()
    return jsonify([category.to_json() for category in categories])


@catalog_bp.route('/child_categories/<int:whose_child_id>', methods=['GET']) # pobieramy kategorie podrzędne dla danej kategorii głównej
def get_child_categories(whose_child_id):

    """-------------------------------Pobranie kategorii podrzędnych-------------------------------"""

    children = Categories.query.filter(
        Categories.parent_id == whose_child_id,
        Categories.isused == True
    ).all()
    
    return jsonify([child.to_json() for child in children])


@catalog_bp.route('/add_category', methods=['POST'])
@jwt_required()
@role_required('admin')
def add_category():

    """-------------------------------Dodanie nowej kategorii-------------------------------"""

    try:
        
        data = request.get_json()

        if not data.get('name') or Categories.query.filter_by(name=data['name']).first():
            return jsonify({"error": "Category name is required and must be unique"}), 400

        new_category = Categories(
            name=data.get('name'), 
            parent_id=data.get('parent_id'),
            isused=data.get('isused', True)  # domyślnie kategoria jest używana
        
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
    

@catalog_bp.route('/modify_category/<int:category_id>', methods=['PUT'])
@jwt_required()
@role_required('admin')
def modify_category(category_id):

    """-------------------------------Modyfikacja kategorii-------------------------------"""

    try:

        category = Categories.query.get(category_id)

        if not category:
            return jsonify({"error": "Category not found"}), 404

        data = request.get_json()

        category.name = data.get('name', category.name)
        category.parent_id = data.get('parent_id', category.parent_id)
        category.isused = data.get('isused', category.isused)

        db.session.commit()

        return jsonify({
            "message": "Category modified successfully",
            "category": category.to_json()
        }), 200

    except Exception as e:
        db.session.rollback()
        print(f"[ERROR]: {str(e)}")
        return jsonify({'error': 'Internal server error'}), 500


## ###################################################################### Atrybuty ######################################################################

@catalog_bp.route('/add_atribute', methods=['POST'])
@jwt_required()
@role_required('admin')
def add_attribute():

    """-------------------------------Dodanie nowego atrybutu-------------------------------"""

    try:

        data = request.get_json()

        if not data.get('name') or Attributes.query.filter_by(name=data['name']).first():
            return jsonify({"error": "Attribute name is required and must be unique"}), 400

        new_attribute = Attributes(
            name=data.get('name')
        )
        db.session.add(new_attribute)
        db.session.commit()

        return jsonify({'message': 'Attribute created successfully',
                        'attribute': new_attribute.to_json()
                        }), 201

    except Exception as e:
        db.session.rollback()
        print(f"[ERROR]: {str(e)}")
        return jsonify({'error': 'Internal server error'}), 500
    

@catalog_bp.route('/delete_attribute/<int:attribute_id>', methods=['DELETE'])
@jwt_required()
@role_required('admin')
def delete_attribute(attribute_id):

    """-------------------------------Usunięcie atrybutu-------------------------------"""

    try:

        attribute = Attributes.query.get(attribute_id)

        if not attribute:
            return jsonify({"error": "Attribute not found"}), 404

        attribute_name = {
            'name': attribute.name,
        }

        db.session.delete(attribute)
        db.session.commit()

        return jsonify({
            "message": "Attribute deleted successfully",
            "attribute": attribute_name
        }), 200

    except Exception as e:
        db.session.rollback()
        print(f"[ERROR]: {str(e)}")
        return jsonify({'error': 'Internal server error'}), 500


@catalog_bp.route('/all_attributes', methods=['GET'])
@jwt_required()
@role_required('admin')
def get_all_attributes():

    """-----------------------------Pobranie wszystkich atrybutów-------------------------------"""

    attributes = Attributes.query.all()
    return jsonify([attribute.to_json() for attribute in attributes])
    
## ###################################################################### Produkty ######################################################################

@catalog_bp.route('/add_product', methods=['POST'])
@jwt_required()
@role_required('admin')
def add_product():

    """-------------------------------Dodanie nowego produktu-------------------------------"""

    try:

        data = request.get_json()

        required_fields = ['category_id', 'name', 'description', 'image', 'quantity', 'unit_price']
        for field in required_fields:
            if not data.get(field):
                return jsonify({'error': f'{field} is required'}), 400
        
        if not Categories.validate_category_id(data.get('category_id')):
            return jsonify({"error": "Invalid category"}), 400

        if not data.get('name') or Products.query.filter_by(name=data['name']).first():
            return jsonify({"error": "Product name is required and must be unique"}), 400

        new_product = Products(
            category_id=data.get('category_id'),
            name=data.get('name'),
            description=data.get('description'),
            image=data.get('image'),
            quantity=data.get('quantity', 0),
            unit_price=data.get('unit_price', 0)
        )
        db.session.add(new_product)
        db.session.commit()

        return jsonify({'message': 'Product created successfully',
                        'product': new_product.to_json()
                        }), 201

    except Exception as e:
        db.session.rollback()
        print(f"[ERROR]: {str(e)}")
        return jsonify({'error': 'Internal server error'}), 500
    

@catalog_bp.route('/delete_product/<int:product_id>', methods=['DELETE'])
@jwt_required()
@role_required('admin')
def delete_product(product_id):

    """-------------------------------Usunięcie produktu-------------------------------"""

    try:

        product = Products.query.get(product_id)
        category = Categories.query.get(product.category_id)

        if not product:
            return jsonify({"error": "Product not found"}), 404

        product_name = {
            'name': product.name,
            'category': category.name
        }

        db.session.delete(product)
        db.session.commit()

        return jsonify({
            "message": "Product deleted successfully",
            "product": product_name
        }), 200

    except Exception as e:
        db.session.rollback()
        print(f"[ERROR]: {str(e)}")
        return jsonify({'error': 'Internal server error'}), 500