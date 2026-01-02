from flask import Flask, request, jsonify, redirect
from flask_cors import CORS
from database import db, URL 
from utils import gerar_codigo_curto
import os

BASE_URL = os.environ.get('BASE_URL', 'http://127.0.0.1:5000')

app = Flask(__name__)
CORS(app)

# Configuração da BD
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///urls.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Inicializa db com app
db.init_app(app)

# Criar tabelas
with app.app_context():
    db.create_all()

# Rota de teste
@app.route('/')
def home():
    return "URL Shortener API - Working! 🚀"

@app.route('/shorten', methods=['POST'])
def shorten():
    data = request.json
    url_original = data.get('url')
    if not url_original:
        return jsonify({"erro":'URL é obrigatório'}), 400
    url_existente = URL.query.filter_by(url_original=url_original).first()
    if url_existente:
        return jsonify({
        'codigo':url_existente.codigo_curto,
        'url_curto':f'{BASE_URL}/{url_existente.codigo_curto}',
        'url_original': url_original
    }), 200
    
    codigo = gerar_codigo_curto()
    while URL.query.filter_by(codigo_curto=codigo).first():
        codigo = gerar_codigo_curto()
    novo_url = URL(url_original=url_original,codigo_curto=codigo)
    try:
        db.session.add(novo_url)
        db.session.commit()
    except Exception as e:
        db.session.rollback()
        return jsonify({'erro':'Erro ao processar'}), 500
    return jsonify({
        'codigo':codigo,
        'url_curto':f'{BASE_URL}/{codigo}',
        'url_original': url_original
    }), 201

@app.route('/<codigo>')
def redirecionar(codigo):
    url_obj = URL.query.filter_by(codigo_curto=codigo).first()
    if not url_obj:
        return jsonify({'erro':'Código não encontrado'}), 404
    return redirect(url_obj.url_original)

if __name__ == '__main__':
    app.run()