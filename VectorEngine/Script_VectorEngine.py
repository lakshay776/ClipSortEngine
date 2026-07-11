import faiss 
import numpy as np
from PreProcessing.Paths import BASE_DIR
from models.Embeddings import encode_passages, encode_query_batch
from PreProcessing.Paths import TEMP_TEXT
from PreProcessing.Chunker import chunker 
import json

def _chunk_with_lines(script, context_words=10):
    """Split script into chunks with surrounding context, tracking source line numbers."""
    # Keep (line_number, text) for non-empty lines
    lines = [
        (i + 1, line.strip())
        for i, line in enumerate(script.splitlines())
        if line.strip()
    ]

    chunks = []      # chunk text
    line_numbers = [] # center line number for each chunk

    for i, (lineno, sentence) in enumerate(lines):
        prev_context = ""
        next_context = ""

        if i > 0:
            prev_words = lines[i - 1][1].split()
            prev_context = " ".join(prev_words[-context_words:])

        if i < len(lines) - 1:
            next_words = lines[i + 1][1].split()
            next_context = " ".join(next_words[:context_words])

        chunk = f"{prev_context} {sentence} {next_context}".strip()
        chunks.append(chunk)
        line_numbers.append(lineno)

    return chunks, line_numbers

def vector_engine(script_file):
    all_embeddings = []
    with open(script_file, "r", encoding="utf-8") as file:
        script = file.read()

    chunks, line_numbers = _chunk_with_lines(script)
    embeddings = encode_passages(chunks)
    metadata = []
    for chunk, emb, lineno in zip(chunks, embeddings, line_numbers):
        all_embeddings.append(emb)
        metadata.append({
            "file_path": str(script_file),
            "line_number": lineno,
            "content": chunk
        })

    passage_vecs = np.array(all_embeddings).astype("float32")

    # Also encode as "query: " vectors — used by Search.py at search time (no model needed)
    query_embeddings = encode_query_batch(chunks)
    query_vecs = np.array(query_embeddings).astype("float32")

    dimension = passage_vecs.shape[1]

    # passage index — for being retrieved
    passage_index = faiss.IndexFlatIP(dimension)
    passage_index.add(passage_vecs)

    # query index — for doing the searching
    query_index = faiss.IndexFlatIP(dimension)
    query_index.add(query_vecs)

    vector_store_dir = BASE_DIR / "VectorStore"
    vector_store_dir.mkdir(parents=True, exist_ok=True)
    faiss.write_index(passage_index, str(vector_store_dir / "Script_vector_store.faiss"))
    faiss.write_index(query_index,   str(vector_store_dir / "Script_query_store.faiss"))
    with open(vector_store_dir / "Script_metadata.json", "w", encoding="utf-8") as file:
        json.dump(metadata, file, indent=2, ensure_ascii=False)
    
    print(f"Stored {passage_index.ntotal} script vectors (passage + query indexes)")