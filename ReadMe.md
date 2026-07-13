flowchart TD
    A(["`**Input**
    Raw Video Clips
    _Assets/_`"]) --> B

    S(["`**Input**
    Shooting Script
    _VideoScript/*.txt_`"]) --> SP

    subgraph PREPROCESS ["⚙️ Pre-Processing"]
        B["🎵 Extract Audio
        _ffmpeg_"]
        B --> C["📝 Transcribe Audio
        _faster-whisper · small · int8_"]
        C --> D["✨ Normalize Transcripts
        _Gemini API_
        _(fix Hinglish, garbled text)_"]
        D --> E["🔢 Chunk & Embed Transcripts
        _intfloat/multilingual-e5-small_
        _(passage: prefix)_"]
        E --> F[("🗄️ FAISS Index
        transcription_vector_store.faiss")]
    end

    subgraph SCRIPT ["📄 Script Processing"]
        SP["🔢 Chunk & Embed Script Lines
        _intfloat/multilingual-e5-small_
        _(query: prefix)_"]
        SP --> SQ[("🗄️ FAISS Index
        Script_query_store.faiss")]
    end

    subgraph SEARCH ["🔍 Search Engine"]
        F --> SE["Cosine Similarity Search
        _FAISS · IndexFlatIP · Top-3_"]
        SQ --> SE
        SE --> LM[("📋 line_mapping.json
        script line → best transcript match")]
    end

    subgraph RENAME ["🏷️ Rename Stage"]
        LM --> SO["Sort by Script Order
        _Sort.py_"]
        SO --> SF[("📋 sorted_file_sequence.json
        transcript file → index")]
        SF --> RN["Find & Rename Video Files
        _Renaming.py_"]
    end

    RN --> OUT(["`**Output**
    Renamed Video Clips
    _1.MOV, 2.MOV, 3.MOV…_`"])
