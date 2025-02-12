import markdown
from weasyprint import HTML, CSS
from weasyprint.text.fonts import FontConfiguration
import os

def markdown_to_pdf():
    # Read the Markdown content
    with open('docs/documentacion_completa.md', 'r', encoding='utf-8') as f:
        markdown_content = f.read()
    
    # Convert Markdown to HTML
    html_content = markdown.markdown(
        markdown_content,
        extensions=['tables', 'fenced_code', 'codehilite', 'toc']
    )
    
    # Add CSS styling
    css_content = '''
    @page {
        margin: 2.5cm;
        @top-center {
            content: "Bienes Raíces con IA - Documentación";
            font-family: Arial;
            font-size: 9pt;
        }
        @bottom-center {
            content: counter(page);
            font-family: Arial;
            font-size: 9pt;
        }
    }
    body {
        font-family: Arial, sans-serif;
        font-size: 11pt;
        line-height: 1.6;
    }
    h1 {
        color: #2E7D32;
        border-bottom: 2px solid #2E7D32;
        padding-bottom: 5px;
        margin-top: 20px;
    }
    h2 {
        color: #1B5E20;
        margin-top: 15px;
    }
    h3 {
        color: #2E7D32;
    }
    code {
        background-color: #f5f5f5;
        padding: 2px 4px;
        border-radius: 4px;
        font-family: 'Courier New', monospace;
    }
    pre {
        background-color: #f5f5f5;
        padding: 10px;
        border-radius: 4px;
        overflow-x: auto;
    }
    table {
        border-collapse: collapse;
        width: 100%;
        margin: 10px 0;
    }
    th, td {
        border: 1px solid #ddd;
        padding: 8px;
        text-align: left;
    }
    th {
        background-color: #2E7D32;
        color: white;
    }
    tr:nth-child(even) {
        background-color: #f9f9f9;
    }
    '''
    
    # Create HTML with CSS
    html = f'''
    <!DOCTYPE html>
    <html>
    <head>
        <meta charset="UTF-8">
        <style>{css_content}</style>
    </head>
    <body>
        {html_content}
    </body>
    </html>
    '''
    
    # Configure fonts
    font_config = FontConfiguration()
    
    # Generate PDF
    HTML(string=html).write_pdf(
        'docs/Documentacion_Bienes_Raices_IA.pdf',
        stylesheets=[CSS(string=css_content, font_config=font_config)],
        font_config=font_config
    )

if __name__ == '__main__':
    markdown_to_pdf()
