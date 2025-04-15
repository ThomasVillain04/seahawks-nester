from flask import Flask, request, jsonify, render_template
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from datetime import datetime

# Initialisation de l'application Flask
app = Flask(__name__)
CORS(app)

# Configuration de la base de données MySQL
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://seahawks_user:P@ssw0rd@192.168.100.231/seahawks_nester'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Initialisation de la BDD
db = SQLAlchemy(app)

# Définition du modèle de la table "sondes"
class Sonde(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    local_ip = db.Column(db.String(100))
    scan_result = db.Column(db.Text)
    connected_machines = db.Column(db.Integer)
    date_reception = db.Column(db.DateTime, default=datetime.utcnow)

# Route d'accueil — affiche les données HTML
@app.route('/')
def index():
    sondes = Sonde.query.order_by(Sonde.date_reception.desc()).all()
    return render_template('sondes.html', sondes=sondes)

# API — reçoit les données des sondes (POST)
@app.route('/api/v1/receive_data', methods=['POST'])
def receive_data():
    data = request.get_json()
    if not data:
        return jsonify({"status": "erreur", "message": "Aucune donnée reçue"}), 400

    try:
        nouvelle_sonde = Sonde(
            local_ip=data.get("local_ip"),
            scan_result=data.get("scan_result"),
            connected_machines=data.get("connected_machines")
        )
        db.session.add(nouvelle_sonde)
        db.session.commit()
        return jsonify({"status": "ok"}), 200
    except Exception as e:
        return jsonify({"status": "erreur", "message": str(e)}), 500

# Lancement de l'application
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
