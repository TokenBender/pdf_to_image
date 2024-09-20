# PDF to Images CLI

A command-line tool to convert PDF files into JPEG images with support for sampling and parallel processing.

## Features

- Convert PDFs to JPEGs: Transform PDF pages into high-quality JPEG images.
- Page Sampling: Specify the percentage of pages to convert from each PDF.
- Parallel Processing: Utilize multiple CPU cores for faster conversions.
- Progress Indicator: Visualize the conversion progress with a progress bar.

## Installation

1. Clone the repository:

    ```bash
    git clone https://github.com/yourusername/pdf-to-images-cli.git
    cd pdf-to-images-cli
    ```

2. Create a virtual environment (optional but recommended):

    ```bash
    python -m venv venv
    source venv/bin/activate  # On Windows: venv\Scripts\activate
    ```

3. Install the required dependencies:

    ```bash
    pip install -r requirements.txt
    ```

## Usage

Run the CLI tool using the following command:

```bash
python pdf_to_images_cli.py [PDF_PATHS] [--sample SAMPLE_PERCENTAGE]
```

### Arguments

- `PDF_PATHS`: One or more paths to the PDF files you want to convert.

### Options

- `--sample`: Percentage of pages to sample from each PDF (0-100). Defaults to `100` (all pages).

### Examples

- **Convert all pages of a single PDF**:

    ```bash
    python pdf_to_images_cli.py /path/to/file.pdf
    ```

- **Convert 50% of pages from multiple PDFs**:

    ```bash
    python pdf_to_images_cli.py /path/to/file1.pdf /path/to/file2.pdf --sample 50
    ```

## Output

Converted JPEG images will be saved in subdirectories named after each PDF file within the same directory as the PDFs.