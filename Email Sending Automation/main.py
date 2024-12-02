from database_connection import DatabaseConnection
from table_pdf_builder import TablePDFBuilder
from dotenv import load_dotenv
import os
import os

load_dotenv()

# Dados de conexão (substitua pelos seus)
servidor = os.getenv('DB_HOST')
banco_dados = os.getenv('DB_NAME')
usuario = os.getenv('DB_USER')
senha = os.getenv('DB_PASSWORD')
driver = "{ODBC Driver 18 for SQL Server}"

# Query SQL
query = """
SELECT ID, DESCRICAO, DATA, VALOR
FROM TABELA
WHERE MONTH(DATA) = 10
AND YEAR(DATA) = 2024;
"""

# Conexão com o banco de dados
db = DatabaseConnection(servidor, banco_dados, usuario, senha, driver)
db.connect()

# Executar a query e obter os dados
resultados = db.execute_query(query)

# Gerar o PDF com os dados obtidos
if resultados:
    pdf_builder = TablePDFBuilder()
    pdf_builder.gerar_pdf(resultados)
else:
    print("Nenhum dado foi retornado pela query.")
