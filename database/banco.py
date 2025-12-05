from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker


engine = create_engine('sqlite:///database/base_api.db')
base_dados = declarative_base()
sessionlocal = sessionmaker(bind=engine)
