import glob
from src.ingest import build_vectorstore

pdf_files = glob.glob("data/*.pdf")
print(f"Found {len(pdf_files)} PDF(s): {pdf_files}")

build_vectorstore(pdf_files)