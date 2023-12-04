import tkinter as tk
from tkinter import filedialog
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
                page = doc[0]
                rect = page.rect
                width, height = rect.width, rect.height
                a4_width, a4_height = width / 2, height / 2

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

def select_input_folder():
    folder_selected = filedialog.askdirectory()
    input_folder_entry.delete(0, tk.END)
    input_folder_entry.insert(0, folder_selected)

def select_output_folder():
    folder_selected = filedialog.askdirectory()
    output_folder_entry.delete(0, tk.END)
    output_folder_entry.insert(0, folder_selected)

def start_processing():
    input_folder = input_folder_entry.get()
    output_folder = output_folder_entry.get()
    split_a2_pdf_to_a4s(input_folder, output_folder)
    status_label.config(text="Processing Complete")

# Set up the Tkinter window
window = tk.Tk()
window.title("A2 to A4 PDF Splitter")

# Create layout
input_folder_label = tk.Label(window, text="Input Folder:")
input_folder_label.pack()
input_folder_entry = tk.Entry(window, width=50)
input_folder_entry.pack()
input_folder_button = tk.Button(window, text="Browse", command=select_input_folder)
input_folder_button.pack()

output_folder_label = tk.Label(window, text="Output Folder:")
output_folder_label.pack()
output_folder_entry = tk.Entry(window, width=50)
output_folder_entry.pack()
output_folder_button = tk.Button(window, text="Browse", command=select_output_folder)
output_folder_button.pack()

start_button = tk.Button(window, text="Start Processing", command=start_processing)
start_button.pack()

status_label = tk.Label(window, text="")
status_label.pack()

# Run the application
window.mainloop()
