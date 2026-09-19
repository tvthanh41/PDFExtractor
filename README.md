# PDF Data Extractor

A modern, fast, PySide6-based desktop application for extracting structured data from PDF files using rule-based templates. Supports extracting via exact text anchor relative positioning, or via percentage-based bounding box extraction. 

## Features
- **Visual Template Editor**: Create extraction rules (Anchors and Bounding Boxes) interactively on a PDF canvas.
- **Save & Load Templates**: Export your rules into JSON `.pdftpl` files to share or reuse.
- **Live Preview**: Instantly preview extraction results against the current document.
- **Batch Processing**: Run templates over entire directories of PDFs simultaneously using multi-core parallel processing, then export the structured results to CSV.

## Requirements
- Python 3.11+
- Windows / macOS / Linux

## Setup Instructions

1. **Clone the repository:**
   ```bash
   git clone <repository_url>
   cd pdf-data-extractor
   ```

2. **Create and activate a virtual environment:**
   ```bash
   python -m venv .venv
   # Windows:
   .venv\Scripts\activate
   # macOS/Linux:
   source .venv/bin/activate
   ```

3. **Install Dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

## Running the Application

To start the PDF Data Extractor application:

```bash
python src/main.py
```

## Running Tests

Integration and Unit tests use `pytest`:

```bash
pytest
```
