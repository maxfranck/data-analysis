from reportlab.lib.pagesizes import A4, landscape
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib import colors
from reportlab.lib.colors import Color
from datetime import datetime
import locale

# Configura a localidade para formatação brasileira
locale.setlocale(locale.LC_ALL, 'pt_BR.UTF-8')

class TablePDFBuilder:
    def __init__(self, output_file="./Email Sending Automation/tabela.pdf"):
        self.output_file = output_file

    @staticmethod
    def hex_to_rgb(hex_color):
        """Converte uma cor hexadecimal (#RRGGBB) para o formato RGB do ReportLab."""
        hex_color = hex_color.lstrip('#')  # Remove o "#" do início
        r, g, b = tuple(int(hex_color[i:i+2], 16) for i in (0, 2, 4))  # Divide em R, G, B
        return Color(r / 255, g / 255, b / 255)  # Normaliza para o intervalo 0-1

    def formatar_data(self, data_str):
        try:
            return datetime.strptime(data_str, "%Y-%m-%d").strftime("%d/%m/%Y")
        except:
            return data_str  # Caso a data já esteja no formato correto ou seja inválida

    def formatar_valor(self, valor):
        try:
            return locale.format_string('%.2f', valor, grouping=True)
        except:
            return str(valor)

    def gerar_pdf(self, dados):
        # Estilos de parágrafo
        estilos = getSampleStyleSheet()
        estilo_descricao = estilos["BodyText"]

        # Processar dados para o PDF
        linhas_formatadas = []
        for linha in dados:
            linha["DESCRICAO"] = Paragraph(str(linha.get("DESCRICAO", "")), estilo_descricao)
            linha["DATA"] = self.formatar_data(linha.get("DATA", ""))
            linha["VALOR"] = self.formatar_valor(linha.get("VALOR", 0))
            linhas_formatadas.append([
                linha.get("ID", ""),
                linha["DESCRICAO"],
                linha["DATA"],
                linha["VALOR"]
            ])

        # Cabeçalho da tabela
        cabecalho = ["ID", "Descrição", "Data", "Valor"]

        # Combinar o cabeçalho e os dados formatados
        dados_tabela = [cabecalho] + linhas_formatadas

        # Configurar a tabela
        colunas = [50, 400, 100, 100]
        tabela = Table(dados_tabela, colWidths=colunas)

        # Estilo da tabela
        estilo = TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), self.hex_to_rgb("#4F4F4F")),  # Cabeçalho com verde personalizado
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.white),
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
            ('VALIGN', (0, 0), (-1, 0), 'MIDDLE'),  # Alinhamento vertical ao centro no cabeçalho
            ('ALIGN', (1, 1), (1, -1), 'LEFT'),
            ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),  # Alinhamento vertical ao centro
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('BOTTOMPADDING', (0, 0), (-1, 0), 3),
            ('GRID', (0, 0), (-1, -1), 1, colors.black),
        ])

        # Linhas zebradas com cores personalizadas
        for i, linha in enumerate(dados_tabela[1:], start=1):
            bg_color = self.hex_to_rgb("#FFFFFF") if i % 2 == 0 else self.hex_to_rgb("#D3D3D3")  # Tons personalizados
            estilo.add('BACKGROUND', (0, i), (-1, i), bg_color)

        tabela.setStyle(estilo)

        # Gerar o PDF
        pdf = SimpleDocTemplate(self.output_file, pagesize=landscape(A4))
        pdf.build([tabela])
        print(f"Tabela gerada no arquivo {self.output_file}")
