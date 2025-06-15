# Running Instructions for PDF Generation Methods

This project contains three different methods for generating PDFs using Flask and different libraries:

- Metodo con pdfkit
- Metodo con reportlab
- Metodo con xhtml2pdf

## Prerequisites

- Python installed (recommended version 3.10 or above)
- Virtual environment setup (optional but recommended)

## Setup

1. Open a terminal.
2. Navigate to the project root directory.
3. Create and activate a virtual environment (optional but recommended):

```sh
python -m venv env
env\Scripts\activate
```

4. Install dependencies for each method by navigating to its folder and running:

```sh
pip install -U -r requirements.txt
```

## Running Each Method

For each method, open a terminal, navigate to the `src` folder inside the method folder, and run the Flask app:

### Metodo con pdfkit

```sh
cd "Metodo con pdfkit/src"
python app.py
```

Runs on port 3000. Open your browser at http://localhost:3000

### Metodo con reportlab

```sh
cd "Metodo con reportlab/src"
python app.py
```

Runs on port 3000. Open your browser at http://localhost:3000

### Metodo con xhtml2pdf

```sh
cd "Metodo con xhtml2pdf/src"
python app.py
```

Runs on port 5030. Open your browser at http://localhost:5030

## Usage

- Use the web form to upload images and generate PDFs.
- Verify the PDF is generated and displayed or downloaded as expected.

If you encounter any issues or need further assistance, please let me know.
