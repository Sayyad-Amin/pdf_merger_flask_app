import os
import tempfile
import logging
from typing import List, Tuple
from werkzeug.datastructures import FileStorage
from PyPDF2 import PdfReader, PdfWriter

logger = logging.getLogger(__name__)

class PDFMergeError(Exception):
    pass

def merge_pdfs(files, output_path, pdf_format='standard'):
    """
    Merge PDF files into a single PDF document
    Returns: (output_path, total_pages)
    
    Args:
        files: List of file paths or FileStorage objects
        output_path: Path to save the merged PDF
        pdf_format: Format to use for the merged PDF (not used - kept for compatibility)
    """
    file_objects = []
    opened_files = []  # Keep track of files we opened ourselves
    temp_path = None
    
    try:
        logger.debug(f"Starting PDF merge: {len(files)} files")
        
        # Validate and prepare files
        if isinstance(files[0], str):
            # Process file paths
            logger.debug(f"Processing file paths: {files}")
            
            # Open each file for processing
            for f in files:
                if not os.path.exists(f):
                    raise PDFMergeError(f"File not found: {f}")
                    
                try:
                    file_obj = open(f, 'rb')
                    file_objects.append(file_obj)
                    opened_files.append(file_obj)
                except Exception as e:
                    raise PDFMergeError(f"Cannot open file {f}: {str(e)}")
        else:
            # Process FileStorage objects
            logger.debug("Processing FileStorage objects")
            file_objects = files
        
        # Create output directory if it doesn't exist
        output_dir = os.path.dirname(output_path)
        if not os.path.exists(output_dir):
            os.makedirs(output_dir, exist_ok=True)
        
        # Create a temporary file for the output to prevent partial writes
        with tempfile.NamedTemporaryFile(delete=False, suffix='.pdf', dir=output_dir) as temp_file:
            temp_path = temp_file.name
        
        # Initialize PDF writer
        merger = PdfWriter()
        total_pages = 0
        
        # Process each input PDF
        for i, file in enumerate(file_objects):
            try:
                # Get file name for better error messages
                filename = getattr(file, 'filename', f"file_{i+1}")
                logger.debug(f"Processing PDF {i+1}/{len(file_objects)}: {filename}")
                
                # Ensure file pointer is at the beginning
                if hasattr(file, 'seek'):
                    file.seek(0)
                
                # Load the PDF and validate it
                try:
                    pdf = PdfReader(file)
                    
                    # Check for empty PDF
                    if len(pdf.pages) == 0:
                        raise PDFMergeError(f"PDF has no pages: {filename}")
                        
                    # Add each page from this PDF
                    logger.debug(f"Adding {len(pdf.pages)} pages from {filename}")
                    for page_num in range(len(pdf.pages)):
                        try:
                            # Add the page with all content
                            page = pdf.pages[page_num]
                            merger.add_page(page)
                            
                            # Try to preserve annotations if they exist
                            if '/Annots' in page:
                                try:
                                    merger.add_annotation(page['/Annots'])
                                except Exception as e:
                                    logger.warning(f"Could not preserve annotations on page {page_num}: {str(e)}")
                        except Exception as page_error:
                            logger.error(f"Error adding page {page_num} from {filename}: {str(page_error)}")
                            raise PDFMergeError(f"Error adding page {page_num} from {filename}: {str(page_error)}")
                    
                    # Update total page count
                    total_pages += len(pdf.pages)
                    
                except Exception as e:
                    raise PDFMergeError(f"Error processing PDF {filename}: {str(e)}")
                
            except PDFMergeError:
                raise
            except Exception as e:
                logger.error(f"Error processing PDF {filename}: {str(e)}", exc_info=True)
                raise PDFMergeError(f"Error processing PDF {filename}: {str(e)}")
        
        # Write the merged PDF to the temporary file
        try:
            logger.debug(f"Writing merged PDF (temp: {temp_path})")
            with open(temp_path, 'wb') as output_file:
                merger.write(output_file)
            
            # If we got here, the write was successful - move to final location
            if os.path.exists(output_path):
                os.remove(output_path)
            os.rename(temp_path, output_path)
            temp_path = None  # Prevent cleanup in finally block
            
            logger.debug(f"Successfully merged {len(file_objects)} PDFs with {total_pages} pages to {output_path}")
            return output_path, total_pages
            
        except Exception as e:
            logger.error(f"Error writing merged PDF: {str(e)}", exc_info=True)
            raise PDFMergeError(f"Error writing merged PDF: {str(e)}")
            
    except PDFMergeError:
        # Re-raise PDFMergeError exceptions
        raise
    except Exception as e:
        # Catch-all for other exceptions
        logger.error(f"Error merging PDFs: {str(e)}", exc_info=True)
        raise PDFMergeError(f'Error merging PDFs: {str(e)}')
    finally:
        # Clean up resources
        
        # Remove temporary file if it exists
        if temp_path and os.path.exists(temp_path):
            try:
                os.remove(temp_path)
                logger.debug(f"Removed temporary file {temp_path}")
            except Exception as e:
                logger.warning(f"Failed to remove temporary file {temp_path}: {str(e)}")
        
        # Close file objects that we opened
        for file_obj in opened_files:
            try:
                file_obj.close()
                logger.debug(f"Closed file {getattr(file_obj, 'name', 'unknown')}")
            except Exception as e:
                logger.warning(f"Failed to close file: {str(e)}")

def is_valid_pdf(file):
    """Validate if the uploaded file is a valid PDF"""
    try:
        reader = PdfReader(file)
        file.seek(0)  # Reset file pointer
        return True
    except Exception as e:
        logger.error(f"Error validating PDF {getattr(file, 'filename', 'unknown')}: {str(e)}")
        return False