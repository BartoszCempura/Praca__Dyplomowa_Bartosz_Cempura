
import os
from flask_apscheduler import APScheduler
from datetime import datetime, timedelta, timezone
from .seed import seed_database

scheduler = APScheduler()

def clear_expired_carts(app):

    """-------------------------------Job usówania koszyków nieaktualizowanych przez 3 dni-------------------------------"""

    
    with app.app_context():
        try:
            from . import db
            from .models import Carts, CartProducts, Products
            from .utils import load_product_map
            
            print("clear_expired_carts job started")
            
            qualification_for_deletion = datetime.now(timezone.utc) - timedelta(hours=12)
            
            deleted_count = 0
            expired_carts = Carts.query.filter(
                Carts.updated_at <= qualification_for_deletion
            ).all()
            expired_carts_ids = [cart.id for cart in expired_carts]
            cart_products = (
                CartProducts.query.with_entities(CartProducts.product_id)
                .filter(CartProducts.cart_id.in_(expired_carts_ids))
                .all()
            )

            product_counts ={}
            for (product_id,) in cart_products:
                if product_id in product_counts:
                    product_counts[product_id] += 1
                else:
                    product_counts[product_id] = 1

            products_to_be_returned = load_product_map(product_counts.keys())

            for product_id, count in product_counts.items():
                products_to_be_returned[product_id].quantity += count
            
            for cart in expired_carts:
                db.session.delete(cart)
                deleted_count += 1
            
            # Zatwierdzamy zmiany
            db.session.commit()
            deleted_when = datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M:%S UTC")
            print(f"Deleted {deleted_count} expired carts at {deleted_when}")
            
        except Exception as e:
            db.session.rollback()
            print(f"Error in clear_expired_carts job: {str(e)}")
            raise

def update_accesory_weight(app):

    """-------------------------------Job aktualizowania wagi akcesorium na bazie sprzedaży z okresu 30 dni-------------------------------"""
    
    with app.app_context():
        try:
            from . import db
            from .models import ProductAccessories, TransactionProducts, Transactions
            
            print("update_accesory_weight job started")
            
            thirty_days_ago = datetime.now(timezone.utc) - timedelta(days=30)
            
            all_product_accesory_relations = ProductAccessories.query.all()
            for pair in all_product_accesory_relations:
                pair.weight = 0.01
            db.session.commit()
            #TODO: dla obsługi zmian wprowadzanych przez admina warto by dodać mechanizm wykluczający zerowanie wag przez niego zdefiniowanych np poprzez dodatkową kolumnę w tabeli ProductAccessories

            recent_transactions = Transactions.query.filter(
                Transactions.created_at >= thirty_days_ago
            ).all()

            product_and_its_transaction = []
            for transaction in recent_transactions:
                products = TransactionProducts.query.filter_by(transaction_id=transaction.id).all()
                for product in products:
                    product_and_its_transaction.append(product)
            

            transactions_dict = {}
            for pair in product_and_its_transaction:
                if pair.transaction_id not in transactions_dict:
                    transactions_dict[pair.transaction_id] = []
                transactions_dict[pair.transaction_id].append(pair.product_id)
            

            product_accesory_pairs_dict = {}
            for pair in all_product_accesory_relations:
                key = (pair.product_id, pair.accessory_product_id)
                product_accesory_pairs_dict[key] = pair
            

            for transaction_id in transactions_dict:
                product_list = transactions_dict[transaction_id]
                product_list_sorted = sorted(product_list)
                
                for i in range(len(product_list_sorted)):
                    for j in range(i + 1, len(product_list_sorted)):
                        a = product_list_sorted[i]
                        b = product_list_sorted[j]
                        
                        if (a, b) in product_accesory_pairs_dict:
                            product_accesory_pairs_dict[(a, b)].weight += 0.01
            
            db.session.commit()
            print("Accessory weights updated successfully.")
            
        except Exception as e:
            db.session.rollback()
            print(f"Error in update_accesory_weight job: {str(e)}")
            raise

def calculate_product_similarity(app):

    """-------------------------------Job wykonujący obliczanie podobieństwa produktów dla systemu rekomendacji-------------------------------"""
    

    with app.app_context():
        try:
            from . import db
            from .models import ProductRecommendations, AttributeWeights, ProductAttributes,  Products
            from collections import defaultdict
            from sqlalchemy import text

            db.session.execute(text("ALTER SEQUENCE analytics.product_recommendations_id_seq RESTART WITH 1"))

            print("ROzpoczynam proces obliczania podomięństwamiędzy produktami...")
            products_data = (
                db.session.query(
                    Products.id.label('product_id'),
                    Products.category_id.label('category_id'),
                    ProductAttributes.attribute_id.label('attribute_id'),
                    ProductAttributes.value.label('value')
                )
                .join(ProductAttributes, Products.id == ProductAttributes.product_id)
                .all()
            )

            attribute_weights = (
                db.session.query(
                    AttributeWeights.category_id.label('category_id'),
                    AttributeWeights.attribute_id.label('attribute_id'),
                    AttributeWeights.weight.label('weight')
                )
                .all()
            )
            # słowniki z danymi dla łatwiejszego dostępu
            products_data_dict = defaultdict(list)
            for row in products_data:
                products_data_dict[row.product_id].append(row)
            attribute_weights_dict = {}
            for row in attribute_weights:
                attribute_weights_dict[(row.category_id, row.attribute_id)] = row.weight

            unique_categories = set()

            for attrs in products_data_dict.values():
                category_id = attrs[0].category_id
                unique_categories.add(category_id)

            unique_categories = sorted(unique_categories)

            product_similarity_scores = []

            for category_id in unique_categories:

                products_in_category = defaultdict(list)
                for product_id, attrs in products_data_dict.items():
                    if attrs[0].category_id == category_id:
                        products_in_category[product_id] = attrs

                attribute_weights_for_category = {}
                for (cat_id, attr_id), weight in attribute_weights_dict.items():
                    if cat_id == category_id:
                        attribute_weights_for_category[attr_id] = weight

                product_ids = list(products_in_category.keys())

                for i in range(len(product_ids)):
                    product_a_id = product_ids[i]
                    attributess_of_a = products_in_category[product_a_id]

                    for j in range(i + 1, len(product_ids)):
                        product_b_id = product_ids[j]
                        attributes_of_b = products_in_category[product_b_id]

                        score = 0.0

                        for attr_a in attributess_of_a:
                            for attr_b in attributes_of_b:
                                if attr_a.attribute_id == attr_b.attribute_id and attr_a.value == attr_b.value:
                                    weight = attribute_weights_for_category.get(attr_a.attribute_id, 0)
                                    score += float(weight)

                        if score > 0:
                            product_similarity_scores.append(
                                ProductRecommendations(
                                    product_id=product_a_id,
                                    recommended_product_id=product_b_id,
                                    score=round(score, 2)
                                )
                            )       

            db.session.query(ProductRecommendations).delete()
            print("Usówanie starych rekomendacji zakończone.")
            db.session.bulk_save_objects(product_similarity_scores)
            db.session.commit()
            print("Nowe rekomendacje produktów zostały zapisane w bazie danych.")

        except Exception as e:
            db.session.rollback()
            print(f"Error in calculate_product_similarity job: {str(e)}")
            raise

def run_seed(app):
    seed_database(app)

def should_run_scheduler():

    """-------------------------------Metoda do określenia warunków uruchomienia procesu scheduler-------------------------------"""

    ## w przypadku wprowadzenia konfiguracji dla środowiskaprodukcyjnego trzeba tu będzie dodać warunki np czy istnieje zmienna środowiskowa ENABLE_SCHEDULER=1

    if os.environ.get('WERKZEUG_RUN_MAIN') != 'true':
        return False  
    return True

def init_scheduler(app):

    """-------------------------------Inicjalizacja scheduler i konfiguracja.-------------------------------"""

    if not should_run_scheduler():
        return
    
    
    app.config.update({
        'SCHEDULER_JOBSTORES': {
            'default': {'type': 'memory'} 
        },
        'SCHEDULER_API_ENABLED': True,
        'SCHEDULER_TIMEZONE': 'UTC'
    })

    scheduler.init_app(app)
    scheduler.start()

    scheduler.add_job(
        id='clear_expired_carts_job',
        func=lambda:clear_expired_carts(app),
        trigger='cron',
        hour=1,
        minute=30,
        replace_existing=True,
        max_instances=1
    )


    scheduler.add_job(
        id='update_accesory_weight_job',
        func=lambda:update_accesory_weight(app),
        trigger='interval',
        days=30,
        replace_existing=True,
        max_instances=1
    )


    scheduler.add_job(
        id='calculate_product_similarity_job',
        func=lambda:calculate_product_similarity(app),
        trigger='cron',
        hour=1,
        minute=20, 
        replace_existing=True,
        max_instances=1
    )


    scheduler.add_job(
        id='seed_job',
        func=lambda:run_seed(app),
        trigger='cron',
        hour=1,
        minute=0,
        replace_existing=True,
        max_instances=1
    )


