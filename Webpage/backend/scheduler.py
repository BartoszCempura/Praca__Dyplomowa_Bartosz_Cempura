
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
            
            qualification_for_deletion = datetime.now(timezone.utc) - timedelta(days=3)
            
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
            from .models import ProductRecommendations, AttributeWeights, ProductAttributes, Attributes, Products, Categories
            from collections import defaultdict
            
            print("calculate_product_similarity job started")
            # Pobieramy wszystkie potrzebne dane z bazy
            complete_data = (
                db.session.query(
                    ProductAttributes.product_id,
                    Products.category_id,
                    ProductAttributes.attribute_id,
                    ProductAttributes.value,
                    AttributeWeights.weight
                )
                .join(Products, Products.id == ProductAttributes.product_id)
                .join(
                    AttributeWeights,
                    (AttributeWeights.attribute_id == ProductAttributes.attribute_id) &
                    (AttributeWeights.category_id == Products.category_id)
                )
                .all()
            )
            # Organizujemy dane w słowniki dla łatwiejszego dostępu
            product_attributes = defaultdict(list) # pod danym product_id trzymamy listę atrybutów
            categories_of_products = {} # przypisuje do product_id category_id
            for product_id, category_id, attribute_id, value, weight in complete_data:
                product_attributes[product_id].append({
                    "attribute_id": attribute_id,
                    "value": value,
                    "weight": float(weight)
                })
                categories_of_products[product_id] = category_id

            db.session.query(ProductRecommendations).delete() # Usuwamy stare rekomendacje

            product_ids = list(product_attributes.keys()) # Lista wszystkich product_id do porównania
            recommendations = [] # Lista do przechowywania nowych rekomendacji
            for single_product_id in product_ids:
                category = categories_of_products[single_product_id]

                for compare_product_id in product_ids:
                    if single_product_id == compare_product_id: # nie porównujemy produktu z samym sobą
                        continue
                    if categories_of_products[compare_product_id] != category: # porównujemy tylko produkty z tej samej kategorii
                        continue

                    score = 0.0
                    attributes_of_product_a = product_attributes[single_product_id]
                    attributes_of_product_b = product_attributes[compare_product_id]

                    for a_attribute in attributes_of_product_a:
                        for b_attribute in attributes_of_product_b:
                            if a_attribute["attribute_id"] == b_attribute["attribute_id"] and a_attribute["value"] == b_attribute["value"]: # atrybut musi być ten sam i mieć tę samą wartość
                                score += a_attribute["weight"] # wtedy dodajemy wagę atrybutu do wyniku

                    if score > 0:
                        recommendations.append(
                            ProductRecommendations(
                                product_id=single_product_id,
                                recommended_product_id=compare_product_id,
                                score=score
                            )
                        )

            db.session.bulk_save_objects(recommendations) # Zapisujemy nowe rekomendacje do bazy ale za jednym razem wszystkie a nie pojedynczo w pętli
            db.session.commit()
            print("Product similarity calculated successfully.")
            
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
    
    # Dodawanie innych jobą w ten sam sposób. Przy modyfikacji trzebausunąć stary wpis
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
            trigger='cron',
            hour=1,
            minute=0,
            replace_existing=True,
            max_instances=1
        )