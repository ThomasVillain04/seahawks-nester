from flask import Flask, request, jsonify, render_template
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from datetime import datetime
import uuid

# Initialisation de l'application Flask
app = Flask(__name__)
CORS(app)

# Configuration de la base de données MySQL
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://seahawks_user:P@ssw0rd@192.168.100.231/seahawks_nester'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Initialisation de SQLAlchemy
db = SQLAlchemy(app)

# Définition du modèle correspondant à la table "sondes"
class Sonde(db.Model):
    __tablename__ = 'sondes'

    id = db.Column(db.String(50), primary_key=True)
    ip = db.Column(db.String(100))
    vm_name = db.Column(db.String(100))
    connectee = db.Column(db.Boolean)
    latence = db.Column(db.String(50))
    version = db.Column(db.String(50))
    machines_connectees = db.Column(db.Integer)

@app.route('/')
def afficher_sondes():
    sondes = Sonde.query.order_by(Sonde.date_reception.desc()).all()
    return render_template('sondes.html', sondes=sondes)


# Route pour recevoir les données POST depuis les sondes
@app.route('/api/v1/receive_data', methods=['POST'])
def receive_data():
    data = request.get_json()
    
    if not data:
        return jsonify({"error": "Aucune donnée reçue"}), 400

    try:
        nouvelle_sonde = Sonde(
            id=str(uuid.uuid4()),
            ip=data.get("local_ip"),
            vm_name=data.get("vm_name"),
            connectee=bool(data.get("connectee")),
            latence=data.get("latence"),
            version=data.get("version"),
            machines_connectees=data.get("connected_machines")
        )
        db.session.add(nouvelle_sonde)
        db.session.commit()
        return jsonify({"status": "ok"}), 200
    except Exception as e:
        print("Erreur lors de l'enregistrement :", e)
        return jsonify({"error": "Erreur serveur"}), 500

# Point de départ de l'application
if __name__ == '__main__':
    app.run(debug=True, host="0.0.0.0", port=5000)
