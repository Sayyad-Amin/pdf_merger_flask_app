import os
import sys
from PyPDF2 import PdfReader, PdfWriter
from utils.pdf_merger import merge_pdfs

def create_simple_pdf(output_path, num_pages=1):
    """Create a simple valid PDF file with the specified number of pages."""
    # Create a PDF with reportlab which will have proper text content
    from reportlab.pdfgen import canvas
    from reportlab.lib.pagesizes import letter
    
    c = canvas.Canvas(output_path, pagesize=letter)
    for i in range(num_pages):
        c.drawString(100, 700, f"This is page {i+1} of test PDF")
        c.drawString(100, 680, "Created for testing PDF merge functionality")
        c.drawString(100, 660, "This content should be preserved in the merged PDF")
        c.drawString(100, 640, "Line 4 of test content")
        c.drawString(100, 620, "Line 5 of test content")
        
        # Draw a rectangle to add some graphics content
        c.rect(90, 610, 200, 100, stroke=1, fill=0)
        
        # Add page number at bottom
        c.drawString(300, 50, f"Page {i+1} of {num_pages}")
        
        if i < num_pages - 1:
            c.showPage()  # Add a new page
    
    c.save()
    return output_path

def test_pdf_merger():
    """Test the PDF merger functionality."""
    print("Creating test PDFs...")
    
    # Create directory for test files if it doesn't exist
    test_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'uploads', 'test')
    os.makedirs(test_dir, exist_ok=True)
    
    # Create test PDFs
    test_pdf1 = os.path.join(test_dir, 'test1.pdf')
    test_pdf2 = os.path.join(test_dir, 'test2.pdf')
    create_simple_pdf(test_pdf1, 1)
    create_simple_pdf(test_pdf2, 2)
    
    print(f"Created test PDF: {test_pdf1} with 1 pages")
    print(f"Created test PDF: {test_pdf2} with 2 pages")
    print()
    
    # Test merging
    print("Testing PDF merger...")
    output_path = os.path.join(test_dir, 'merged_output.pdf')
    
    try:
        # Perform the merge
        merged_path, total_pages = merge_pdfs([test_pdf1, test_pdf2], output_path)
        
        print(f"Success! Merged 2 PDFs into {merged_path} with {total_pages} pages.")
        print()
        
        # Verify the merged PDF
        with open(merged_path, 'rb') as f:
            pdf = PdfReader(f)
            page_count = len(pdf.pages)
            print(f"Verification: Merged PDF has {page_count} pages")
            
            # Check if pages have content
            empty_pages = 0
            for i in range(page_count):
                page = pdf.pages[i]
                if '/Contents' not in page:
                    print(f"Warning: Page {i+1} has no content")
                    empty_pages += 1
            
            if empty_pages == 0:
                print("All pages in the merged PDF have content")
        
        print(f"\nDone testing. Check the merged PDF at: {merged_path}")
        return True
    except Exception as e:
        print(f"Error during test: {str(e)}")
        return False

def merge_from_command_line():
    """Merge PDFs from command line arguments."""
    if len(sys.argv) < 3:
        print(f"Usage: python {sys.argv[0]} pdf1.pdf pdf2.pdf [pdf3.pdf ...]")
        return
    
    input_files = sys.argv[1:]
    output_file = 'merged_output.pdf'
    
    try:
        output_path, total_pages = merge_pdfs(input_files, output_file)
        print(f"Successfully merged {len(input_files)} PDFs into {output_path} with {total_pages} pages")
    except Exception as e:
        print(f"Error merging PDFs: {str(e)}")

if __name__ == "__main__":
    if len(sys.argv) > 1:
        # Command line mode
        merge_from_command_line()
    else:
        # Test mode
        print(f"Usage: python {sys.argv[0]} pdf1.pdf pdf2.pdf [pdf3.pdf ...]")
        test_pdf_merger()