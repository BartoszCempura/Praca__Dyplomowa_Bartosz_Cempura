
import os
from flask_apscheduler import APScheduler
from apscheduler.jobstores.sqlalchemy import SQLAlchemyJobStore
from sqlalchemy import MetaData
from datetime import datetime, timedelta, timezone

scheduler = APScheduler()

def clear_expired_carts():

    """-------------------------------Job usówania koszyków nieaktualizowanych przez 3 dni-------------------------------"""

    # Pobieramy instancję aplikacji z scheduler
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