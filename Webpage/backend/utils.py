## tutaj będziemy deklarowac endpointy - czyli co się wyświetla nam na 

from flask import Blueprint, request, jsonify
from backend import db

utils_bp = Blueprint('utils', __name__, url_prefix='/api/utils')

@utils_bp.route('/health', methods=['GET'])
def health_check():
    return {'status': 'healthy'}, 200