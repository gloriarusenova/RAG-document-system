from abc import ABC, abstractmethod
from typing import Optional, List
from pydantic import BaseModel


class EvaluationResult(BaseModel):
    question: str
    response: str
    expected_answer: str
    is_correct: bool
    reasoning: Optional[str] = None
    
    # --- NEW OPTIONAL FIELDS FOR METRICS (backward compatible) ---
    retrieved_doc_ids: Optional[List[str]] = None
    relevant_doc_ids: Optional[List[str]] = None
    precision: Optional[float] = None
    recall: Optional[float] = None
    mrr: Optional[float] = None


class BaseEvaluator(ABC):
    """Base interface for the evaluation component."""

    @abstractmethod
    def evaluate(
        self, query: str, response: str, expected_answer: str
    ) -> EvaluationResult:
        pass
