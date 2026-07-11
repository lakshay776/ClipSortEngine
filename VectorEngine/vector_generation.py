import faiss 
import numpy as np
from PreProcessing.Paths import BASE_DIR
from models.Embeddings import encode_passages
from PreProcessing.Paths import TEMP_TEXT
import json
from PreProcessing.Chunker import chunker

def vector_engine(transcriptions):
    all_embeddings = []
    metadata=[]
    for file_path in transcriptions:
        with open(file_path,"r",encoding="utf-8") as file:
            text = file.read()

        chunks = chunker(text)
        embeddings = encode_passages(chunks)

        for chunk, embedding in zip(chunks, embeddings):
            all_embeddings.append(embedding)
            metadata.append({
                "file_path": str(file_path),
                "content": chunk
            })

    vectors = np.array(all_embeddings).astype("float32")

    dimension = vectors.shape[1]

    index = faiss.IndexFlatIP(dimension)

    index.add(vectors)
    vector_store_dir = BASE_DIR / "VectorStore"
    vector_store_dir.mkdir(parents=True, exist_ok=True)
    faiss.write_index(index, str(vector_store_dir / "transcription_vector_store.faiss"))
    with open(vector_store_dir / "transcription_metadata.json", "w", encoding="utf-8") as file:
        json.dump(metadata, file, indent=2, ensure_ascii=False)
    
    print(f"Stored {index.ntotal} vectors")


