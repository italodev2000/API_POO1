from flask import Flask
from app.controllers.routes_controllers import router
from database.banco import Base, engine

app = Flask(__name__)

# Criar tabelas
Base.metadata.create_all(bind=engine)

# Registrar rotas
app.register_blueprint(router)


if __name__ == "__main__":
    app.run(debug=True)
