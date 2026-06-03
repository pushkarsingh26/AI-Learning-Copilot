import fitz  # PyMuPDF
from langchain_core.documents import Document
from langchain_text_splitters import RecursiveCharacterTextSplitter

def load_and_split_pdf(file_path: str) -> list[Document]:
    doc = fitz.open(file_path)
    text = ""
    for page in doc:
        text += page.get_text() + "\n"
    
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=1000,
        chunk_overlap=200
    )
    chunks = text_splitter.split_text(text)
    
    # Store source metadata
    documents = [Document(page_content=chunk, metadata={"source": file_path}) for chunk in chunks]
    return documents
