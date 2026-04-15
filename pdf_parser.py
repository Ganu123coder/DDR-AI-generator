import fitz  # PyMuPDF
import os

def extract_text_and_images(pdf_path, output_folder="images"):
    doc = fitz.open(pdf_path)
    text = ""
    images = []

    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    for page_num, page in enumerate(doc):
        text += page.get_text()

        image_list = page.get_images(full=True)
        for img_index, img in enumerate(image_list):
            xref = img[0]
            base_image = doc.extract_image(xref)
            image_bytes = base_image["image"]

            image_filename = f"{output_folder}/img_{page_num}_{img_index}.png"
            with open(image_filename, "wb") as f:
                f.write(image_bytes)

            images.append(image_filename)

    return text, images