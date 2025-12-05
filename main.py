
from flask import Flask
from database.banco import base_dados, engine
from app.models import models_alunos, models_cursos, models_matricluas

base_dados.metadata.create_all(bind=engine)

app = Flask(__name__)
app.config['JSON_SORT_KEYS_'] = False


if __name__ == '__main__':
    app.run(port=7070, host='localhost')
