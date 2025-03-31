from langchain_community.document_loaders import PyPDFLoader

class PDFExtractor:
    def __init__(self):
        """
        Initializes the PDFExtractor.
        """
        self.name = "pdf_extractor"

    def extract_text_pypdf(self, file_path):
        """Extracts text from a PDF file and returns a list of text strings (one per page)."""
        print(" Starting PDF text extraction..")
        document_loader = PyPDFLoader(file_path)
        return document_loader.load()
