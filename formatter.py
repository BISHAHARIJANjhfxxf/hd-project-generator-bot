from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, PageBreak
)
from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
from reportlab.lib import colors
from reportlab.lib.pagesizes import A4
from reportlab.lib.units import inch

def add_page_number(canvas, doc):
    canvas.setFont("Helvetica", 10)
    canvas.drawRightString(580, 20, f"Page {doc.page}")

def generate_pdf(text):

    file_path = "HD_Project_Output.pdf"

    doc = SimpleDocTemplate(
        file_path,
        pagesize=A4,
        rightMargin=50,
        leftMargin=60,
        topMargin=60,
        bottomMargin=50,
        compression=0  # ensures no raster compression
    )

    styles = getSampleStyleSheet()

    normal_style = ParagraphStyle(
        name="NormalStyle",
        parent=styles["Normal"],
        fontName="Helvetica",
        fontSize=12,
        leading=18
    )

    chapter_style = ParagraphStyle(
        name="ChapterStyle",
        parent=styles["Heading1"],
        fontName="Helvetica-Bold",
        fontSize=18,
        spaceAfter=12
    )

    elements = []
    lines = text.split("\n")
    table_buffer = []

    def flush_table():
        nonlocal table_buffer
        if table_buffer:
            table = Table(table_buffer, repeatRows=1)
            table.setStyle(TableStyle([
                ('GRID', (0,0), (-1,-1), 1, colors.black),
                ('BACKGROUND', (0,0), (-1,0), colors.HexColor("#F2F2F2")),
                ('FONTNAME', (0,0), (-1,0), 'Helvetica-Bold'),
                ('FONTNAME', (0,1), (-1,-1), 'Helvetica'),
                ('FONTSIZE', (0,0), (-1,-1), 11),
            ]))
            elements.append(table)
            elements.append(Spacer(1, 0.3 * inch))
            table_buffer = []

    for line in lines:
        stripped = line.strip()

        if "|" in line:
            row = [cell.strip() for cell in line.strip("|").split("|")]
            table_buffer.append(row)
            continue

        if "\t" in line:
            row = [cell.strip() for cell in line.split("\t")]
            table_buffer.append(row)
            continue

        flush_table()

        if stripped.lower().startswith("chapter"):
            elements.append(PageBreak())
            elements.append(Paragraph(stripped, chapter_style))
            elements.append(Spacer(1, 0.3 * inch))
        elif stripped == "":
            elements.append(Spacer(1, 0.2 * inch))
        else:
            elements.append(Paragraph(stripped, normal_style))
            elements.append(Spacer(1, 0.2 * inch))

    flush_table()

    doc.build(elements, onLaterPages=add_page_number)

    return file_path
