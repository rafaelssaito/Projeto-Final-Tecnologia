from flask import Blueprint, request, jsonify
from models import Evento
from datetime import datetime
from extensions import db  # Certifique-se de importar corretamente o db
import functools
import firebase_admin
from firebase_admin import credentials, auth

# Inicializa o Firebase Admin SDK
cred = credentials.Certificate("C:/Users/Rafael Saito/Desktop/P2 Tecnologia/serviceAccountKey.json")
firebase_admin.initialize_app(cred)

routes = Blueprint("routes", __name__)

# Middleware para proteger endpoints com Firebase Authentication
def firebase_required(func):
    @functools.wraps(func)
    def decorated_function(*args, **kwargs):
        auth_header = request.headers.get("Authorization", None)
        if not auth_header:
            return jsonify({"mensagem": "Token de autenticação necessário"}), 401

        parts = auth_header.split()
        if parts[0].lower() != "bearer" or len(parts) != 2:
            return jsonify({"mensagem": "Formato do token inválido"}), 401

        id_token = parts[1]

        try:
            decoded_token = auth.verify_id_token(id_token)
            request.firebase_user = decoded_token  # Adiciona os dados do usuário na requisição
        except Exception as e:
            return jsonify({"mensagem": "Token inválido", "erro": str(e)}), 401

        return func(*args, **kwargs)
    return decorated_function

@routes.route("/eventos", methods=["POST"])
@firebase_required  # Protege o endpoint de criação de eventos
def criar_evento():
    dados = request.get_json()
    data_formatada = datetime.strptime(dados["data"], "%Y-%m-%d %H:%M:%S")
    
    novo_evento = Evento(titulo=dados["titulo"], data=data_formatada)
    db.session.add(novo_evento)
    db.session.commit()
    
    return jsonify({
        "mensagem": "Evento criado!",
        "evento": {"titulo": novo_evento.titulo, "data": novo_evento.data.strftime("%Y-%m-%d %H:%M:%S")}
    }), 201

@routes.route("/eventos", methods=["GET"])
def listar_eventos():
    eventos = Evento.query.all()
    output = []
    for evento in eventos:
        evento_data = {
            "id": evento.id,
            "titulo": evento.titulo,
            "data": evento.data.strftime("%Y-%m-%d %H:%M:%S")
        }
        output.append(evento_data)
    return jsonify({"eventos": output})

@routes.route("/eventos/<int:id>", methods=["PUT"])
@firebase_required  # Protege o endpoint de atualização de eventos
def atualizar_evento(id):
    evento = Evento.query.get(id)
    if evento is None:
        return jsonify({"mensagem": "Evento não encontrado"}), 404

    dados = request.get_json()
    if "titulo" in dados:
        evento.titulo = dados["titulo"]
    if "data" in dados:
        try:
            evento.data = datetime.strptime(dados["data"], "%Y-%m-%d %H:%M:%S")
        except ValueError:
            return jsonify({"mensagem": "Formato de data inválido. Use YYYY-MM-DD HH:MM:SS"}), 400

    db.session.commit()
    return jsonify({
        "mensagem": "Evento atualizado!",
        "evento": {
            "id": evento.id,
            "titulo": evento.titulo,
            "data": evento.data.strftime("%Y-%m-%d %H:%M:%S")
        }
    })

@routes.route("/eventos/<int:id>", methods=["DELETE"])
@firebase_required  # Protege o endpoint de remoção de eventos
def remover_evento(id):
    evento = Evento.query.get(id)
    if evento is None:
        return jsonify({"mensagem": "Evento não encontrado"}), 404

    db.session.delete(evento)
    db.session.commit()
    return jsonify({"mensagem": "Evento removido com sucesso!"})

@routes.route("/evento-protegido", methods=["GET"])
@firebase_required  # Apenas usuários autenticados podem acessar esse endpoint
def evento_protegido():
    usuario = request.firebase_user
    return jsonify({
        "mensagem": "Acesso concedido ao endpoint protegido!",
        "usuario": usuario
    })
