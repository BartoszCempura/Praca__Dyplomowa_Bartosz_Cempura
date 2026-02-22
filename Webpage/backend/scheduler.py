
import os
from flask_apscheduler import APScheduler
from apscheduler.jobstores.sqlalchemy import SQLAlchemyJobStore
from sqlalchemy import MetaData
from datetime import datetime, timedelta, timezone

scheduler = APScheduler()

def clear_expired_carts():

    """-------------------------------Job usówania koszyków nieaktualizowanych przez 3 dni-------------------------------"""

    # Pobieramy instancję aplikacji z scheduler. Niezbędne aby uniknąć pętli importów
    app = scheduler.app
    
    with app.app_context():
        try:
            from . import db
            from .models import Carts
            
            print("clear_expired_carts job started")
            
            qualification_for_deletion = datetime.now(timezone.utc) - timedelta(hours=12)
            
            deleted_count = Carts.query.filter(
                Carts.updated_at <= qualification_for_deletion
            ).delete(synchronize_session=False)
            
            # Zatwierdzamy zmiany
            db.session.commit()
            deleted_when = datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M:%S UTC")
            print(f"Deleted {deleted_count} expired carts at {deleted_when}")
            
        except Exception as e:
            db.session.rollback()
            print(f"Error in clear_expired_carts job: {str(e)}")
            raise

def update_accesory_weight():

    """-------------------------------Job aktualizowania wagi akcesorium na bazie sprzedaży z okresu 30 dni-------------------------------"""

    app = scheduler.app
    
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
            # dla obsługi zmian wprowadzanych przez admina warto by dodać mechanizm wykluczający zerowanie wag przez niego zdefiniowanych np poprzez dodatkową kolumnę w tabeli ProductAccessories

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

def calculate_product_similarity():

    """-------------------------------Job wykonujący obliczanie podobieństwa produktów dla systemu rekomendacji-------------------------------"""
    app = scheduler.app
    
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
    
    database_url = os.environ.get('DATABASE_URL')
    metadata = MetaData(schema='utils')
    
    app.config.update({
        'SCHEDULER_JOBSTORES': {
            'default': SQLAlchemyJobStore(url=database_url, metadata=metadata)
        },
        'SCHEDULER_API_ENABLED': True,
        'SCHEDULER_TIMEZONE': 'UTC'
    })

    scheduler.init_app(app)
    scheduler.start()

    scheduler.remove_all_jobs()
    print("Removed all existing jobs from database")
    
    if not scheduler.get_job('clear_expired_carts_job'):
        scheduler.add_job(
            id='clear_expired_carts_job',
            func=clear_expired_carts,
            trigger='cron',
            hour=0,
            minute=0,
            replace_existing=True,
            max_instances=1
    )

    if not scheduler.get_job('update_accesory_weight_job'):
        scheduler.add_job(
            id='update_accesory_weight_job',
            func=update_accesory_weight,
            trigger='interval',   # 'interval' zamiast 'cron', bo chodzi o odstęp czasu
            days=30,              # co 30 dni
            replace_existing=True,
            max_instances=1
        )

    if not scheduler.get_job('calculate_product_similarity_job'):
        scheduler.add_job(
            id='calculate_product_similarity_job',
            func=calculate_product_similarity,
            trigger='interval',   # 'interval' zamiast 'cron', bo chodzi o odstęp czasu
            minutes=5,
            replace_existing=True,
            max_instances=1
        )

