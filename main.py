# main.py
from flask import Flask
from extensions import db
from routes_module import routes

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///agenda.db"

# Associa o app à instância do SQLAlchemy
db.init_app(app)

# Cria as tabelas do banco de dados
with app.app_context():
    db.create_all()

# Registra o blueprint com as rotas definidas
app.register_blueprint(routes)

if __name__ == "__main__":
    app.run(debug=True)
