import fitz  # PyMuPDF
import os

def split_a2_pdf_to_a4s(folder_path, output_folder):
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    for filename in os.listdir(folder_path):
        if filename.endswith(".pdf"):
            input_path = os.path.join(folder_path, filename)
            output_path = os.path.join(output_folder, filename)

            with fitz.open(input_path) as doc:
                # Assuming the A2 page is in landscape orientation
                page = doc[0]
                rect = page.rect
                width, height = rect.width, rect.height
                a4_width, a4_height = width / 2, height / 2

                # Define the four quarters
                top_left = fitz.Rect(0, 0, a4_width, a4_height)
                top_right = fitz.Rect(a4_width, 0, width, a4_height)
                bottom_left = fitz.Rect(0, a4_height, a4_width, height)
                bottom_right = fitz.Rect(a4_width, a4_height, width, height)
                areas = [top_left, top_right, bottom_left, bottom_right]

                new_doc = fitz.open()
                for area in areas:
                    new_page = new_doc.new_page(width = a4_width, height = a4_height)
                    new_page.show_pdf_page(new_page.rect, doc, page.number, clip=area)

                new_doc.save(output_path)

folder_path = 'path/to/your/a2_pdfs'
output_folder = 'path/to/output_folder'
split_a2_pdf_to_a4s(folder_path, output_folder)
