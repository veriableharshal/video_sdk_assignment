from typing import List

def chunk_by_word_count(
    text: str,
    chunk_size: int = 200,
    overlap: int = 50
) -> List[str]:
    try:
        if chunk_size <= 0:
            raise ValueError("Chunk size must be positive")
            
        if overlap >= chunk_size:
            raise ValueError("Overlap must be less than chunk size")
        
        words = text.split()
        chunks = []
        
        for i in range(0, len(words), chunk_size - overlap):
            chunk_words = words[i:i + chunk_size]
            
            if chunk_words:  
                chunk_text = ' '.join(chunk_words)
                chunks.append(chunk_text)
            
           
            if i + chunk_size >= len(words):
                break
                
        return chunks
        
    except Exception as e:
        raise RuntimeError(f"Word-based chunking failed: {e}")