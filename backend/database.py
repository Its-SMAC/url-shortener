from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

db = SQLAlchemy()

class URL(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    url_original = db.Column(db.Text,nullable=False)
    codigo_curto = db.Column(db.String(6),unique=True,nullable=False)
    criado_em = db.Column(db.DateTime,  default=datetime.utcnow)
