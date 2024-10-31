from sqlalchemy import create_engine
from sqlalchemy.engine import URL
from dotenv import load_dotenv
import pandas as pd
import os

load_dotenv()

server = os.getenv('DB_HOST')
database = os.getenv('DB_NAME')
uid = os.getenv('DB_USER')
pwd = os.getenv('DB_PASSWORD')
driver = "{ODBC Driver 18 for SQL Server}"

try:
    connection_string = (
        f'DRIVER={driver};SERVER={server};DATABASE={database};'
        f'UID={uid};PWD={pwd};TrustServerCertificate=Yes'
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
        df = pd.read_sql_query(f'select top 5 * FROM {table_name}', src_conn)
        print(df)
        # load(df, table_name)

    src_conn.close()

except Exception as e:
    print("Data extract error: " + str(e))
