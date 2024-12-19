import os
from PyPDF2 import PdfMerger, PdfReader, PdfWriter
from pdf2image import convert_from_path
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter
import io


# 1 Merging pdf code

def merge_pdfs(pdf_list, output_file):
    merger= PdfMerger()
    for pdf in pdf_list:
        merger.append(pdf)
    merger.write(output_file)
    merger.close()
    print(f"Merged PDFs saved to {output_file}")
# 2 splitting pdf code
def split_pdf(input_pdf, output_dir):
    """
        Splits a PDF into individual pages and saves them separately.

        Args:
            input_pdf (str): Path to the input PDF file.
            output_dir (str): Directory where individual page PDFs will be saved.
        """
    reader=PdfReader(input_pdf)
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
    for i, page in enumerate(reader.pages):
        writer=PdfWriter()
        writer.add_page(page)
        output_file=os.path.join(output_dir, f"page_{i+1}.pdf")
        with open(output_file, "wb") as output_pdf:
            writer.write(output_pdf)
    print(f"Split PDF saved to {output_dir}")


# 3 watermark PDF


def add_watermark(input_pdf, watermark_text, output_pdf):
    """
    Adds a watermark to each page of the input PDF.

    Args:
        input_pdf (str): Path to the input PDF file.
        watermark_text (str): Text to use for the watermark.
        output_pdf (str): Path to save the watermarked PDF.

    """
    try:
        # Create a PDF containing the watermark text
        packet = io.BytesIO()
        c = canvas.Canvas(packet, pagesize=letter)
        c.setFont("Helvetica", 40)
        c.setFillColorRGB(0.8, 0.8, 0.8, alpha=0.5)  # Light gray color with transparency
        c.drawString(100, 500, watermark_text)  # Set watermark position
        c.save()
        packet.seek(0)  # Reset buffer to the beginning

        # Read the watermark PDF
        watermark_reader = PdfReader(packet)
        watermark_page = watermark_reader.pages[0]

        # Read the input PDF
        pdf_reader = PdfReader(input_pdf)
        pdf_writer = PdfWriter()

        # Add the watermark to each page
        for page in pdf_reader.pages:
            page.merge_page(watermark_page)
            pdf_writer.add_page(page)

        # Write the watermarked PDF to a new file
        with open(output_pdf, "wb") as output_file:
            pdf_writer.write(output_file)

        print(f"Watermark added successfully. Saved to {output_pdf}")
    except Exception as e:
        print(f"An error occurred while adding the watermark: {e}")

# 4 Convert PDF to Images
def pdf_to_images(input_pdf, output_dir, image_format="JPEG"):
    """
    Converts each page of a PDF to images and saves them with the same name as the input PDF.

    Args:
        input_pdf (str): Path to the input PDF file.
        output_dir (str): Directory to save the output images.
        image_format (str): Image format, "JPEG" or "PNG". Default is "JPEG".

    Returns:
        list: A list of paths to the generated image files.
    """
    # Create the output directory if it doesn’t exist
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    # Extract the base name of the input PDF (without extension)
    base_name = os.path.splitext(os.path.basename(input_pdf))[0]

    # Convert PDF pages to images
    images = convert_from_path(input_pdf)
    image_paths = []

    for i, img in enumerate(images):
        # Create output file name using the base name and page index
        image_file = os.path.join(output_dir, f"{base_name}_page_{i + 1}.{image_format.lower()}")
        img.save(image_file, image_format.upper())
        image_paths.append(image_file)

    print(f"Converted PDF '{input_pdf}' pages to images in {image_format} format at '{output_dir}'")
    return image_paths

def main():
    """
    Main function to dynamically select and run PDF operations.
    """
    while True:  # Loop to allow multiple operations in one session
        print("\nSelect an operation:")
        print("1. Merge PDFs")
        print("2. Add Watermark to a PDF")
        print("3. Split PDF into Individual Pages")
        print("4. Convert PDF to Images")
        print("5. Exit")

        # Get user's choice
        choice = input("Enter the number of the operation you'd like to execute: ").strip()

        if choice == "1":  # Merge PDFs
            pdf_list = input("Enter the paths of the PDF files to merge, separated by commas: ").strip().split(',')
            output_file = input("Enter the path for the output merged PDF: ").strip()
            try:
                merge_pdfs(pdf_list, output_file)
            except Exception as e:
                print(f"Error during merge operation: {e}")

        elif choice == "2":  # Add Watermark
            input_pdf = input("Enter the path to the input PDF file: ").strip()
            watermark_text = input("Enter the text for the watermark: ").strip()
            output_pdf = input("Enter the path for the output watermarked PDF: ").strip()
            try:
                add_watermark(input_pdf, watermark_text, output_pdf)
            except Exception as e:
                print(f"Error during watermark operation: {e}")

        elif choice == "3":  # Split PDF
            input_pdf = input("Enter the path to the input PDF file: ").strip()
            output_dir = input("Enter the path to the output directory for split pages: ").strip()
            try:
                split_pdf(input_pdf, output_dir)
            except Exception as e:
                print(f"Error during split operation: {e}")

        elif choice == "4":  # Convert PDF to Images
            input_pdf = input("Enter the path to the input PDF file: ").strip()
            output_dir = input("Enter the path to the output directory for images: ").strip()
            image_format = input("Enter the image format (JPEG/PNG). Default is JPEG: ").strip() or "JPEG"
            try:
                pdf_to_images(input_pdf, output_dir, image_format)
            except Exception as e:
                print(f"Error during image conversion: {e}")

        elif choice == "5":  # Exit
            print("Exiting the program. Goodbye!")
            break

        else:  # Invalid choice
            print("Invalid choice dummy. Please select a valid operation from the menu.")


# Execute the main function only if the script is run directly
if __name__ == "__main__":
    main()