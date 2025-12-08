from sqlalchemy.orm import Session
from database.banco import SessionLocal, engine, Base
from app.models.models_alunos import Aluno
from app.models.models_cursos import Curso
from app.models.models_matricluas import Matricula


def init_db():
    Base.metadata.create_all(bind=engine)

    db: Session = SessionLocal()
    try:

        if db.query(Aluno).count() == 0:
            print("Seeding initial data for Alunos...")
            alunos = [
                Aluno(nome="João Silva", email="joao.silva@email.com"),
                Aluno(nome="Maria Souza", email="maria.souza@email.com"),
                Aluno(nome="Pedro Santos", email="pedro.santos@email.com"),
            ]
            db.add_all(alunos)
            db.commit()
            print(f"Seeded {len(alunos)} Alunos.")
        else:
            print("Alunos table already has data. Skipping seed.")

        if db.query(Curso).count() == 0:
            print("Seeding initial data for Cursos...")
            cursos = [
                Curso(nome_curso="Engenharia de Software",
                      carga_horaria="360h", periodo="Noturno", mensalidade=800),
                Curso(nome_curso="Análise e Desenvolvimento de Sistemas",
                      carga_horaria="240h", periodo="Diurno", mensalidade=650),
                Curso(nome_curso="Redes de Computadores",
                      carga_horaria="180h", periodo="Noturno", mensalidade=500),
            ]
            db.add_all(cursos)
            db.commit()
            print(f"Seeded {len(cursos)} Cursos.")
        else:
            print("Cursos table already has data. Skipping seed.")

    except Exception as e:
        db.rollback()
        print(f"An error occurred during database seeding: {e}")
    finally:
        db.close()


if __name__ == '__main__':
    init_db()
