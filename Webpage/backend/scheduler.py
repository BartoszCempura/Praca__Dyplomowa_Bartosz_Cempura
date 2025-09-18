
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
                pair.weight = 0.00
            db.session.commit()
            

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