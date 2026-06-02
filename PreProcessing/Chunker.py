def chunker(text, context_words=10):
    import re

    # Split on: English (.!?) + Hindi dandas (।॥) + newlines (from whisper segments)
    sentences = re.split(r'[.!?।॥\n]+', text)

    sentences = [
        sentence.strip()
        for sentence in sentences
        if sentence.strip()
    ]

    chunks = []
    for i, sentence in enumerate(sentences):

        prev_context = ""
        next_context = ""

        if i > 0:
            prev_words = sentences[i - 1].split()
            prev_context = " ".join(prev_words[-context_words:])

        if i < len(sentences) - 1:
            next_words = sentences[i + 1].split()
            next_context = " ".join(next_words[:context_words])

        chunk = f"{prev_context} {sentence} {next_context}".strip()
        chunks.append(chunk)

    return chunks