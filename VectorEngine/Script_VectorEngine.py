import faiss 
import numpy as np
from PreProcessing.Paths import BASE_DIR
from models.Embeddings import embedding_model
from PreProcessing.Paths import TEMP_TEXT


def vector_engine(transcriptions):
    all_embeddings = []
  
    for file_path in transcriptions:
        with open(file_path,"r",encoding="utf-8") as file:
            text = file.read()

        embedding = embedding_model.encode(text)

        all_embeddings.append(embedding)

    vectors = np.array(all_embeddings).astype("float32")

    dimension = vectors.shape[1]

    index = faiss.IndexFlatL2(dimension)

    index.add(vectors)
    vector_store_dir = BASE_DIR / "VectorStore"
    vector_store_dir.mkdir(parents=True, exist_ok=True)
    faiss.write_index(index, str(vector_store_dir / "vector_store.faiss"))

    print(f"Stored {index.ntotal} vectors")