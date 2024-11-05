import pandas as pd

df = pd.read_excel("teste.xlsx")

df['DATA_NEG'] = pd.to_datetime(df['DATA_NEG'])
df['Mes_Ano'] = df['DATA_NEG'].dt.to_period('M')

# Criação da tabela dinâmica
pivot_table = pd.pivot_table(
    data=df,
    values='VALOR',
    index='CLIENTE',
    columns='Mes_Ano',
    aggfunc='sum',
    margins=True,
    margins_name='Total Geral',
    fill_value=0
)

pivot_table.columns = [col.strftime('%b/%y').upper() if isinstance(col, pd.Period) else col for col in pivot_table.columns]

# Converter a tabela dinâmica para HTML
html = pivot_table.to_html(classes='tabela-dinamica', escape=False)

# Função para colorir valores negativos
def color_negative_values(val):
    formatted_value = f"{val:.2f}"
    if val < 0:
        return f'<span class="negativo">{formatted_value}</span>'  # Envolvendo em span com classe negativo
    return formatted_value

# Aplicar a função para todos os valores da tabela
for col in pivot_table.columns:
    pivot_table[col] = pivot_table[col].apply(color_negative_values)

# Converter novamente a tabela dinâmica em HTML com os valores coloridos
html = pivot_table.to_html(classes='tabela-dinamica', escape=False)

# Remover a linha do título do índice
# Aqui vamos substituir o texto da primeira linha do cabeçalho do índice por uma string vazia
# html = html.replace('<th>CLIENTE</th>', '<th>CLIENTE</th>')

# Adicionar estilos personalizados
html = f"""
<html>
<head>
    <style>
        .tabela-dinamica {{
            border-collapse: collapse;
            width: 100%;
        }}
        .tabela-dinamica th {{
            background-color: blue;
            color: white;
            font-weight: bold;
            padding: 10px;
            text-align: left;
        }}
        .tabela-dinamica td {{
            border: 1px solid #dddddd;
            text-align: center;
            padding: 8px;
        }}
        .tabela-dinamica td.produto {{
            text-align: left; /* Alinha o conteúdo da coluna Produto à esquerda */
        }}
        .tabela-dinamica tr:nth-child(even) {{
            background-color: lightgray;
        }}
        .tabela-dinamica tr:hover {{
            background-color: #f5f5f5;
        }}
        .tabela-dinamica .negativo {{
            color: red; /* Define a cor vermelha para valores negativos */
            font-weight: bold; /* Adiciona negrito */
        }}
    </style>
</head>
<body>
    <h2>Tabela Dinâmica de Vendas</h2>
    {html}
</body>
</html>
"""

# Salvar o HTML em um arquivo
with open('pivot_table.html', 'w') as f:
    f.write(html)

print("Tabela dinâmica salva como HTML com sucesso!")
