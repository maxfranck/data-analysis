from reportlab.lib.pagesizes import A4, landscape
from reportlab.platypus import BaseDocTemplate, PageTemplate, Frame, Table, TableStyle, Paragraph
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
        def cabecalho(canvas, doc):
            """Adiciona um cabeçalho apenas na primeira página."""
            if doc.page == 1:  # Verifica se é a primeira página
                canvas.saveState()
                canvas.setFont('Helvetica-Bold', 14)
                canvas.drawString(30, 560, "Relatório Mensal - Outubro 2024")
                canvas.setFont('Helvetica', 10)
                canvas.drawString(30, 545, "Este relatório apresenta os dados filtrados para o mês de outubro de 2024.")
                canvas.restoreState()

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
        cabecalho_tabela = ["ID", "Descrição", "Data", "Valor"]
        dados_tabela = [cabecalho_tabela] + linhas_formatadas

        # Configurar a tabela
        colunas = [50, 400, 100, 100]
        tabela = Table(dados_tabela, colWidths=colunas)

        # Estilo da tabela
        estilo = TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), self.hex_to_rgb("#4F4F4F")),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.white),
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
            ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('BOTTOMPADDING', (0, 0), (-1, 0), 3),
            ('GRID', (0, 0), (-1, -1), 1, colors.black),
        ])

        # Linhas zebradas com cores personalizadas
        for i, linha in enumerate(dados_tabela[1:], start=1):
            bg_color = self.hex_to_rgb("#FFFFFF") if i % 2 == 0 else self.hex_to_rgb("#D3D3D3")
            estilo.add('BACKGROUND', (0, i), (-1, i), bg_color)

        tabela.setStyle(estilo)

        # Criar o documento com cabeçalho
        pdf = BaseDocTemplate(self.output_file, pagesize=landscape(A4))
        frame = Frame(pdf.leftMargin, pdf.bottomMargin, pdf.width, pdf.height - 50, id='normal')
        template = PageTemplate(id='test', frames=frame, onPage=cabecalho)
        pdf.addPageTemplates([template])

        # Gerar o conteúdo do PDF
        elementos = [tabela]
        pdf.build(elementos)

        print(f"Tabela gerada no arquivo {self.output_file}")
