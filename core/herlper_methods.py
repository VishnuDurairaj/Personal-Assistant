import fitz  # PyMuPDF
import os
import shutil

def pdf_to_images(pdf_path, output_folder, zoom_factor=2):
    """
    Converts each page of the given PDF into zoomed images and saves them in the specified output folder.

    :param pdf_path: Path to the input PDF file.
    :param output_folder: Folder where the images will be saved.
    :param zoom_factor: Zoom factor for the images (default is 1.5, i.e., 150%).
    """
    # Open the PDF
    pdf_document = fitz.open(pdf_path)

    # Ensure the output folder exists
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)
    else:
        shutil.rmtree(output_folder)
        os.makedirs(output_folder)

    # Iterate through the pages
    for page_num in range(pdf_document.page_count):
        # Get the page
        page = pdf_document.load_page(page_num)

        # Define the zoom matrix (scale)
        mat = fitz.Matrix(zoom_factor, zoom_factor)  # Zoom the image by the zoom_factor

        # Get the pixmap (image) from the page with zoom
        pix = page.get_pixmap(matrix=mat)

        # Define the output image path
        image_path = os.path.join(output_folder, f"page_{page_num + 1}_zoomed.png")

        # Save the zoomed image
        pix.save(image_path)

        print(f"Saved {image_path}")
    
    # Close the PDF document
    pdf_document.close()

    return output_folder


# Example usage:
# pdf_to_images("2024-FC-EROLLGEN-S10-46-FinalRoll-Revision2-ENG-3-WI.pdf", "output_images")
