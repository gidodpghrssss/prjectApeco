from reportlab.lib import colors
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
import markdown2
import re

def clean_html(html):
    # Remove HTML tags but keep the text
    clean = re.compile('<.*?>')
    return re.sub(clean, '', html)

def create_pdf():
    # Read the Markdown content
    with open('docs/documentacion_completa.md', 'r', encoding='utf-8') as f:
        markdown_content = f.read()

    # Convert Markdown to HTML
    html = markdown2.markdown(markdown_content)

    # Create PDF document
    doc = SimpleDocTemplate(
        "docs/Documentacion_Bienes_Raices_IA.pdf",
        pagesize=A4,
        rightMargin=72,
        leftMargin=72,
        topMargin=72,
        bottomMargin=72
    )

    # Styles
    styles = getSampleStyleSheet()
    styles.add(ParagraphStyle(
        name='CustomTitle',
        parent=styles['Title'],
        fontSize=24,
        spaceAfter=30,
        textColor=colors.HexColor('#2E7D32')
    ))
    styles.add(ParagraphStyle(
        name='CustomHeading1',
        parent=styles['Heading1'],
        fontSize=20,
        spaceAfter=16,
        textColor=colors.HexColor('#1B5E20')
    ))
    styles.add(ParagraphStyle(
        name='CustomHeading2',
        parent=styles['Heading2'],
        fontSize=16,
        spaceAfter=12,
        textColor=colors.HexColor('#2E7D32')
    ))
    styles.add(ParagraphStyle(
        name='CustomBody',
        parent=styles['Normal'],
        fontSize=11,
        spaceAfter=8
    ))

    # Content elements
    elements = []

    # Add title
    elements.append(Paragraph("Bienes Raíces con IA", styles['CustomTitle']))
    elements.append(Spacer(1, 12))

    # Process content
    lines = html.split('\n')
    for line in lines:
        if line.strip():
            if line.startswith('<h1>'):
                text = clean_html(line)
                elements.append(Paragraph(text, styles['CustomHeading1']))
            elif line.startswith('<h2>'):
                text = clean_html(line)
                elements.append(Paragraph(text, styles['CustomHeading2']))
            elif line.startswith('<h3>'):
                text = clean_html(line)
                elements.append(Paragraph(text, styles['CustomHeading2']))
            else:
                text = clean_html(line)
                if text.strip():
                    elements.append(Paragraph(text, styles['CustomBody']))
            elements.append(Spacer(1, 6))

    # Build PDF
    doc.build(elements)

if __name__ == '__main__':
    create_pdf()
