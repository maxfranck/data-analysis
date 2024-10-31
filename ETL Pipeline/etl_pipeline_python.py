from sqlalchemy import create_engine
from sqlalchemy.engine import URL
from dotenv import load_dotenv
import pandas as pd
import os

load_dotenv()

a_server = os.getenv('A_DB_HOST')
a_database = os.getenv('A_DB_NAME')
a_uid = os.getenv('A_DB_USER')
a_pwd = os.getenv('A_DB_PASSWORD')
b_server = os.getenv('B_DB_HOST')
b_database = os.getenv('B_DB_NAME')
b_uid = os.getenv('B_DB_USER')
b_pwd = os.getenv('B_DB_PASSWORD')
driver = "{ODBC Driver 18 for SQL Server}"

def extract():
    try:
        connection_string = (
            f'DRIVER={driver};SERVER={a_server};DATABASE={a_database};'
            f'UID={a_uid};PWD={a_pwd};TrustServerCertificate=Yes'
        )
        connection_url = URL.create("mssql+pyodbc", query={"odbc_connect": connection_string})
        src_engine = create_engine(connection_url)
        src_conn = src_engine.connect()
        print("Conexão bem-sucedida!")

        query = """
            select  t.name as table_name
            from sys.tables t
            where t.name in ('TB_LOTE_LOCALIZACAO','TB_LOC_QUADRA')
        """
        src_tables = pd.read_sql_query(query, src_conn).to_dict()['table_name']

        for id in src_tables:
            table_name = src_tables[id]
            if table_name == 'TB_LOTE_LOCALIZACAO':
                df = pd.read_sql_query(f'select top 5 ID, IDLote, Pilha, posicao, IDEmpresa from {table_name}', src_conn)
            else:
                df = pd.read_sql_query(f'select top 5 ID, Nome, IDCorredor, posicao, pilha from {table_name}', src_conn)
            load(df, table_name)

        src_conn.close()

    except Exception as e:
        print("Data extract error: " + str(e))

def load(df, tbl):
    try:
        rows_imported = 0
        engine = create_engine(f'postgresql://{b_uid}:{b_pwd}@{b_server}:5432/{b_database}')
        print(f'importing rows {rows_imported} to {rows_imported + len(df)}... for table {tbl}')

        df.to_sql(f'stg_{tbl}', engine, if_exists='replace', index=False, chunksize=100000)
        rows_imported += len(df)

        print("Data imported successful")
    except Exception as e:
        print("Data load error: " + str(e))

try:
    extract()
except Exception as e:
    print("Error while extracting data: " + str(e))
