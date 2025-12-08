from flask import Flask
from app.controllers.routes_controllers import router
from database.banco import Base, engine
from database.seed import init_db

app = Flask(__name__)

Base.metadata.create_all(bind=engine)

init_db()

app.register_blueprint(router)


if __name__ == "__main__":
    app.run(debug=True)
