"""Integration with existing RAG pipeline."""
import sys
import os
from typing import Dict, List, Tuple
import statistics
from dotenv import load_dotenv

# Load environment variables from .env file
env_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), '.env')
if os.path.exists(env_path):
    load_dotenv(env_path)
    print(f"✅ Loaded environment variables from {env_path}")
else:
    print(f"⚠️  Warning: .env file not found at {env_path}")

# Add the parent and src directories to path
current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(current_dir)
src_dir = os.path.join(parent_dir, 'src')

for directory in [parent_dir, src_dir]:
    if directory not in sys.path:
        sys.path.insert(0, directory)

# Now we can import from src modules
from rag_pipeline import RAGPipeline
from impl import Datastore, Indexer, Retriever, ResponseGenerator


def create_pipeline() -> RAGPipeline:
    """Create and return a new RAG Pipeline instance."""
    datastore = Datastore()
    indexer = Indexer()
    retriever = Retriever(datastore=datastore)
    response_generator = ResponseGenerator()
    return RAGPipeline(datastore, indexer, retriever, response_generator, None)


class RetrievalScore:
    """Container for retrieval quality metrics."""
    
    def __init__(self, 
                 avg_score: float,
                 top_score: float, 
                 num_sources: int,
                 score_variance: float,
                 sources: List[str],
                 sources_with_scores: List[Tuple[str, float]]):
        self.avg_score = avg_score
        self.top_score = top_score
        self.num_sources = num_sources
        self.score_variance = score_variance
        self.sources = sources
        self.sources_with_scores = sources_with_scores
        
    @property
    def quality_score(self) -> float:
        """
        Calculate an overall quality score (0-100).
        
        Combines:
        - Average similarity score (weighted 60%)
        - Consistency (low variance is good) (weighted 20%)
        - Number of high-quality sources (weighted 20%)
        """
        # Normalize average score to 0-100
        avg_component = self.avg_score * 60
        
        # Consistency component (lower variance is better)
        # Normalize variance to 0-1, then invert it
        consistency = max(0, 1 - (self.score_variance / 0.1)) * 20
        
        # Source count component (having 3+ good sources is ideal)
        source_component = min(self.num_sources / 5.0, 1.0) * 20
        
        return round(avg_component + consistency + source_component, 1)
    
    @property
    def grade(self) -> str:
        """Get letter grade for the retrieval quality."""
        score = self.quality_score
        if score >= 90:
            return "A+"
        elif score >= 85:
            return "A"
        elif score >= 80:
            return "A-"
        elif score >= 75:
            return "B+"
        elif score >= 70:
            return "B"
        elif score >= 65:
            return "B-"
        elif score >= 60:
            return "C+"
        elif score >= 55:
            return "C"
        else:
            return "C-"


class RAGService:
    """Wrapper for the existing RAG pipeline with scoring."""
    
    def __init__(self):
        self.pipeline = create_pipeline()
    
    def query_with_scores(self, question: str) -> Dict:
        """
        Query the RAG pipeline and return response with quality scores.
        
        Returns:
            {
                "answer": str,
                "retrieval_score": RetrievalScore,
            }
        """
        # Get raw search results with scores
        search_results_with_scores = self._search_with_scores(question)
        
        # Extract just the content for response generation
        search_results = [content for content, _ in search_results_with_scores]
        
        # Generate response using existing pipeline
        answer = self.pipeline.response_generator.generate_response(
            question, 
            search_results
        )
        
        # Calculate retrieval quality score
        retrieval_score = self._calculate_retrieval_score(search_results_with_scores)
        
        return {
            "answer": answer,
            "retrieval_score": retrieval_score,
        }
    
    def _search_with_scores(self, query: str, top_k: int = 10) -> List[Tuple[str, float]]:
        """
        Search and return results with similarity scores.
        
        Returns:
            List of (content, similarity_score) tuples
        """
        # Get initial search results from datastore with more results for reranking
        vector = self.pipeline.datastore.get_vector(query)
        results = (
            self.pipeline.datastore.table.search(vector)
            .select(["content", "_distance"])
            .limit(top_k * 3)
            .to_list()
        )
        
        # Convert distance to similarity score (closer = higher score)
        # LanceDB uses L2 distance, so we invert it
        results_with_scores = []
        for result in results:
            content = result.get("content")
            distance = result.get("_distance", 0)
            # Convert L2 distance to similarity (0-1 scale)
            # Using exponential decay: e^(-distance)
            import math
            similarity = math.exp(-distance)
            results_with_scores.append((content, similarity))
        
        # Get reranked results (just content)
        search_results = [content for content, _ in results_with_scores]
        reranked_results = self.pipeline.retriever._rerank(query, search_results, top_k=top_k)
        
        # Match reranked results back to their scores
        reranked_with_scores = []
        for reranked_content in reranked_results:
            # Find the matching score from original results
            for content, score in results_with_scores:
                if content == reranked_content:
                    reranked_with_scores.append((content, score))
                    break
        
        return reranked_with_scores
    
    def _calculate_retrieval_score(self, 
                                   results_with_scores: List[Tuple[str, float]]) -> RetrievalScore:
        """Calculate retrieval quality metrics from scored results."""
        if not results_with_scores:
            return RetrievalScore(0.0, 0.0, 0, 0.0, [], [])
        
        scores = [score for _, score in results_with_scores]
        sources = [content for content, _ in results_with_scores]
        
        avg_score = statistics.mean(scores)
        top_score = max(scores)
        num_sources = len(sources)
        score_variance = statistics.variance(scores) if len(scores) > 1 else 0.0
        
        return RetrievalScore(
            avg_score=avg_score,
            top_score=top_score,
            num_sources=num_sources,
            score_variance=score_variance,
            sources=sources,
            sources_with_scores=results_with_scores
        )
    
    def get_document_count(self) -> int:
        """Get number of indexed chunks."""
        try:
            return self.pipeline.datastore.table.count_rows()
        except Exception as e:
            print(f"Error getting document count: {e}")
            return 0


# Global singleton instance
_rag_service = None

def get_rag_service() -> RAGService:
    """Get or create the global RAG service instance."""
    global _rag_service
    if _rag_service is None:
        _rag_service = RAGService()
    return _rag_service

