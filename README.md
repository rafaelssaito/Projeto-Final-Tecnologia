# Projeto-Final-Tecnologia
Uma API REST para gerenciar eventos e autenticação usando Firebase. Permite CRUD completo de eventos com proteção via tokens JWT.

## 🔗 Pré-requisitos

- Python 3.9 ou superior
- Flask
- Firebase Admin SDK
- Docker (Opcional)

  ## 📦 Instalação

1. Clone o repositório:
   ```bash
   git clone https://github.com/seu-usuario/seu-repositorio.git

 2.  cd seu-repositorio

 3. Crie um maquina virtual
python -m venv venv
source venv/bin/activate  # macOS/Linux
venv\Scripts\activate  # Windows

 4. pip install -r requirements.txt


## 🔒 Configuração do Firebase

1. Acesse [Firebase Console](https://console.firebase.google.com).
2. Baixe o arquivo `serviceAccountKey.json` e coloque na pasta do projeto.
3. Certifique-se de que a autenticação Firebase está ativada.

