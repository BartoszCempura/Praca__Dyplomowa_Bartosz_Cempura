from flask import Blueprint, request, jsonify
from backend import db
from backend.models import User

analytics_bp = Blueprint('analytics', __name__, url_prefix='/api/analytics')