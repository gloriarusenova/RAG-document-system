from typing import List, Dict


class MetricsCalculator:
    """
    A modular utility for calculating retrieval metrics (Precision, Recall, MRR).
    This is a self-contained calculator that works with document IDs.
    """
    
    @staticmethod
    def _calculate_precision(retrieved_ids: List[str], relevant_ids: List[str]) -> float:
        """
        Calculate Precision: |retrieved ∩ relevant| / |retrieved|
        
        Args:
            retrieved_ids: List of document IDs returned by the retriever
            relevant_ids: List of relevant document IDs (ground truth)
            
        Returns:
            Precision score between 0.0 and 1.0
        """
        if not retrieved_ids:
            return 0.0
            
        relevant_set = set(relevant_ids)
        retrieved_set = set(retrieved_ids)
        
        intersection = len(retrieved_set.intersection(relevant_set))
        return intersection / len(retrieved_ids)
    
    @staticmethod
    def _calculate_recall(retrieved_ids: List[str], relevant_ids: List[str]) -> float:
        """
        Calculate Recall: |retrieved ∩ relevant| / |relevant|
        
        Args:
            retrieved_ids: List of document IDs returned by the retriever
            relevant_ids: List of relevant document IDs (ground truth)
            
        Returns:
            Recall score between 0.0 and 1.0
        """
        if not relevant_ids:
            return 0.0
            
        relevant_set = set(relevant_ids)
        retrieved_set = set(retrieved_ids)
        
        intersection = len(retrieved_set.intersection(relevant_set))
        return intersection / len(relevant_ids)
    
    @staticmethod
    def _calculate_mrr(retrieved_ids: List[str], relevant_ids: List[str]) -> float:
        """
        Calculate Mean Reciprocal Rank for a single query.
        
        Args:
            retrieved_ids: List of document IDs in retrieval order
            relevant_ids: List of relevant document IDs (ground truth)
            
        Returns:
            MRR score between 0.0 and 1.0
        """
        if not retrieved_ids or not relevant_ids:
            return 0.0
            
        relevant_set = set(relevant_ids)
        
        for rank, doc_id in enumerate(retrieved_ids):
            if doc_id in relevant_set:
                return 1.0 / (rank + 1)
        
        return 0.0
    
    @staticmethod
    def calculate_retrieval_metrics(retrieved_ids: List[str], 
                                  relevant_ids: List[str]) -> Dict[str, float]:
        """
        Calculate all retrieval metrics for a single query.
        
        Args:
            retrieved_ids: List of document IDs returned by the retriever (in order)
            relevant_ids: List of relevant document IDs (ground truth)
            
        Returns:
            Dictionary with precision, recall, and mrr scores
        """
        return {
            "precision": MetricsCalculator._calculate_precision(retrieved_ids, relevant_ids),
            "recall": MetricsCalculator._calculate_recall(retrieved_ids, relevant_ids),
            "mrr": MetricsCalculator._calculate_mrr(retrieved_ids, relevant_ids)
        }
