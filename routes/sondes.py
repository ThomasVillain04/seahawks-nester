from flask import Blueprint, jsonify
from models import Sonde, db

# Création d'un Blueprint pour gérer les sondes
sondes_bp = Blueprint('sondes', __name__)

# Route pour récupérer toutes les sondes
@sondes_bp.route('/')
def get_sondes():
    sondes = Sonde.query.all()
    return jsonify([sonde.to_dict() for sonde in sondes])

# Route pour récupérer une sonde par son ID
@sondes_bp.route('/<id>')
def get_sonde(id):
    sonde = Sonde.query.get(id)
    if sonde:
        return jsonify(sonde.to_dict())
    return jsonify({"message": "Sonde non trouvée"}), 404
