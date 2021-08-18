""" Controllers package init """
from flask import Blueprint

# Create Blueprint
endpoint_bp = Blueprint("endpoint_bp", __name__)

from app.controllers import game
