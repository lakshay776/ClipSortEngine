from PreProcessing.Paths import BASE_DIR
import faiss
import numpy as np
import json

# ── Paths ────────────────────────────────────────────────────────────────────
VECTOR_STORE             = BASE_DIR / "VectorStore"
SCRIPT_QUERY_INDEX_PATH  = VECTOR_STORE / "Script_query_store.faiss"   # "query:" vectors
SCRIPT_META_PATH         = VECTOR_STORE / "Script_metadata.json"
TRANSCRIPT_INDEX_PATH    = VECTOR_STORE / "transcription_vector_store.faiss"
TRANSCRIPT_META_PATH     = VECTOR_STORE / "transcription_metadata.json"

TOP_K = 3   # how many nearest transcription chunks to return per script chunk

def search():

    # Load both indexes — no embedding model needed at search time
    script_query_index = faiss.read_index(str(SCRIPT_QUERY_INDEX_PATH))
    transcript_index   = faiss.read_index(str(TRANSCRIPT_INDEX_PATH))

    with open(SCRIPT_META_PATH, "r", encoding="utf-8") as f:
        script_meta = json.load(f)

    with open(TRANSCRIPT_META_PATH, "r", encoding="utf-8") as f:
        transcript_meta = json.load(f)

    n_scripts     = script_query_index.ntotal
    n_transcripts = transcript_index.ntotal

    results = []

    for idx in range(n_scripts):
        # Pure memory lookup — reconstruct the stored "query:" vector
        query_vec = script_query_index.reconstruct(idx).reshape(1, -1)

        scores, indices = transcript_index.search(query_vec, TOP_K)

        matches = []
        for rank, (score, t_idx) in enumerate(zip(scores[0], indices[0]), start=1):
            if t_idx == -1:      # FAISS returns -1 when not enough results
                continue
            matches.append({
                "rank":         rank,
                "cosine_score": float(round(score, 4)),   # 1.0 = identical
                "transcript":   transcript_meta[t_idx],
            })

        results.append({
            "script_chunk": script_meta[idx],
            "top_matches":  matches,
        })

    # ── Print results ─────────────────────────────────────────────────────────
    for res in results:
        sc = res["script_chunk"]
        print(f"\n{'='*70}")
        print(f"SCRIPT  line {sc['line_number']}: {sc['content'][:80]}...")
        print(f"{'─'*70}")
        for m in res["top_matches"]:
            tm = m["transcript"]
            content = tm.get("content") or tm.get("text") or str(tm)
            print(f"  [{m['rank']}] score={m['cosine_score']:.4f}  {content[:80]}...")

    print(f"\nDone. Matched {n_scripts} script chunks against {n_transcripts} transcription chunks.")
