from sentence_transformers import SentenceTransformer
import numpy as np
from typing import Optional
from ..core.exceptions import SummarizationError

class TextSummarizer:
    """Lightweight text summarization"""
    
    def __init__(self, model_name: str = 'all-MiniLM-L6-v2'):
        """
        Initialize summarizer with a compact model
        
        Args:
            model_name (str): Sentence transformer model
        """
        try:
            self.model = SentenceTransformer(model_name)
        except Exception as e:
            raise SummarizationError(f"Failed to load summarization model: {e}")
    
    def summarize(self, text: str, max_length: int = 150) -> Optional[str]:
        """
        Generate extractive summary
        
        Args:
            text (str): Input text
            max_length (int): Maximum summary length
        
        Returns:
            Summarized text
        """
        try:
            if not text:
                return None
            
            # Split text into sentences
            sentences = [s.strip() for s in text.split('.') if s.strip()]
            
            if len(sentences) <= 2:
                return text[:max_length]
            
            # Compute sentence embeddings
            embeddings = self.model.encode(sentences)
            
            # Compute centrality scores
            centroid = np.mean(embeddings, axis=0)
            scores = [np.linalg.norm(emb - centroid) for emb in embeddings]
            
            # Select top sentences
            top_indices = sorted(
                range(len(scores)), 
                key=lambda i: scores[i]
            )[:3]
            
            summary = '. '.join([sentences[i] for i in top_indices])
            return summary[:max_length]
        
        except Exception as e:
            raise SummarizationError(f"Summarization failed: {e}")