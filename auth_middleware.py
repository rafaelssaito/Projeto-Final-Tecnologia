# auth_middleware.py
import functools
from flask import request, jsonify
import firebase_admin
from firebase_admin import credentials, auth as firebase_auth

# Inicializa o Firebase Admin SDK com sua conta de serviço.
# Substitua 'path/to/serviceAccountKey.json' pelo caminho para o seu arquivo JSON.
cred = credentials.Certificate(r"C:\Users\Rafael Saito\Desktop\P2 Tecnologia\serviceAccountKey.json")
firebase_admin.initialize_app(cred)

def firebase_required(func):
    """
    Decorator para proteger endpoints; ele extrai o token enviado no header Authorization,
    verifica seu valor com o Firebase e permite o acesso apenas se o token for válido.
    """
    @functools.wraps(func)
    def decorated_function(*args, **kwargs):
        id_token = None
        auth_header = request.headers.get('Authorization', None)

        if auth_header:
            parts = auth_header.split()
            if parts[0].lower() != 'bearer':
                return jsonify({"mensagem": "O header Authorization deve iniciar com Bearer"}), 401
            elif len(parts) == 1:
                return jsonify({"mensagem": "Token não informado"}), 401
            elif len(parts) > 2:
                return jsonify({"mensagem": "Header Authorization inválido"}), 401
            id_token = parts[1]
        else:
            return jsonify({"mensagem": "Header Authorization é necessário"}), 401

        try:
            # Verifica o token com o Firebase
            decoded_token = firebase_auth.verify_id_token(id_token)
            # Optional: você pode armazenar as informações do usuário na requisição
            request.firebase_user = decoded_token
        except Exception as e:
            return jsonify({"mensagem": "Token inválido", "erro": str(e)}), 401

        return func(*args, **kwargs)
    return decorated_function