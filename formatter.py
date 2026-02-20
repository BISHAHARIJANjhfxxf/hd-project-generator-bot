from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, PageBreak
)
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib import colors
from reportlab.lib.pagesizes import A4
from reportlab.lib.units import inch

def generate_pdf(text, body_size=15, heading_color="black"):

    file_path = "FINAL_Project.pdf"

    doc = SimpleDocTemplate(
        file_path,
        pagesize=A4,
        rightMargin=60,
        leftMargin=60,
        topMargin=60,
        bottomMargin=60,
        compression=0
    )

    heading_size = body_size + 5

    normal_style = ParagraphStyle(
        name="Normal",
        fontName="Helvetica",
        fontSize=body_size,
        leading=body_size + 6
    )

    heading_style = ParagraphStyle(
        name="Heading",
        fontName="Helvetica-Bold",
        fontSize=heading_size,
        leading=heading_size + 8,
        spaceAfter=12
    )

    elements = []
    lines = text.split("\n")

    table_mode = False
    table_data = []

    def render_table():
        nonlocal table_data
        if table_data:
            table = Table(table_data, repeatRows=1)
            table.setStyle(TableStyle([
                ('GRID', (0,0), (-1,-1), 1, colors.black),
                ('BACKGROUND', (0,0), (-1,0), colors.lightgrey),
                ('FONTNAME', (0,0), (-1,0), 'Helvetica-Bold'),
                ('FONTNAME', (0,1), (-1,-1), 'Helvetica'),
                ('FONTSIZE', (0,0), (-1,-1), body_size - 1),
            ]))
            elements.append(table)
            elements.append(Spacer(1, 0.3 * inch))
            table_data = []

    for line in lines:
        stripped = line.strip()

        # TABLE BLOCK START
        if stripped == "#table":
            table_mode = True
            continue

        # TABLE BLOCK END
        if stripped == "#endtable":
            table_mode = False
            render_table()
            continue

        if table_mode:
            row = [cell.strip() for cell in stripped.split("|")]
            table_data.append(row)
            continue

        render_table()

        # CHAPTER DETECT
        if stripped.lower().startswith("chapter"):
            elements.append(PageBreak())
            elements.append(
                Paragraph(
                    f'<b><font color="{heading_color}">{stripped}</font></b>',
                    heading_style
                )
            )
            elements.append(Spacer(1, 0.4 * inch))
            continue

        # BOLD SUPPORT
        if stripped.startswith("**") and stripped.endswith("**"):
            clean = stripped[2:-2]
            elements.append(Paragraph(f"<b>{clean}</b>", normal_style))
            elements.append(Spacer(1, 0.2 * inch))
            continue

        if stripped == "":
            elements.append(Spacer(1, 0.2 * inch))
        else:
            elements.append(Paragraph(stripped, normal_style))
            elements.append(Spacer(1, 0.2 * inch))

    render_table()
    doc.build(elements)

    return file_path
