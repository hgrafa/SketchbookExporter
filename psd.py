import os
from Models.ProgressBar import ProgressBar
from PyPDF2 import PdfWriter
from psd_tools import PSDImage
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas


def create_folder(folder_name):
    try:
        os.mkdir(folder_name)
    except FileExistsError:
        pass


def delete_folder(folder_name):
    try:
        os.rmdir(folder_name)
    except FileNotFoundError:
        pass


def parse_psd_document(psd_document):
    psd = PSDImage.open(psd_document)

    for layer in psd._layers:
        layer.visible = False

    return psd


def save_layer_as_img(layer, layer_name):
    layer.visible = True
    psd.composite().save(f'images/{layer_name}.png')
    layer.visible = False


def save_img_as_page(layer_name):
    pdf = canvas.Canvas(f'pages/{layer_name}.pdf', pagesize=letter)
    pdf.drawImage(f'images/{layer_name}.png', 0, 0,
                  width=pdf_width, height=pdf_height)
    pdf.save()


def merge_pages(output_filename):
    folder_path = 'pages'
    pdf_files = [f for f in os.listdir(folder_path) if f.endswith('.pdf')]

    merger = PdfWriter()

    for pdf_file in pdf_files:
        file_path = os.path.join(folder_path, pdf_file)
        with open(file_path, 'rb') as f:
            merger.append(f)

    # Salvar o arquivo mesclado
    merged_path = os.path.join(folder_path, f'../pdfs/{output_filename}.pdf')
    with open(merged_path, 'wb') as f:
        merger.write(f)

    print(f'File generated: {output_filename}.pdf')


psd = parse_psd_document('file.psd')
pdf = canvas.Canvas('aula.pdf', pagesize=letter)
pdf_width, pdf_height = letter
number_of_pages = len(psd._layers)-1
progress_bar = ProgressBar(number_of_pages)

create_folder('images')
create_folder('pages')

for i, layer in enumerate(psd._layers):

    layer.visible = True

    if i == 0:
        continue

    progress_bar.advance()
    layer_name = f'camada_{i:03d}'
    save_layer_as_img(layer, layer_name)
    save_img_as_page(layer_name)

    # Esconde a camada

merge_pages('aula1')
# delete_folder('layers')
# delete_folder('pages')
