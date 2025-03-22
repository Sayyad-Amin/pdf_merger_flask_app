# PDF Merger Application

A modern web application for merging multiple PDF files into a single document.

## Features

- Drag and drop interface for file uploads
- Real-time progress tracking
- Modern UI with light/dark mode
- Secure file handling
- Responsive design for mobile and desktop
- PDF to Word conversion
- PDF to JPG conversion
- PDF to Excel conversion
- PDF to PowerPoint conversion

## Technologies Used

- Flask (Python web framework)
- PyPDF2 (PDF manipulation library)
- Modern HTML/CSS with animations
- Docker for containerization

## Running with Docker

### Prerequisites

- Docker
- Docker Compose

### Steps to Run

1. Clone the repository:
   ```
   git clone <repository-url>
   cd pdf-merger-api
   ```

2. Build and start the Docker container:
   ```
   docker-compose up -d --build
   ```

3. Access the application:
   Open your browser and navigate to `http://localhost:5000`

4. To stop the application:
   ```
   docker-compose down
   ```

## Running Without Docker

### Prerequisites

- Python 3.9+
- pip

### Steps to Run

1. Clone the repository:
   ```
   git clone <repository-url>
   cd pdf-merger-api
   ```

2. Create a virtual environment (optional but recommended):
   ```
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. Install dependencies:
   ```
   pip install -r requirements.txt
   ```

4. Run the application:
   ```
   python app.py
   ```

5. Access the application:
   Open your browser and navigate to `http://localhost:5000`

## How to Use

1. Upload PDF files by dragging and dropping them into the designated area or by clicking "Choose Files"
2. Select at least 2 PDF files
3. Click "Merge PDFs"
4. Wait for the process to complete
5. Download the merged PDF file

## License

MIT License

## Author

Your Name
