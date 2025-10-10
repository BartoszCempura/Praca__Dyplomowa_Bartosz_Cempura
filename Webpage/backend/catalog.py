from flask import Blueprint, request, jsonify
from backend import db
from backend.models import Categories, Attributes, Products, ProductAttributes, AttributeWeights, ProductAccessories, Promotions, ProductPromotions
from flask_jwt_extended import jwt_required
from backend.utils import role_required
from sqlalchemy import func

catalog_bp = Blueprint('catalog', __name__, url_prefix='/api/catalog')


## ###################################################################### Kategorie ######################################################################


@catalog_bp.route('/admin/categories', methods=['GET'])
@jwt_required()
@role_required('admin')
def get_all_categories():

    """-----------------------------Pobranie wszystkich kategorii przez administratora-------------------------------"""

    categories = Categories.query.all()
    return jsonify([category.to_json() for category in categories])


@catalog_bp.route('/categories', methods=['GET']) # przy ładowaniu strony głównej pobieramy kategorie główne
def get_root_categories():

    """-------------------------------Pobranie kategorii głównych-------------------------------"""

    categories = Categories.query.filter(
        Categories.parent_id == None,
        Categories.isused == True
    ).all()
    return jsonify([category.to_json() for category in categories])


@catalog_bp.route('/categories/<int:whose_child_id>', methods=['GET']) # pobieramy kategorie podrzędne dla danej kategorii głównej
def get_child_categories(whose_child_id):

    """-------------------------------Pobranie kategorii podrzędnych-------------------------------"""

    children = Categories.query.filter(
        Categories.parent_id == whose_child_id,
        Categories.isused == True
    ).all()
    
    return jsonify([child.to_json() for child in children])


@catalog_bp.route('/admin/categories', methods=['POST'])
@jwt_required()
@role_required('admin')
def add_category():

    """-------------------------------Dodanie nowej kategorii przez administratora-------------------------------"""

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
    

@catalog_bp.route('/admin/categories/<int:category_id>', methods=['DELETE'])
@jwt_required()
@role_required('admin')
def delete_category(category_id):

    """-------------------------------Usunięcie kategorii przez administratora-------------------------------"""

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
    

@catalog_bp.route('/admin/categories/<int:category_id>', methods=['PUT'])
@jwt_required()
@role_required('admin')
def modify_category(category_id):

    """-------------------------------Modyfikacja kategorii przez administratora-------------------------------"""

    try:
        # zastosowanie w przypadkach gdy użytkonik chce przypisac kategorii parent_id albo zmienić jej status na nieużywaną
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


@catalog_bp.route('/admin/attributes', methods=['POST'])
@jwt_required()
@role_required('admin')
def add_attribute():

    """-------------------------------Dodanie nowego atrybutu przez administratora-------------------------------"""

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
    

@catalog_bp.route('/admin/attributes/<int:attribute_id>', methods=['DELETE'])
@jwt_required()
@role_required('admin')
def delete_attribute(attribute_id):

    """-------------------------------Usunięcie atrybutu przez administratora-------------------------------"""

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


@catalog_bp.route('/admin/attributes', methods=['GET'])
@jwt_required()
@role_required('admin')
def get_all_attributes():

    """-----------------------------Pobranie wszystkich atrybutów przez administratora-------------------------------"""

    attributes = Attributes.query.all()
    return jsonify([attribute.to_json() for attribute in attributes])

    
## ###################################################################### Produkty ######################################################################


@catalog_bp.route('/admin/products', methods=['POST'])
@jwt_required()
@role_required('admin')
def add_product():

    """-------------------------------Dodanie nowego produktu przez administratora-------------------------------"""

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
    

@catalog_bp.route('/admin/products/<int:product_id>', methods=['DELETE'])
@jwt_required()
@role_required('admin')
def delete_product(product_id):

    """-------------------------------Usunięcie produktu przez administratora-------------------------------"""

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
    

@catalog_bp.route('/admin/products', methods=['GET'])
@jwt_required()
@role_required('admin')
def get_all_products():

    """-----------------------------Pobranie wszystkich produktów dla administratora-------------------------------"""

    products = Products.query.all()
    return jsonify([product.to_json() for product in products])
# tutaj warto było by dodać paginacje


@catalog_bp.route('/products/<string:category_slug>', methods=['GET'])
def get_products_by_category_slug(category_slug):

    """-------------------------------Pobieranie produktów po slug kategorii z paginacją-------------------------------"""

    try:
        # endpoint używany do wyświelania produktów w danej kategorii na stronie głównej
        # slug jest unikalnym identyfikatorem kategorii, który jest używany w URL
        page = request.args.get('page', 1, type=int)
        per_page = request.args.get('limit', 20, type=int)

        category = Categories.query.filter_by(slug=category_slug, isused=True).first()
        if not category:
            return jsonify({"error": "Category not found"}), 404

        pagination = Products.query.filter_by(category_id=category.id).paginate(
            page=page, per_page=per_page, error_out=False
        )

        return jsonify({
            "products": [product.to_json() for product in pagination.items],
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
    

@catalog_bp.route('/admin/products/<int:product_id>', methods=['PUT'])
@jwt_required()
@role_required('admin')
def modify_product(product_id):

    """-------------------------------Modyfikacja danych produktu przez administratora-------------------------------"""

    try:

        product = Products.query.get(product_id)

        if not product:
            return jsonify({"error": "Product not found"}), 404

        data = request.get_json()

        category = data.get('category_id', product.category_id) # jeżeli podano id kategorii to sprawdzamy czy jest poprawne

        if category is not None:
            if not Categories.validate_category_id(category):
                return jsonify({"error": "Invalid category"}), 400
            product.category_id = category
        
        new_name = data.get('name', product.name) # jeżeli podano nazwe to sprawdzamy czy jest unikalna
        
        if new_name and new_name != product.name:
            if Products.query.filter_by(name=new_name).first():
                return jsonify({"error": "Product name must be unique"}), 400
            product.name = new_name

        product.category_id = category
        product.name = new_name
        product.description = data.get('description', product.description)
        product.image = data.get('image', product.image)
        product.quantity = data.get('quantity', product.quantity)
        product.unit_price = data.get('unit_price', product.unit_price)

        db.session.commit()

        return jsonify({
            "message": "Product modified successfully",
            "product": product.to_json()
        }), 200

    except Exception as e:
        db.session.rollback()
        print(f"[ERROR]: {str(e)}")
        return jsonify({'error': 'Internal server error'}), 500
    

@catalog_bp.route('/products', methods=['GET'])
def search_products():

    """-------------------------------Wyszukiwanie produktów po wartości argumentu search-------------------------------"""

    try:

        search_value = request.args.get('search', '', type=str)
        page = request.args.get('page', 1, type=int)
        per_page = request.args.get('limit', 20, type=int)

        if search_value:
            results = Products.query.filter(func.lower(Products.name).contains(search_value.lower())) # pobieramy nazwy produktów, zmniejszmay rozmiar liter i to samo robimy dla wyszukiwanego ciągu znaków
            # następnie sprawdzamy czy nazwa produktu zawiera wyszukiwany ciąg znaków
        else:
            results = Products.query # jeśli nie ma wartości wyszukiwania, zwracamy wszystkie produkty

        pagination = results.paginate(page=page, per_page=per_page, error_out=False)
        products = pagination.items

        return jsonify({
            "products": [product.to_json() for product in products],
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


## ###################################################################### Atrybuty produktów ######################################################################


@catalog_bp.route('/admin/product-attributes', methods=['POST'])
@jwt_required()
@role_required('admin')
def connect_attribute_to_product():

    """-------------------------------Dodanie nowego atrybutu dla produktu przez administratora-------------------------------"""

    try:

        data = request.get_json()

        required_fields = ['product_id', 'attributes']
        for field in required_fields:
            if not data.get(field):
                return jsonify({'error': f'{field} is required'}), 400

        if not Products.query.get(data.get('product_id')):
            return jsonify({"error": "Invalid product"}), 400
        
        attributes_data = data.get('attributes', [])

        created_connections = []

        for attribute in attributes_data:
            attribute_id = attribute.get('attribute_id')
            value = attribute.get('value')

            if not attribute_id or not value:
                return jsonify({"error": "Attribute id and value are required"}), 400

            if not Attributes.query.get(attribute_id):
                return jsonify({"error": f"Invalid attribute {attribute_id}"}), 400
            
            existing = ProductAttributes.query.filter(
                ProductAttributes.product_id==data.get('product_id'),
                ProductAttributes.attribute_id==attribute_id
            ).first()

            if existing:
                return jsonify({'error': 'Attribute already connected to product'}), 400

            new_attribute = ProductAttributes(
                product_id=data.get('product_id'),
                attribute_id=attribute_id,
                value=value
            )
            db.session.add(new_attribute)
            created_connections.append(new_attribute)

        db.session.commit()

        return jsonify({'message': f'Successfully added {len(created_connections)} attributes to product'}), 201

    except Exception as e:
        db.session.rollback()
        print(f"[ERROR]: {str(e)}")
        return jsonify({'error': 'Internal server error'}), 500
    

"""
# postman: http://127.0.0.1:5000/api/catalog/product-attributes/2 metoda GET

@catalog_bp.route('/product-attributes/<int:product_id>', methods=['GET'])
def get_all_attributes_of_product(product_id):

    #-------------------------------Pobranie name oraz value atrybutów dla danego produktu-------------------------------

    try:
        # endpoint używany do pobierania atrybutów produktu na stronie produktu
        # zwraca tylko nazwy atrybutów i ich wartości
        product = Products.query.get(product_id)
        if not product:
            return jsonify({'error': 'Product not found'}), 404

        results = db.session.query(
            Attributes.name,
            ProductAttributes.value
        ).join(Attributes, ProductAttributes.attribute_id == Attributes.id
        ).filter(ProductAttributes.product_id == product_id).all() #łączymy dwie tabele: ProductAttributes i Attributes, aby pobrać nazwy atrybutów i ich wartości dla danego produktu

        return jsonify([{'name': name, 'value': value} for name, value in results]), 200

    except Exception as e:
        print(f"[ERROR]: {str(e)}")
        return jsonify({'error': 'Internal server error'}), 500
"""
    
@catalog_bp.route('/products/<int:product_id>', methods=['GET'])
def get_product_details(product_id):

    """-------------------------------Pobranie pełnych danych produktu wraz z atrybutami i ceną z rabatem-------------------------------"""

    try:
        product = Products.query.get(product_id)
        if not product:
            return jsonify({'error': 'Product not found'}), 404

        # Pobieramy atrybuty
        attributes = db.session.query(
            Attributes.name,
            ProductAttributes.value
        ).join(
            Attributes, ProductAttributes.attribute_id == Attributes.id
        ).filter(
            ProductAttributes.product_id == product_id
        ).all()

        return jsonify({
            "product": product.to_json_description_view(), # nie wiem czy nie będzie tutaj trzeba dać prostrzego wglądu, bez kategorii , updated at itd
            "attributes": [{"name": name, "value": value} for name, value in attributes]
        }), 200

    except Exception as e:
        print(f"[ERROR]: {str(e)}")
        return jsonify({'error': 'Internal server error'}), 500
    
    
@catalog_bp.route('/admin/product-attributes/<int:product_id>', methods=['GET'])
@jwt_required()
@role_required('admin')
def get_full_attribute_and_product_connection_info(product_id):

    """-------------------------------Pobranie pełnych danych atrybutu dla produktu prze administratora-------------------------------"""

    try:
        ## dla panelu administratora gdzie będą potrzebne wszystkie informacje o połączeniu atrybutu z produktem
        product = Products.query.get(product_id)
        if not product:
            return jsonify({'error': 'Product not found'}), 404
        
        results = ProductAttributes.query.filter_by(product_id=product_id).all()

        return jsonify([result.to_json() for result in results]), 200

    except Exception as e:
        print(f"[ERROR]: {str(e)}")
        return jsonify({'error': 'Internal server error'}), 500
    
    

@catalog_bp.route('/admin/product-attributes/<int:connection_id>', methods=['DELETE'])
@jwt_required()
@role_required('admin')
def delete_attribute_product_connection(connection_id):

    """-------------------------------Usunięcie połączenia atrybutu z produktem-------------------------------"""

    try:

        ## powinien być używany z ADMIN get_full_attribute_and_product_connection_info

        connection = ProductAttributes.query.get(connection_id)

        if not connection:
            return jsonify({'error': 'There is no such connection'}), 404
        
        product = Products.query.get(connection.product_id)
        attribute = Attributes.query.get(connection.attribute_id)

        deleted_connection = {
            'product': product.name if product else None,
            'attribute': attribute.name if attribute else None
        }

        db.session.delete(connection)
        db.session.commit()

        return jsonify({
            "message": "Connection deleted successfully",
            "product": deleted_connection['product'],
            "attribute": deleted_connection['attribute']
        }), 200

    except Exception as e:
        db.session.rollback()
        print(f"[ERROR]: {str(e)}")
        return jsonify({'error': 'Internal server error'}), 500
    
    
    
@catalog_bp.route('/admin/product-attributes/<int:ProductAttributes_id>', methods=['PUT'])
@jwt_required()
@role_required('admin')
def modify_connection_value(ProductAttributes_id):

    """-------------------------------Modyfikacja wartości połączenia atrybutu z produktem-------------------------------"""  

    try:

        data = request.get_json()

        connection = ProductAttributes.query.get(ProductAttributes_id)

        if not connection:
            return jsonify({'error': 'There is no such connection'}), 400

        connection.value = data.get('value', connection.value)

        db.session.commit()

        return jsonify({
            "message": "Product aattribute value modified successfully",
            "product": connection.to_json()
        }), 200

    except Exception as e:
        db.session.rollback()
        print(f"[ERROR]: {str(e)}")
        return jsonify({'error': 'Internal server error'}), 500
    

## ###################################################################### wagi atrybutów ######################################################################


@catalog_bp.route('/admin/attribute-weights', methods=['POST'])
@jwt_required()
@role_required('admin')
def add_attribute_weight_for_category():

    """-------------------------------Dodawanie wagi kategorii dla produktu przez administratora-------------------------------"""  

    try:
        data = request.get_json()

        required_fields = ['attribute_id', 'category_id', 'weight']
        for field in required_fields:
            if not data.get(field):
                return jsonify({'error': f'{field} is required'}), 400

        if not Attributes.query.get(data.get('attribute_id')):
            return jsonify({"error": "Invalid attribute"}), 400

        if not Categories.validate_category_id(data.get('category_id')):
            return jsonify({"error": "Invalid category"}), 400
        
        existing_entry = AttributeWeights.query.filter(
            AttributeWeights.attribute_id == data.get('attribute_id'),
            AttributeWeights.category_id == data.get('category_id')
        ).first()

        if existing_entry:
            return jsonify({'error': 'This attribute is already assigned to the given category'}), 400


        set_up_weight = AttributeWeights(
            attribute_id=data.get('attribute_id'),
            category_id=data.get('category_id'),
            weight=data.get('weight')
        )
        db.session.add(set_up_weight)
        db.session.commit()


        return jsonify({
            "message": "Category weight for product set succesfully",
            "product": set_up_weight.to_json()
        }), 200

    except Exception as e:
        db.session.rollback()
        print(f"[ERROR]: {str(e)}")
        return jsonify({'error': 'Internal server error'}), 500
    
    

@catalog_bp.route('/admin/attribute-weights/<int:AttributeWeights_id>', methods=['DELETE'])
@jwt_required()
@role_required('admin')
def delete_attribute_category_weight(AttributeWeights_id):

    """-------------------------------Usunięcie wagi kategorii przez administratora-------------------------------"""

    try:

        attribute_weight = AttributeWeights.query.get(AttributeWeights_id)

        if not attribute_weight:
            return jsonify({'error': 'There is no such attribute weight'}), 404
        
        attribute = Attributes.query.get(attribute_weight.attribute_id)
        category = Categories.query.get(attribute_weight.category_id)

        deleted_connection = {
            'attribute': attribute.name if attribute else None,
            'category': category.name if category else None
        }

        db.session.delete(deleted_connection)
        db.session.commit()

        return jsonify({
            "message": "Connection deleted successfully",
            "product": deleted_connection['attribute'],
            "attribute": deleted_connection['category']
        }), 200
    

    except Exception as e:
        db.session.rollback()
        print(f"[ERROR]: {str(e)}")
        return jsonify({'error': 'Internal server error'}), 500
    

@catalog_bp.route('/admin/attribute-weights/<int:AttributeWeights_id>', methods=['PUT'])
@jwt_required()
@role_required('admin')
def modify_attribute_weight(AttributeWeights_id):

    """-------------------------------Modyfikacja wartości połączenia atrybutu z produktem przez administratora-------------------------------"""  

    try:

        data = request.get_json()

        attribute_weight = AttributeWeights.query.get(AttributeWeights_id)

        if not attribute_weight:
            return jsonify({'error': 'There is no such attribute weight'}), 404

        attribute_weight.weight = data.get('weight', attribute_weight.weight)

        db.session.commit()

        return jsonify({
            "message": "Product attribute value modified successfully",
            "product": attribute_weight.to_json()
        }), 200

    except Exception as e:
        db.session.rollback()
        print(f"[ERROR]: {str(e)}")
        return jsonify({'error': 'Internal server error'}), 500
    

    
@catalog_bp.route('/admin/attribute-weights/<int:category_id>', methods=['GET'])
@jwt_required()
@role_required('admin')
def get_attribute_weights_for_category(category_id):

    """-------------------------------Zwraca wszystkie atrybuty dla wybranej kategorii dla administratora-------------------------------"""  

    try:

        if not Categories.validate_category_id(category_id):
            return jsonify({"error": "Invalid category"}), 400

        results = AttributeWeights.query.filter_by(category_id=category_id).all()

        if not results:
            return jsonify({'error': 'There are no attribute weights for this category'}), 404

        return jsonify([result.to_json() for result in results]), 200

    except Exception as e:
        print(f"[ERROR]: {str(e)}")
        return jsonify({'error': 'Internal server error'}), 500


## ###################################################################### Akcesoria dla produktu ######################################################################


@catalog_bp.route('/admin/product-accessories', methods=['POST'])
@jwt_required()
@role_required('admin')
def add_product_accessory_relation():

    """-------------------------------Dodawanie relacji między akcesorium a produktem przez administratora-------------------------------"""

    try:

        data = request.get_json()

        required_fields = ['product_id', 'accessory_product_id']
        for field in required_fields:
            if not data.get(field):
                return jsonify({'error': f'{field} is required'}), 400

        if not Products.query.get(data.get('product_id')):
            return jsonify({"error": "Invalid product"}), 400

        if not Products.query.get(data.get('accessory_product_id')):
            return jsonify({"error": "Invalid product"}), 400
        
        existing_entry = ProductAccessories.query.filter(
            ProductAccessories.product_id == data.get('product_id'),
            ProductAccessories.accessory_product_id == data.get('accessory_product_id')
        ).first()

        if existing_entry:
            return jsonify({'error': 'This attribute is already assigned to the given category'}), 400


        set_up_accessory = ProductAccessories(
            product_id=data.get('product_id'),
            accessory_product_id=data.get('accessory_product_id'),
            weight=data.get('weight')
        )
        db.session.add(set_up_accessory)
        db.session.commit()


        return jsonify({
            "message": "Accessory for product set succcess",
            "product": set_up_accessory.to_json()
        }), 200

    except Exception as e:
        db.session.rollback()
        print(f"[ERROR]: {str(e)}")
        return jsonify({'error': 'Internal server error'}), 500
    
    

@catalog_bp.route('/admin/product-accessories/<int:relation_id>', methods=['DELETE'])
@jwt_required()
@role_required('admin')
def delete_product_accessory_relation(relation_id):

    """-------------------------------Usunięcie relacji akcesorium z produktem przez administratora-------------------------------"""


    try:

        accessory_relation = ProductAccessories.query.get(relation_id)

        if not accessory_relation:
            return jsonify({'error': 'There is no such accessory relation'}), 404
        
        product = Products.query.get(accessory_relation.product_id)
        accessory = Products.query.get(accessory_relation.accessory_product_id)

        deleted_connection ={
            "product": product.name,
            "accessory": accessory.name
        }

        db.session.delete(accessory_relation)
        db.session.commit()

        return jsonify({
            "message": "Connection deleted successfully",
            "product": deleted_connection['product'],
            "attribute": deleted_connection['accessory']
        }), 200

    except Exception as e:
        db.session.rollback()
        print(f"[ERROR]: {str(e)}")
        return jsonify({'error': 'Internal server error'}), 500
    

@catalog_bp.route('/admin/product-accessories/<int:relation_id>', methods=['PUT'])
@jwt_required()
@role_required('admin')
def modify_relation_weight(relation_id):

    """-------------------------------Modyfikacja wartości wagi dla relacji akcesorium produkt przez administratora-------------------------------"""  

    try:

        data = request.get_json()

        relation_weight = ProductAccessories.query.get(relation_id)

        if not relation_weight:
            return jsonify({'error': 'There is no such relation'}), 404

        relation_weight.weight = data.get('weight', relation_weight.weight)

        db.session.commit()

        return jsonify({
            "message": "Product aattribute value modified successfully",
            "product": relation_weight.to_json()
        }), 200

    except Exception as e:
        db.session.rollback()
        print(f"[ERROR]: {str(e)}")
        return jsonify({'error': 'Internal server error'}), 500
    

    
@catalog_bp.route('/admin/product-accessories/<int:product_id>', methods=['GET'])
@jwt_required()
@role_required('admin')
def get_all_accessories_for_product(product_id):

    """-------------------------------Zwraca wszystkie akcesoria w relacji z produktem dla administratora-------------------------------"""  

    try:

        if not Products.query.get(product_id):
            return jsonify({"error": "Invalid product"}), 400

        results = ProductAccessories.query.filter_by(product_id=product_id).all()

        if not results:
            return jsonify({'error': 'There are no accessories for this product'}), 404

        return jsonify([result.to_json() for result in results]), 200

    except Exception as e:
        print(f"[ERROR]: {str(e)}")
        return jsonify({'error': 'Internal server error'}), 500



## ###################################################################### Promocje ######################################################################


@catalog_bp.route('/admin/promotions', methods=['POST'])
@jwt_required()
@role_required('admin')
def add_promotion():

    """-------------------------------Dodawanie promocji przez administratora-------------------------------"""

    try:

        data = request.get_json()

        required_fields = ['name', 'discount_percent', 'start_date', 'end_date']
        for field in required_fields:
            if not data.get(field):
                return jsonify({'error': f'{field} is required'}), 400

        if Promotions.query.filter_by(name=data.get('name')).first():
            return jsonify({"error": "A promotion with this name already exists"}), 409

        if not Promotions.validate_discount(data.get('discount_percent')):
            return jsonify({"error": "Discount needs to be bigger than 0%"}), 400

        if not Promotions.validate_promotion_live(data.get('start_date'), data.get('end_date')):
            return jsonify({"error": "The end date must be later than the start date"})

        set_up_promotion = Promotions(
            name=data.get('name'),
            discount_percent=data.get('discount_percent'),
            start_date=data.get('start_date'),
            end_date=data.get('end_date')
        )
        db.session.add(set_up_promotion)
        db.session.commit()


        return jsonify({
            "message": "Adding Promotion successsfull",
            "product": set_up_promotion.to_json()
        }), 200

    except Exception as e:
        db.session.rollback()
        print(f"[ERROR]: {str(e)}")
        return jsonify({'error': 'Internal server error'}), 500
    
    

@catalog_bp.route('/admin/promotions/<int:promotion_id>', methods=['DELETE'])
@jwt_required()
@role_required('admin')
def delete_promotion(promotion_id):

    """-------------------------------Usunięcie danej promocji przez administratora-------------------------------"""

    try:

        promotion = Promotions.query.get(promotion_id)

        if not promotion:
            return jsonify({'error': 'There is no promotion with such id'}), 404
        
        promotion_name = {
            "name": promotion.name
        }

        db.session.delete(promotion)
        db.session.commit()

        return jsonify({
            "message": "Promotion deletion successsfull",
            "Promotion": promotion_name.to_json()
        }), 200

    except Exception as e:
        db.session.rollback()
        print(f"[ERROR]: {str(e)}")
        return jsonify({'error': 'Internal server error'}), 500
    

@catalog_bp.route('/admin/promotions/<int:promotion_id>', methods=['PUT'])
@jwt_required()
@role_required('admin')
def modify_promotion(promotion_id):

    """-------------------------------Modyfikacja zasad, danych danej promocji przez administratora-------------------------------"""  

    try:

        data = request.get_json()

        promotion = Promotions.query.get(promotion_id)

        if not promotion:
            return jsonify({'error': 'There is no promotion with such id'}), 404

        promotion.name = data.get('name', promotion.name)
        promotion.discount_percent = data.get('discount_percent', promotion.discount_percent)
        promotion.start_date = data.get('start_date', promotion.start_date)
        promotion.end_date = data.get('end_date', promotion.end_date)

        db.session.commit()

        return jsonify({
            "message": "Promotion data modified successfully",
            "product": promotion.to_json()
        }), 200

    except Exception as e:
        db.session.rollback()
        print(f"[ERROR]: {str(e)}")
        return jsonify({'error': 'Internal server error'}), 500
    

    
@catalog_bp.route('/admin/promotions', methods=['GET'])
@jwt_required()
@role_required('admin')
def get_all_promotions():

    """-------------------------------Zwraca wszystkie promocje dla administratora-------------------------------"""  

    promotions = Promotions.query.all()
    return jsonify([promotion.to_json() for promotion in promotions]), 200

## ###################################################################### Przypisywanie produktów do promocji ######################################################################

# react będzie przechowywał w usestate listę produktów które następnie będą przekazywane do endpoint dodającego promocje to bazy danych

@catalog_bp.route('/admin/product-promotions/<int:promotion_id>', methods=['POST'])
@jwt_required()
@role_required('admin')
def add_products_to_promotion(promotion_id):

    """-------------------------------Przypisywanie produktów do promocji przez administratora-------------------------------"""

    try:
        data = request.get_json()
        products_ids = data.get('product_ids') # przekazujemy do endpoint listę produktów 

        if not promotion_id or not products_ids:
            return jsonify({'error': 'promotion_id and product_ids are required'}), 400

        if not Promotions.query.get(promotion_id):
            return jsonify({'error': 'Promotion not found'}), 404

        added = []
        for product_id in products_ids:
            product = Products.query.get(product_id)
            if not product:
                continue  # sprawdzamy czy dany produkt istnieje, jak nie to go pomijamy
      # można tutaj doać listę skipped która przechowywała by listę odrzuconych i zwrócić ją w wyniku
            exists = ProductPromotions.query.filter_by(product_id=product_id).first() # sprawdzamy czy dany produkt jeż już w jakiejś promocji. Nie może być w 2 na raz

            if not exists:
                promotion_for_product = ProductPromotions()
                promotion_for_product.product_id = product_id
                promotion_for_product.promotion_id = promotion_id
                db.session.add(promotion_for_product)
                added.append(product_id)

        db.session.commit()

        return jsonify({
            'message': f'Added {len(added)} products to promotion',
            'product_ids': added
        }), 200

    except Exception as e:
        db.session.rollback()
        print(f"[ERROR]: {str(e)}")
        return jsonify({'error': 'Internal server error'}), 500



@catalog_bp.route('/product-promotions/<int:promotion_id>', methods=['GET'])
def get_all_products_in_promotion(promotion_id):

    """-------------------------------Pobieramy listę wszystkich produktów objętych promocją-------------------------------"""

    try:
        products = ProductPromotions.query.filter_by(promotion_id=promotion_id).all()
        if not products:
            return jsonify({'error': 'No products found for this promotion'}), 404
        
        return jsonify([product.to_json_user_view() for product in products]), 200
    
    except Exception as e:
        print(f"[ERROR]: {str(e)}")
        return jsonify({'error': 'Internal server error'}), 500
    

@catalog_bp.route('/admin/product-promotions/<int:product_id>', methods=['DELETE'])
@jwt_required()
@role_required('admin')
def remove_product_from_promotion(product_id):

    """-------------------------------Usunięcie produktu z promocji przez administratora-------------------------------"""
     
    try:

        products = ProductPromotions.query.filter_by(product_id=product_id).first()
        if not products:
            return jsonify({'error': 'This product was not added to this promotion'}), 404
        
        product = Products.query.get(products.product_id)

        removed = {
            "name": product.name
        }
        
        db.session.delete(products)
        db.session.commit()

        return jsonify({
            "message": "Product removed from promotion",
            "Product": removed
        }), 200
    
    except Exception as e:
        print(f"[ERROR]: {str(e)}")
        return jsonify({'error': 'Internal server error'}), 500

# można by zmodyfikować ten endpoint tak aby pozwalał na usunięcie wielu produktów z promocji na raz