from backend import create_app, db
from backend.models import *
from backend.scheduler import calculate_product_similarity

app = create_app()

calculate_product_similarity(app)
