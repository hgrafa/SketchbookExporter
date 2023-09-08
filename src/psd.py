import os
import Utils.folder as folder
from PyPDF2 import PdfWriter
from psd_tools import PSDImage
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas

def parse_psd_document(psd_document):
    psd = PSDImage.open(psd_document)

    for layer in psd._layers:
        layer.visible = False

    return psd

def save_layer_as_img(layer, layer_name):
    layer.visible = True
    psd.composite().save(f'Temp/{layer_name}.png')
    layer.visible = False

def save_img_as_page(layer_name):
    pdf = canvas.Canvas(f'Temp/{layer_name}.pdf', pagesize=letter)
    pdf.drawImage(f'Temp/{layer_name}.png', 0, 0,
                  width=pdf_width, height=pdf_height)
    pdf.save()

def merge_pages(output_filename):
    folder_path = 'Temp'
    pdf_files = [f for f in os.listdir(folder_path) if f.endswith('.pdf')]

    merger = PdfWriter()

    for pdf_file in pdf_files:
        file_path = os.path.join(folder_path, pdf_file)
        with open(file_path, 'rb') as f:
            merger.append(f)

    # Salvar o arquivo mesclado
    merged_path = os.path.join(folder_path, f'../Output/{output_filename}.pdf')
    with open(merged_path, 'wb') as f:
        merger.write(f)

# ----------------------------------------------------------

start = 25
number = 25

for file_number in range(start, number+1):
    psd = parse_psd_document(f'Psd/{file_number}.psd')
    pdf = canvas.Canvas('aula.pdf', pagesize=letter)
    pdf_width, pdf_height = letter
    number_of_pages = len(psd._layers) - 1

    # ----------------------------------------------------------

    folder.create('Temp')

    for i, layer in enumerate(psd._layers):

        if i == 0:
            continue

        layer.visible = True

        layer_name = f'{i:03d}'
        save_layer_as_img(layer, layer_name)
        save_img_as_page(layer_name)
        # Esconde a camada

    merge_pages(f'{file_number}')
    print(f'PDF {file_number} gerado.')
    folder.clear('Temp/')
