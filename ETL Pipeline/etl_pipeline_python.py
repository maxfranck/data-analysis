# Importa os pacotes necessários
from sqlalchemy import create_engine
from sqlalchemy.engine import URL
from dotenv import load_dotenv
import pandas as pd
import os

# Carrega as variáveis de ambiente a partir do arquivo .env
load_dotenv()

# Define as variáveis de conexão para o banco de dados A (SQL Server)
a_server = os.getenv('A_DB_HOST')
a_database = os.getenv('A_DB_NAME')
a_uid = os.getenv('A_DB_USER')
a_pwd = os.getenv('A_DB_PASSWORD')

# Define as variáveis de conexão para o banco de dados B (PostgreSQL)
b_server = os.getenv('B_DB_HOST')
b_database = os.getenv('B_DB_NAME')
b_uid = os.getenv('B_DB_USER')
b_pwd = os.getenv('B_DB_PASSWORD')

# Define o driver ODBC para a conexão com o SQL Server
driver = "{ODBC Driver 18 for SQL Server}"

# Função para extrair dados do banco A (SQL Server)
def extract():
    try:
        # Configura a string de conexão para o SQL Server
        connection_string = (
            f'DRIVER={driver};SERVER={a_server};DATABASE={a_database};'
            f'UID={a_uid};PWD={a_pwd};TrustServerCertificate=Yes'
        )
        connection_url = URL.create("mssql+pyodbc", query={"odbc_connect": connection_string})

        # Cria a conexão com o banco de dados SQL Server
        src_engine = create_engine(connection_url)
        src_conn = src_engine.connect()
        print("Conexão bem-sucedida!")

        # Define a query para listar tabelas específicas do banco A
        query = """
            select  t.name as table_name
            from sys.tables t
            where t.name in ('TB_LOTE_LOCALIZACAO','TB_LOC_QUADRA')
        """

        # Executa a query e converte o resultado em um dicionário com os nomes das tabelas
        src_tables = pd.read_sql_query(query, src_conn).to_dict()['table_name']

        # Para cada tabela encontrada, realiza uma extração de dados
        for id in src_tables:
            table_name = src_tables[id]

            # Define a query SQL para extrair as colunas necessárias de cada tabela
            if table_name == 'TB_LOTE_LOCALIZACAO':
                df = pd.read_sql_query(f'select top 5 ID, IDLote, Pilha, posicao, IDEmpresa from {table_name}', src_conn)
            else:
                df = pd.read_sql_query(f'select top 5 ID, Nome, IDCorredor, posicao, pilha from {table_name}', src_conn)

            # Carrega os dados extraídos para o banco de dados B
            load(df, table_name)

        # Fecha a conexão com o banco A após a extração
        src_conn.close()

    except Exception as e:
        print("Data extract error: " + str(e))

# Função para carregar dados no banco B (PostgreSQL)
def load(df, tbl):
    try:
        rows_imported = 0

        # Configura a string de conexão para o PostgreSQL
        engine = create_engine(f'postgresql://{b_uid}:{b_pwd}@{b_server}:5432/{b_database}')

        # Cria a conexão com o banco de dados PostgreSQL
        conn = engine.connect()

        # Imprime o status da importação de dados
        print(f'importing rows {rows_imported} to {rows_imported + len(df)}... for table {tbl}')

        # Insere os dados no banco B, criando ou substituindo a tabela de estágio correspondente
        df.to_sql(f'stg_{tbl}', conn, if_exists='replace', index=False, chunksize=100000)

        # Atualiza a contagem de linhas importadas
        rows_imported += len(df)

        print("Data imported successfully")

        # Fecha a conexão com o banco B após a carga
        conn.close()

    except Exception as e:
        print("Data load error: " + str(e))

# Executa o processo de extração e carga de dados
try:
    extract()
except Exception as e:
    print("Error while extracting data: " + str(e))
