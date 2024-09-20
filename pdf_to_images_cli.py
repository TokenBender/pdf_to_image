import multiprocessing
import random
from pathlib import Path

import typer
from pdf2image import convert_from_path
from tqdm import tqdm

CPU_COUNT = multiprocessing.cpu_count()
MAX_WORKERS = min(32, CPU_COUNT)

app = typer.Typer()

def process_pdf(pdf_path: Path, sample_percentage: int, output_dir: Path):
    """
    Converts a PDF file to JPEG images, saving them in the specified output directory.

    Args:
        pdf_path (Path): Path to the PDF file.
        sample_percentage (int): Percentage of pages to sample.
        output_dir (Path): Directory where images will be saved.

    Returns:
        tuple: (list of saved image paths, error message or None, number of pages processed)
    """
    try:
        images = convert_from_path(pdf_path)
        total_pages = len(images)

        pages_to_convert = int(total_pages * (sample_percentage / 100))
        pages_to_convert = max(1, min(pages_to_convert, total_pages))

        selected_pages = (
            sorted(random.sample(range(total_pages), pages_to_convert))
            if 0 < sample_percentage < 100
            else range(total_pages)
        )

        converted_images = []
        for page_num in selected_pages:
            image = images[page_num]
            image_filename = f"{pdf_path.stem}_page_{page_num+1}.jpg"
            image_path = output_dir / image_filename
            image.save(image_path, "JPEG", quality=85, optimize=True)
            converted_images.append(image_path)

        return converted_images, None, len(converted_images)
    except Exception as e:
        return [], f"Error processing {pdf_path.name}: {str(e)}", 0

def pdf_to_images(pdf_paths: list[Path], sample_percentage: int):
    """
    Processes multiple PDF files, converting them to images.

    Args:
        pdf_paths (list of Path): List of PDF file paths.
        sample_percentage (int): Percentage of pages to sample from each PDF.

    Returns:
        tuple: (list of all saved image paths, message string, list of skipped PDFs with errors)
    """
    all_images = []
    skipped_pdfs = []

    # Calculate total pages for progress bar
    total_pages = 0
    for pdf in pdf_paths:
        try:
            images = convert_from_path(pdf)
            total_pages += len(images)
        except Exception:
            skipped_pdfs.append(f"Failed to read {pdf.name}")
    
    with tqdm(total=total_pages, desc="Processing PDFs") as pbar:
        with multiprocessing.Pool(processes=MAX_WORKERS) as pool:
            results = [
                pool.apply_async(process_pdf, args=(pdf, sample_percentage, get_output_dir(pdf)))
                for pdf in pdf_paths
            ]
            for res in results:
                images, error, pages_processed = res.get()
                if error:
                    skipped_pdfs.append(error)
                    typer.echo(error, err=True)
                else:
                    all_images.extend(images)
                pbar.update(pages_processed)

    message = f"Saved {len(all_images)} images in their respective subfolders."
    if skipped_pdfs:
        message += f"\nSkipped {len(skipped_pdfs)} PDFs due to errors."
    typer.echo(message)
    return all_images, message, skipped_pdfs

def get_output_dir(pdf_path: Path) -> Path:
    """
    Creates and returns a subdirectory named after the PDF file for saving images.

    Args:
        pdf_path (Path): Path to the PDF file.

    Returns:
        Path: Path to the output directory.
    """
    sub_dir = pdf_path.parent / pdf_path.stem
    sub_dir.mkdir(exist_ok=True)
    return sub_dir

@app.command()
def main(
    pdfs: list[Path] = typer.Argument(..., help="Path to PDF files to convert."),
    sample: int = typer.Option(100, help="Percentage of pages to sample per PDF (0-100)."),
):
    """
    Converts PDF files to JPEG images.

    Args:
        pdfs (list of Path): List of PDF file paths.
        sample (int): Percentage of pages to sample from each PDF.
    """
    images, message, skipped = pdf_to_images(pdfs, sample)
    typer.echo(message)
    typer.echo("Process completed successfully.")

if __name__ == "__main__":
    app()