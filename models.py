from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class Sonde(db.Model):
    __tablename__ = 'sondes'  # Nom de la table dans MySQL

    id = db.Column(db.String(50), primary_key=True)
    ip = db.Column(db.String(100))
    vm_name = db.Column(db.String(100))
    connectee = db.Column(db.Boolean)
    latence = db.Column(db.String(50))
    version = db.Column(db.String(50))
    machines_connectees = db.Column(db.Integer)

    def to_dict(self):
        return {
            "id": self.id,
            "ip": self.ip,
            "vm_name": self.vm_name,
            "connectee": self.connectee,
            "latence": self.latence,
            "version": self.version,
            "machines_connectees": self.machines_connectees
        }
