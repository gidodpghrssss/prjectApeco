from fpdf import FPDF
import markdown2
import textwrap

class PDF(FPDF):
    def header(self):
        # Logo
        self.set_font('Arial', 'B', 15)
        self.set_text_color(46, 125, 50)  # Green color
        self.cell(0, 10, 'Bienes Raíces con IA', 0, 1, 'C')
        self.ln(10)

    def footer(self):
        self.set_y(-15)
        self.set_font('Arial', 'I', 8)
        self.cell(0, 10, f'Página {self.page_no()}', 0, 0, 'C')

def create_pdf():
    # Read the Markdown content
    with open('docs/documentacion_completa.md', 'r', encoding='utf-8') as f:
        markdown_content = f.read()

    # Convert Markdown to HTML
    html = markdown2.markdown(markdown_content)

    # Create PDF
    pdf = PDF()
    pdf.add_page()
    pdf.set_auto_page_break(auto=True, margin=15)

    # Title
    pdf.set_font('Arial', 'B', 20)
    pdf.set_text_color(46, 125, 50)
    pdf.cell(0, 10, 'Documentación Completa', 0, 1, 'C')
    pdf.ln(10)

    # Content
    pdf.set_font('Arial', '', 11)
    pdf.set_text_color(0, 0, 0)

    # Split content into lines and add to PDF
    lines = html.split('\n')
    for line in lines:
        if line.startswith('# '):  # Main headers
            pdf.set_font('Arial', 'B', 16)
            pdf.set_text_color(46, 125, 50)
            pdf.ln(5)
            pdf.cell(0, 10, line[2:], 0, 1)
            pdf.ln(5)
        elif line.startswith('## '):  # Sub headers
            pdf.set_font('Arial', 'B', 14)
            pdf.set_text_color(27, 94, 32)
            pdf.ln(5)
            pdf.cell(0, 10, line[3:], 0, 1)
        elif line.startswith('### '):  # Sub sub headers
            pdf.set_font('Arial', 'B', 12)
            pdf.set_text_color(46, 125, 50)
            pdf.cell(0, 10, line[4:], 0, 1)
        else:  # Normal text
            pdf.set_font('Arial', '', 11)
            pdf.set_text_color(0, 0, 0)
            # Wrap text to fit page width
            for wrapped_line in textwrap.wrap(line, width=90):
                pdf.cell(0, 10, wrapped_line, 0, 1)

    # Save the PDF
    pdf.output('docs/Documentacion_Bienes_Raices_IA.pdf', 'F')

if __name__ == '__main__':
    create_pdf()
