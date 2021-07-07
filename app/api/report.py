import os

import xlsxwriter
from docx.shared import Mm
from docxtpl import DocxTemplate, InlineImage
from flask import current_app
from reportlab.lib.colors import HexColor
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import SimpleDocTemplate, Table, Image, PageBreak, Paragraph
from reportlab.lib.units import inch
from reportlab.lib import colors
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont


def excel_write(path):
    workbook = xlsxwriter.Workbook(path)
    worksheet = workbook.add_worksheet("test1")
    worksheet.set_column('A:A', 20)

    bold = workbook.add_format({'bold': True})

    worksheet.write('A1', 'Hello')

    worksheet.write('A2', 'World', bold)

    worksheet.write(2, 0, 123)
    worksheet.write(3, 0, 123.456)

    worksheet.write_column(4, 0, [1, 2, 3, 4])

    worksheet.write_row(1, 1, [1, 2, 3, 4])

    chart = workbook.add_chart({'type': 'column'})

    chart.add_series({'values': ["test1",  # worksheet。sheet_name
                                 4, 0, 7, 0  
                                 ]})
    worksheet.insert_chart('B3', chart)

    workbook.close()
    return path


def word_write(generated_doc_path):
    template_path = current_app.config.get("REPORT_TEMPLATES")
    path = os.path.join(template_path, 'test.docx')

    doc = DocxTemplate(path)
    context = {
        'title': "person",
        'table': [
            {"name": "zsy", "age": 11},
            {"name": "zsy", "age": 21},
            {"name": "zsy", "age": 20},
            {"name": "zsy1", "age": 10},
            {"name": "zsy2", "age": 30},
            {"name": "zsy3", "age": 40},
        ],
        'header': 'person info',
        'footer': '1',
        'image': InlineImage(doc, os.path.join(template_path, 'test.jpg'), height=Mm(10)),
    }
    doc.render(context)

    doc.save(generated_doc_path)
    return generated_doc_path


def table_model():
    """
    :return:
    """
    template_path = current_app.config.get("REPORT_TEMPLATES")
    image_path = os.path.join(template_path, 'test.jpg')
    new_img = Image(image_path, width=300, height=300)
    base = [
        [new_img, ""],
        ["big", "small"],
        ["WebFramework", "django"],
        ["", "flask"],
        ["", "web.py"],
        ["", "tornado"],
        ["Office", "xlsxwriter"],
        ["", "openpyxl"],
        ["", "xlrd"],
        ["", "xlwt"],
        ["", "python-docx"],
        ["", "docxtpl"],
    ]

    style = [
        ('FONTNAME', (0, 0), (-1, -1), 'SimSun'),

        ('SPAN', (0, 0), (1, 0)),
        ('SPAN', (0, 2), (0, 5)),
        ('SPAN', (0, 6), (0, 11)),

        ('BACKGROUND', (0, 1), (1, 1), HexColor('#548DD4')),

        ('TEXTCOLOR', (0, 1), (1, 1), colors.white),
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),

        ('GRID', (0, 0), (-1, -1), 0.5, colors.grey),
        ('BOX', (0, 0), (-1, -1), 0.5, colors.black),

    ]

    component_table = Table(base, style=style)
    return component_table


def paragraph_model(msg):
    """
    :param msg:
    :return:
    """
    style = ParagraphStyle(
        name='Normal',
        fontName='SimSun',
        fontSize=50,
    )

    return Paragraph(msg, style=style)


def image_model():
    """
    :return:
    """
    template_path = current_app.config.get("REPORT_TEMPLATES")
    image_path = os.path.join(template_path, 'test.jpg')
    new_img = Image(image_path, width=300, height=300)
    return new_img


def pdf_write(generated_pdf_path):
    """
    generate pdf
    :return:
    """
    font_path = current_app.config.get("SIM_SUN")

    pdfmetrics.registerFont(TTFont('SimSun', os.path.join(font_path, 'SimSun.ttf')))
    styles = getSampleStyleSheet()
    styles.add(ParagraphStyle(fontName='SimSun', name='SimSun', leading=20, fontSize=12))
    data = list()
    paragraph = paragraph_model("test add some words")
    data.append(paragraph)
    data.append(PageBreak())  
    table = table_model()
    data.append(table)
    data.append(PageBreak())  
    img = image_model()
    data.append(img)

    pdf = SimpleDocTemplate(generated_pdf_path, rightMargin=0, leftMargin=0, topMargin=40, bottomMargin=0, )
    pdf.pagesize = (9 * inch, 10 * inch)

    pdf.multiBuild(data)
    return generated_pdf_path
