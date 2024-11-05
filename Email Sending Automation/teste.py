import pandas as pd

df = pd.read_excel("teste.xlsx")

df['DATA_NEG'] = pd.to_datetime(df['DATA_NEG'])

df['Mes_Ano'] = df['DATA_NEG'].dt.to_period('M')

pivot_table = pd.pivot_table(
    data=df,
    values='VALOR',
    index='CLIENTE',
    columns='Mes_Ano',
    aggfunc='sum',
    margins=True,        # Adiciona o total geral
    margins_name='Total Geral'  # Nomeia o total geral
)
pivot_table.fillna(0, inplace=True)

# pivot_table.columns = pivot_table.columns.strftime('%b/%y').str.upper()
pivot_table.columns = [col.strftime('%b/%y').upper() if isinstance(col, pd.Period) else col for col in pivot_table.columns]

# Função para formatar valores negativos em vermelho
def color_negative_red(val):
    color = 'red' if val < 0 else 'black'
    return f'color: {color}'

# Aplicar o estilo na tabela pivô usando `map`
tabela_pivo_style = pivot_table.style.map(color_negative_red).format('{:.2f}')

tabela_pivo_style.set_table_attributes('style="border-collapse: collapse; text-align: left; border: 1px solid black;"')
tabela_pivo_style.set_properties(**{'border': '1px solid black'})

# tabela_pivo_style
tabela_pivo_style.to_html('tabela_pivo_style.html')
