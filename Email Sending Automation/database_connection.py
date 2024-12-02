from sqlalchemy import create_engine, text
from sqlalchemy.engine import URL

class DatabaseConnection:
    def __init__(self, server, database, username, password, driver):
        # Configuração da string de conexão
        self.connection_string = (
            f'DRIVER={driver};SERVER={server};DATABASE={database};'
            f'UID={username};PWD={password};TrustServerCertificate=Yes'
        )
        self.engine = None
        self.connection_url = URL.create("mssql+pyodbc", query={"odbc_connect": self.connection_string})

    def connect(self):
        # Conectar ao banco de dados
        try:
            self.engine = create_engine(self.connection_url)
            print("Conexão com o banco de dados estabelecida com sucesso.")
        except Exception as e:
            print(f"Erro ao conectar ao banco de dados: {e}")

    def execute_query(self, query):
        # Executa uma query e retorna os resultados como lista de dicionários
        if self.engine:
            try:
                with self.engine.connect() as connection:
                    result = connection.execute(text(query)).mappings()  # Usar .mappings() aqui
                    return [dict(row) for row in result]  # Transforma cada linha em dicionário
            except Exception as e:
                print(f"Erro ao executar a query: {e}")
        else:
            print("Conexão não estabelecida.")
        return []
