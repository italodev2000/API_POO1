# Educapoints Uninassau – API em Python

API desenvolvida em Python para gerenciar rotinas de realização de matriculas de alunos em cursos de todas
as finalidades

# Tecnologias/FrameWorks

* Python 3.10+
* Flask 
* SQLite 
* SQLAlchemy (ORM)
* Pydantic
* venv

# Estrutura de arquitetura do Projeto 

Educapoints_Uninassau/
│     
│   ├── controllers/        * Controladores (rotas)
│   ├── services/           * Regras de negócio
│   ├── repositories/       * Acesso ao banco
│   ├── models/             * Modelos / entidades
│   |── database/           * Configuração do banco
|   ├── main.py              * Arquivo principal da aplicação
│      
├── requirements.txt        # Dependências do projeto
└── README.md               # Documentação

# Clonar o repositório
git clone https://github.com/italodev2000/Projeto_API_educacional.git
cd PROJETO_EDUCA

# Instalar dependências
pip install -r requirements.txt

📑 Endpoints (Exemplo)
Método	Rota	Descrição
GET	/items	Lista todos os itens
POST	/items	Cria um item
GET	/items/{id}	Retorna um item específico
PUT	/items/{id}	Atualiza um item
DELETE	/items/{id}	Remove um item

🗄️ Banco de Dados

Execute o script de criação:

python src/database/create_tables.py

# Padronizado (PEP8)

👨‍💻 Autores

Integrantes:

Perfies GitHub: