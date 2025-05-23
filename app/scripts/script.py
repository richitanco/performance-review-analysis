import chromadb
from chromadb.utils import embedding_functions
import os
import docx
import PyPDF2
from langchain.text_splitter import CharacterTextSplitter

splitter = CharacterTextSplitter(separator=' ',chunk_size=250, chunk_overlap=175)
default_ef = embedding_functions.DefaultEmbeddingFunction()

def read_docx(file_path):
    try:
        doc = docx.Document(file_path)
        full_text = []
        for para in doc.paragraphs:
            full_text.append(para.text.lower())
        
        full_text = splitter.split_text(' '.join(full_text))
        return full_text
    except Exception as e:
        print(f"Error reading {file_path}: {e}")
        return None

def read_pdf(file_path):
    try:
        with open(file_path, 'rb') as pdf_file:
            pdf_reader = PyPDF2.PdfReader(pdf_file)
            full_text = []
            for page in pdf_reader.pages:
                full_text.append(page.extract_text().lower())
            
            full_text = splitter.split_text(' '.join(full_text))
            return full_text
    except Exception as e:
        print(f"Error reading {file_path}: {e}")
        return None

chromadb_client = chromadb.HttpClient(host="localhost", port=8000)
print("ChromaDB client initialized")
list_collections = chromadb_client.list_collections()

if "documents" in list_collections:
    chromadb_client.delete_collection("documents")
    print("Deleted existing collection 'documents'")
    collection = chromadb_client.get_or_create_collection(name="documents", metadata={"hnsw:space": "cosine"},embedding_function=default_ef)
    print("Created new collection 'documents'")
else:
    # Create or get a collection
    collection = chromadb_client.get_or_create_collection(name="documents", metadata={"hnsw:space": "cosine"},embedding_function=default_ef)
    print("Created new collection 'documents'")

DOCS_PATH = "documents"

documents_to_add = []
ids_to_add = []
metadatas_to_add = []
doc_id = 0
for root,_,files in os.walk(DOCS_PATH):
    
    for file_name in files:
        doc_id += 1
        file_path = os.path.join(root, file_name)
        file_content = None
        file_extension = ''

        if file_name.endswith(".docx"):
            file_content = read_docx(file_path)
            file_extension = "docx"
        elif file_name.endswith(".pdf"):
            file_content = read_pdf(file_path)
            file_extension = "pdf"
        else:
            print(f"Skipping unsupported file type: {file_name}")
            continue
    
        if file_content is not None:
            relative_path_id = os.path.relpath(file_path, start=os.getcwd()).replace("\\", "/")
            # Using relative file path as ID for uniqueness
            
            for i,content in enumerate(file_content):
                if content.strip():
                    relative_path_id += f"_{i + 1}_{len(file_content)}"
                    ids_to_add.append(relative_path_id)
                    documents_to_add.append(content)
                    metadatas_to_add.append(
                        {"doc_id":doc_id,
                         "source": relative_path_id, 
                         "type": file_extension, 
                         "file_name": file_name, 
                         "chunk": i+1, 
                         "total_chunks": len(file_content)}
                         )
        
        elif file_content is None:
            print(f"Error reading {file_name}")
        else:
            print(f"File {file_path} is empty or contains only whitespace.")

if documents_to_add:
    try:
        collection.add(
            documents=documents_to_add,
            ids=ids_to_add,
            metadatas=metadatas_to_add,

        )
        print("Added documents to ChromaDB collections:    documents     ")
    except Exception as e:
        print("No new documents found or processed.")