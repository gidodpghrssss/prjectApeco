import markdown
import pdfkit
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
    css = '''
    <style>
        body {
            font-family: Arial, sans-serif;
            line-height: 1.6;
            max-width: 800px;
            margin: 0 auto;
            padding: 20px;
        }
        h1 {
            color: #2E7D32;
            border-bottom: 2px solid #2E7D32;
            padding-bottom: 5px;
        }
        h2 {
            color: #1B5E20;
            margin-top: 20px;
        }
        h3 {
            color: #2E7D32;
        }
        code {
            background: #f4f4f4;
            padding: 2px 5px;
            border-radius: 3px;
        }
        pre {
            background: #f4f4f4;
            padding: 15px;
            border-radius: 5px;
            overflow-x: auto;
        }
        table {
            border-collapse: collapse;
            width: 100%;
            margin: 15px 0;
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
    </style>
    '''
    
    # Complete HTML document
    html = f'''
    <!DOCTYPE html>
    <html>
    <head>
        <meta charset="UTF-8">
        {css}
    </head>
    <body>
        {html_content}
    </body>
    </html>
    '''
    
    # Save HTML file
    with open('docs/temp.html', 'w', encoding='utf-8') as f:
        f.write(html)
    
    # Convert to PDF
    options = {
        'page-size': 'A4',
        'margin-top': '2cm',
        'margin-right': '2cm',
        'margin-bottom': '2cm',
        'margin-left': '2cm',
        'encoding': 'UTF-8',
        'custom-header': [
            ('Accept-Encoding', 'gzip')
        ],
        'no-outline': None,
        'enable-local-file-access': None
    }
    
    pdfkit.from_file('docs/temp.html', 'docs/Documentacion_Bienes_Raices_IA.pdf', options=options)
    
    # Clean up temporary file
    os.remove('docs/temp.html')

if __name__ == '__main__':
    markdown_to_pdf()
