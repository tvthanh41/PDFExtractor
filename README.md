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

## How to Use the App

The core concept behind PDF Data Extractor is that many forms, invoices, and reports follow a predictable structure. We provide two main approaches to extract text from these documents:

1. **Bounding Box (Region) Extraction**: 
   Draw a box over a specific area of the page. The app will extract whatever text falls within that relative percentage coordinate. This is great for highly standardized forms where the text you need is always in the exact same physical location.
   
2. **Anchor-based Extraction**: 
   Sometimes, documents shift slightly or grow in length, making fixed bounding boxes unreliable. Instead, you can define an "Anchor Text" (e.g., `"Total Amount:"`). The app will first locate that specific word on the page, and then look for your target data at a relative offset (e.g., right next to it, or just below it). This method is highly robust against formatting shifts.

**Basic Workflow:**
1. Go to **File -> New Template** and select a sample PDF.
2. Add a rule by clicking **Add Rule**. Choose whether it's an Anchor or a Bounding Box rule.
3. Draw a selection over the canvas to define where the data (or anchor) is located.
4. Preview the rule to ensure it extracts the right text.
5. Save the template (`.pdftpl`).
6. Go to **File -> Run Batch**, select your saved template, and choose a folder full of PDFs. The app will extract the data from all of them and save it to a `.csv` file.

## Running the Application

To start the PDF Data Extractor application from source:

```bash
python src/main.py
```

Alternatively, download the standalone executable from the Releases page and run it directly!

## Credits & Open Source Dependencies

This application is made possible thanks to several excellent open source projects:
- **[PySide6](https://doc.qt.io/qtforpython-6/)**: The official Python binding for the Qt GUI framework, powering our responsive and modern user interface.
- **[PyMuPDF](https://pymupdf.readthedocs.io/)**: A high-performance PDF rendering and text extraction library that drives our backend parsing engine.
- **[PyInstaller](https://pyinstaller.org/)**: Used to bundle the application and its dependencies into a standalone executable.
- **[Pytest](https://docs.pytest.org/) & [pytest-qt](https://pytest-qt.readthedocs.io/)**: Our testing framework for ensuring reliability and regression prevention.

## Running Tests

Integration and Unit tests use `pytest`:

```bash
pytest
```
