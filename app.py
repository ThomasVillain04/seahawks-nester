from flask import Flask, request, jsonify, render_template
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from datetime import datetime
import sqlalchemy.exc

app = Flask(__name__)
CORS(app)

# ⚙️ Configuration MySQL (modifie user/mdp/IP au besoin)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://seahawks_user:P@ssw0rd@192.168.100.231/seahawks_nester'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# 📦 Base de données
db = SQLAlchemy(app)

# 🧩 Modèle Sonde
class Sonde(db.Model):
    __tablename__ = 'sondes'
    id = db.Column(db.String(50), primary_key=True)
    ip = db.Column(db.String(100))
    vm_name = db.Column(db.String(100))
    connectee = db.Column(db.Boolean)
    latence = db.Column(db.String(50))
    version = db.Column(db.String(50))
    machines_connectees = db.Column(db.Integer)
    date_reception = db.Column(db.DateTime, default=datetime.utcnow)

# 🌐 Page HTML principale
@app.route('/')
def index():
    try:
        sondes = Sonde.query.order_by(Sonde.date_reception.desc()).all()
    except sqlalchemy.exc.OperationalError:
        sondes = []  # La BDD est inaccessible
    return render_template('index.html', sondes=sondes)

# 📥 Réception de données POST depuis les sondes
@app.route('/api/v1/receive_data', methods=['POST'])
def receive_data():
    data = request.get_json()
    print("✅ Données reçues :", data)

    try:
        sonde = Sonde(
            id=data.get('id'),
            ip=data.get('local_ip'),
            vm_name=data.get('vm_name'),
            connectee=data.get('connectee'),
            latence=data.get('latence'),
            version=data.get('version'),
            machines_connectees=data.get('connected_machines')
        )
        db.session.merge(sonde)
        db.session.commit()
        return jsonify({"status": "ok"}), 200
    except Exception as e:
        print("❌ Erreur :", e)
        return jsonify({"status": "error", "details": str(e)}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
