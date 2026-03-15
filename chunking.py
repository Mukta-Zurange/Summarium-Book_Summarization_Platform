def smart_chunk_text(
    text,
    tokenizer,
    target_chunks=5,
    min_chunk_tokens=500,
    max_chunk_tokens=900,
    overlap_ratio=0.1
):
    input_ids = tokenizer.encode(text)
    total_tokens = len(input_ids)

    approx_chunk_size = total_tokens // target_chunks
    chunk_size = max(min_chunk_tokens, min(approx_chunk_size, max_chunk_tokens))

    overlap = int(chunk_size * overlap_ratio)
    step = chunk_size - overlap

    chunks = []
    i = 0
    chunk_id = 1

    while i < total_tokens:
        chunk_ids = input_ids[i:i + chunk_size]
        chunk_text = tokenizer.decode(chunk_ids, skip_special_tokens=True)

        chunks.append({
            "chunk_id": chunk_id,
            "text": chunk_text
        })

        i += step
        chunk_id += 1

    return chunks