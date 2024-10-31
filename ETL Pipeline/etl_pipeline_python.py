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
  
    query = "SELECT TOP 10 * FROM TABLE_NAME"
    
    df = pd.read_sql(query, src_conn)
    
    print(df)

    src_conn.close()

except Exception as e:
    print("Data extract error: " + str(e))
