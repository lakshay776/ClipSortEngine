from sentence_transformers import SentenceTransformer

# intfloat/multilingual-e5-small REQUIRES prefixes:
#   "passage: " for text being stored (documents/chunks)
#   "query: "   for text being searched
# Without these the model is miscalibrated and scores are meaningless.
embedding_model = SentenceTransformer('intfloat/multilingual-e5-small')

def encode_passages(texts):
    """Use this when encoding chunks to store in FAISS."""
    prefixed = [f"passage: {t}" for t in texts]
    return embedding_model.encode(prefixed, normalize_embeddings=True)

def encode_query(text):
    """Use this when encoding a single search query."""
    return embedding_model.encode(f"query: {text}", normalize_embeddings=True)

def encode_query_batch(texts):
    """Use this when encoding a batch of texts as queries (e.g. to build a query FAISS index)."""
    prefixed = [f"query: {t}" for t in texts]
    return embedding_model.encode(prefixed, normalize_embeddings=True)