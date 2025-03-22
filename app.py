import os
import uuid
import logging
from flask import Flask, request, jsonify, send_file, render_template
from werkzeug.utils import secure_filename
from utils.pdf_merger import merge_pdfs, is_valid_pdf, PDFMergeError
from utils.pdf_converter import PDFConverter

# Configure logging
logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'uploads')
app.config['MAX_CONTENT_LENGTH'] = 50 * 1024 * 1024  # 50MB max upload
app.config['ALLOWED_EXTENSIONS'] = {'pdf'}

# Ensure upload directory exists
if not os.path.exists(app.config['UPLOAD_FOLDER']):
    os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

def allowed_file(filename):
    """Check if the file has an allowed extension"""
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in app.config['ALLOWED_EXTENSIONS']

@app.route('/')
def index():
    """Render the main page."""
    return render_template('index.html')

@app.route('/merge', methods=['POST'])
def merge():
    """Merge uploaded PDF files."""
    try:
        logger.debug("Received merge request")
        
        # Check if any files were uploaded
        if 'files[]' not in request.files:
            logger.warning("No files in request")
            return jsonify({'error': 'No files uploaded'}), 400
            
        files = request.files.getlist('files[]')
        
        # Check if any valid files were provided
        if not files or len(files) == 0:
            logger.warning("Empty files list")
            return jsonify({'error': 'No files uploaded'}), 400
            
        # Validate file count
        if len(files) < 2:
            logger.warning("Only one file uploaded")
            return jsonify({'error': 'Please upload at least 2 PDF files to merge'}), 400
            
        # Create a unique directory for this merge operation
        merge_id = str(uuid.uuid4())
        merge_dir = os.path.join(app.config['UPLOAD_FOLDER'], merge_id)
        os.makedirs(merge_dir, exist_ok=True)
        
        # Check and save valid PDF files
        saved_files = []
        invalid_files = []
        
        for file in files:
            if file and allowed_file(file.filename):
                # Check if it's a valid PDF
                if is_valid_pdf(file):
                    # Save the file
                    safe_filename = secure_filename(file.filename)
                    file_path = os.path.join(merge_dir, safe_filename)
                    file.save(file_path)
                    saved_files.append(file_path)
                    logger.debug(f"Saved valid PDF: {safe_filename}")
                else:
                    invalid_files.append(file.filename)
                    logger.warning(f"Invalid PDF content: {file.filename}")
            else:
                # Not a PDF file
                if file and file.filename:
                    invalid_files.append(file.filename)
                    logger.warning(f"Invalid file type: {file.filename}")
        
        # Check if we have valid PDFs to merge
        if len(saved_files) < 2:
            # Clean up saved files
            for f in saved_files:
                try:
                    os.remove(f)
                except Exception as e:
                    logger.warning(f"Error removing file {f}: {str(e)}")
                    
            # Remove the merge directory if it's empty
            try:
                os.rmdir(merge_dir)
            except Exception as e:
                logger.warning(f"Error removing directory {merge_dir}: {str(e)}")
                
            return jsonify({
                'error': 'Not enough valid PDF files to merge',
                'invalid_files': invalid_files
            }), 400
        
        # Merge the PDFs
        output_filename = "merged.pdf"
        output_path = os.path.join(merge_dir, output_filename)
        
        try:
            logger.debug(f"Merging {len(saved_files)} PDFs")
            output_path, total_pages = merge_pdfs(saved_files, output_path)
            
            # Validate the merged file
            with open(output_path, 'rb') as f:
                if not is_valid_pdf(f):
                    raise PDFMergeError("Generated PDF is invalid")
            
            # Return the result with download link
            download_url = f"/download/{merge_id}/{output_filename}"
            logger.info(f"Merge successful: {total_pages} pages, download URL: {download_url}")
            
            return jsonify({
                'success': True,
                'message': f'Successfully merged {len(saved_files)} PDFs into {total_pages} pages',
                'download_url': download_url,
                'merge_id': merge_id,
                'total_pages': total_pages
            })
            
        except PDFMergeError as e:
            logger.error(f"PDF merge error: {str(e)}")
            return jsonify({
                'error': f'Error merging PDFs: {str(e)}',
                'invalid_files': invalid_files
            }), 400
        except Exception as e:
            logger.error(f"Unexpected error during merge: {str(e)}", exc_info=True)
            return jsonify({'error': f'Server error: {str(e)}'}), 500
    except Exception as e:
        logger.error(f"Server error in merge route: {str(e)}", exc_info=True)
        return jsonify({'error': f'Server error: {str(e)}'}), 500

@app.route('/download/<merge_id>/<filename>')
def download(merge_id, filename):
    """Download a merged PDF file."""
    try:
        # Validate merge_id and filename to prevent directory traversal
        if '..' in merge_id or '/' in merge_id or '\\' in merge_id:
            return jsonify({'error': 'Invalid merge ID'}), 400
            
        if '..' in filename or '/' in filename or '\\' in filename:
            return jsonify({'error': 'Invalid filename'}), 400
            
        # Get the file path
        file_path = os.path.join(app.config['UPLOAD_FOLDER'], merge_id, filename)
        
        # Check if file exists
        if not os.path.exists(file_path):
            logger.warning(f"Download requested for non-existent file: {file_path}")
            return jsonify({'error': 'File not found'}), 404
            
        # Return the file
        logger.info(f"Serving download: {file_path}")
        return send_file(file_path, as_attachment=True, download_name=filename)
    except Exception as e:
        logger.error(f"Error in download route: {str(e)}", exc_info=True)
        return jsonify({'error': f'Server error: {str(e)}'}), 500

@app.route('/convert/word', methods=['POST'])
def convert_to_word():
    """Convert PDF to Word document"""
    try:
        if 'file' not in request.files:
            return jsonify({'error': 'No file uploaded'}), 400

        file = request.files['file']
        if file and allowed_file(file.filename):
            # Save the file
            safe_filename = secure_filename(file.filename)
            file_path = os.path.join(app.config['UPLOAD_FOLDER'], safe_filename)
            file.save(file_path)

            # Convert to Word
            output_path = PDFConverter.pdf_to_word(file_path)
            return send_file(output_path, as_attachment=True)
        else:
            return jsonify({'error': 'Invalid file type'}), 400
    except Exception as e:
        logger.error(f"Error converting to Word: {str(e)}", exc_info=True)
        return jsonify({'error': f'Conversion error: {str(e)}'}), 500

@app.route('/convert/jpg', methods=['POST'])
def convert_to_jpg():
    """Convert PDF to JPG images"""
    try:
        if 'file' not in request.files:
            return jsonify({'error': 'No file uploaded'}), 400

        file = request.files['file']
        if file and allowed_file(file.filename):
            # Save the file
            safe_filename = secure_filename(file.filename)
            file_path = os.path.join(app.config['UPLOAD_FOLDER'], safe_filename)
            file.save(file_path)

            # Convert to JPG
            image_paths = PDFConverter.pdf_to_jpg(file_path)
            if len(image_paths) == 1:
                return send_file(image_paths[0], as_attachment=True)
            else:
                # Zip multiple images
                import zipfile
                from io import BytesIO
                memory_file = BytesIO()
                with zipfile.ZipFile(memory_file, 'w') as zf:
                    for image_path in image_paths:
                        zf.write(image_path, os.path.basename(image_path))
                memory_file.seek(0)
                return send_file(memory_file, as_attachment=True, download_name='converted_images.zip')
        else:
            return jsonify({'error': 'Invalid file type'}), 400
    except Exception as e:
        logger.error(f"Error converting to JPG: {str(e)}", exc_info=True)
        return jsonify({'error': f'Conversion error: {str(e)}'}), 500

@app.route('/convert/excel', methods=['POST'])
def convert_to_excel():
    """Convert PDF to Excel spreadsheet"""
    try:
        if 'file' not in request.files:
            return jsonify({'error': 'No file uploaded'}), 400

        file = request.files['file']
        if file and allowed_file(file.filename):
            # Save the file
            safe_filename = secure_filename(file.filename)
            file_path = os.path.join(app.config['UPLOAD_FOLDER'], safe_filename)
            file.save(file_path)

            # Convert to Excel
            output_path = PDFConverter.pdf_to_excel(file_path)
            return send_file(output_path, as_attachment=True)
        else:
            return jsonify({'error': 'Invalid file type'}), 400
    except Exception as e:
        logger.error(f"Error converting to Excel: {str(e)}", exc_info=True)
        return jsonify({'error': f'Conversion error: {str(e)}'}), 500

@app.route('/convert/ppt', methods=['POST'])
def convert_to_ppt():
    """Convert PDF to PowerPoint presentation"""
    try:
        if 'file' not in request.files:
            return jsonify({'error': 'No file uploaded'}), 400

        file = request.files['file']
        if file and allowed_file(file.filename):
            # Save the file
            safe_filename = secure_filename(file.filename)
            file_path = os.path.join(app.config['UPLOAD_FOLDER'], safe_filename)
            file.save(file_path)

            # Convert to PowerPoint
            output_path = PDFConverter.pdf_to_ppt(file_path)
            return send_file(output_path, as_attachment=True)
        else:
            return jsonify({'error': 'Invalid file type'}), 400
    except Exception as e:
        logger.error(f"Error converting to PowerPoint: {str(e)}", exc_info=True)
        return jsonify({'error': f'Conversion error: {str(e)}'}), 500

if __name__ == '__main__':
    app.run(debug=True)