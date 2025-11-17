"""State management for RAG evaluation interface."""
import reflex as rx
from typing import List, Optional
import json
import random
from pathlib import Path

from .models import ChatMessage, ChatSession
from .rag_service import get_rag_service


class TestQuestion(rx.Base):
    """Test question from sample data."""
    question: str
    expected_answer: str
    relevant_doc_ids: List[str] = []


class RetrievedChunk(rx.Base):
    """A retrieved chunk with relevance status."""
    content: str
    source_id: str
    is_relevant: bool
    rank: int


class EvaluationResult(rx.Base):
    """Evaluation result with metrics."""
    question: str
    generated_answer: str
    expected_answer: str
    is_correct: bool
    reasoning: str
    precision: float = 0.0
    recall: float = 0.0
    mrr: float = 0.0
    retrieved_count: int = 0
    relevant_count: int = 0
    retrieved_chunks: List[RetrievedChunk] = []


class EvalState(rx.State):
    """State for evaluation dashboard."""
    
    @staticmethod
    def clean_answer(answer: str) -> str:
        """Remove reasoning tags and other XML-style tags from answer."""
        import re
        # Remove <reasoning>...</reasoning> tags and content
        answer = re.sub(r'<reasoning>.*?</reasoning>', '', answer, flags=re.DOTALL)
        # Remove <result>...</result> tags but keep content
        answer = re.sub(r'<result>(.*?)</result>', r'\1', answer, flags=re.DOTALL)
        # Remove any other XML-style tags
        answer = re.sub(r'<[^>]+>', '', answer)
        # Clean up extra whitespace
        answer = ' '.join(answer.split())
        return answer.strip()
    
    # All test questions
    all_questions: List[TestQuestion] = []
    
    # Random suggestions
    suggested_questions: List[TestQuestion] = []
    
    # Selected question
    selected_question: str = ""
    selected_test_data: Optional[TestQuestion] = None
    
    # Free text input
    custom_question_input: str = ""
    
    # Evaluation result
    current_result: Optional[EvaluationResult] = None
    
    # Loading state
    is_evaluating: bool = False
    
    # Error handling
    error_message: str = ""
    
    # Document count
    doc_count: int = 0
    
    # Chunk retrieval settings
    top_k: int = 30  # Number of chunks to retrieve
    
    # UI state for chunk expansion
    expanded_chunks: dict[int, bool] = {}
    
    @rx.var
    def question_options(self) -> List[str]:
        """Get list of question strings for dropdown."""
        return [q.question for q in self.all_questions]
    
    def on_load(self):
        """Load test questions and initialize."""
        self._load_test_questions()
        self._load_random_suggestions()
        
        # Ensure input field starts empty
        self.custom_question_input = ""
        self.selected_question = ""
        self.current_result = None
        
        # Get document count
        try:
            rag_service = get_rag_service()
            self.doc_count = rag_service.get_document_count()
        except Exception as e:
            print(f"Error loading document count: {e}")
            self.doc_count = 0
    
    def set_top_k(self, value: int):
        """Update the number of chunks to retrieve."""
        self.top_k = max(5, min(50, value))  # Clamp between 5 and 50
    
    def toggle_chunk_expansion(self, chunk_rank: int):
        """Toggle expansion state for a specific chunk."""
        current_state = self.expanded_chunks.get(chunk_rank, False)
        self.expanded_chunks[chunk_rank] = not current_state
    
    def _load_test_questions(self):
        """Load all test questions from JSON file."""
        try:
            questions_path = Path(__file__).parent.parent / "sample_data" / "eval" / "sample_questions.json"
            with open(questions_path, 'r') as f:
                data = json.load(f)
            
            self.all_questions = [
                TestQuestion(
                    question=item["question"],
                    expected_answer=item["answer"],
                    relevant_doc_ids=item.get("relevant_doc_ids", [])
                )
                for item in data
            ]
            print(f"✅ Loaded {len(self.all_questions)} test questions")
        except Exception as e:
            print(f"Error loading test questions: {e}")
            self.error_message = f"Failed to load test questions: {str(e)}"
    
    def _load_random_suggestions(self):
        """Load 3 random suggestions."""
        if len(self.all_questions) >= 3:
            self.suggested_questions = random.sample(self.all_questions, 3)
        else:
            self.suggested_questions = self.all_questions.copy()
    
    def refresh_suggestions(self):
        """Get new random suggestions."""
        self._load_random_suggestions()
    
    def set_custom_question(self, value: str):
        """Update the custom question input."""
        self.custom_question_input = value
        if value.strip():
            self.selected_question = value.strip()
            # For custom questions, we won't have test data
            self.selected_test_data = None
    
    def select_question(self, question_text: str):
        """Select a question from dropdown or suggestions."""
        print(f"🔍 select_question called with: {question_text[:50]}...")
        self.selected_question = question_text
        self.custom_question_input = question_text  # Sync with input field
        
        # Find the test data for this question
        found = False
        for q in self.all_questions:
            if q.question == question_text:
                self.selected_test_data = q
                found = True
                print(f"✅ Found matching test data")
                break
        
        if not found:
            print(f"⚠️ No matching test data found for: {question_text[:50]}...")
            self.selected_test_data = None
        
        # Clear previous result
        self.current_result = None
        self.error_message = ""
    
    def submit_custom_question(self):
        """Submit the custom question from text input."""
        if self.custom_question_input.strip():
            question = self.custom_question_input.strip()
            self.selected_question = question
            
            # Find the test data for this question
            for q in self.all_questions:
                if q.question == question:
                    self.selected_test_data = q
                    break
            else:
                # If not found in test data, still allow custom questions
                self.selected_test_data = TestQuestion(
                    question=question,
                    expected_answer="",
                    relevant_doc_ids=[]
                )
            
            # Create a placeholder result immediately to show the question
            self.current_result = EvaluationResult(
                question=question,
                generated_answer="",  # Empty, will be replaced
                expected_answer="",
                is_correct=False,
                reasoning="",
            )
            
            # Set loading state
            self.is_evaluating = True
            
            # Clear error
            self.error_message = ""
            
            # Yield to update UI before starting evaluation
            yield
            
            # Trigger evaluation
            self.evaluate_selected_question()
    
    def handle_dropdown_select(self, question_text: str):
        """Handle dropdown selection - just populate the input field."""
        if question_text:
            self.custom_question_input = question_text
            self.selected_question = question_text
            # Find the test data for this question
            for q in self.all_questions:
                if q.question == question_text:
                    self.selected_test_data = q
                    break
    
    def evaluate_selected_question(self):
        """Evaluate the selected question."""
        print(f"🎯 evaluate_selected_question called")
        print(f"   selected_question: {self.selected_question[:50] if self.selected_question else 'EMPTY'}...")
        print(f"   selected_test_data: {self.selected_test_data is not None}")
        
        if not self.selected_test_data:
            self.error_message = "No question selected. Please click a question first."
            print(f"❌ No selected_test_data")
            return
        
        self.is_evaluating = True
        self.error_message = ""
        self.expanded_chunks = {}  # Reset expansion state
        
        try:
            # Import evaluator here to avoid circular imports
            from src.impl import Evaluator
            
            # Get RAG service
            rag_service = get_rag_service()
            
            # Get answer from RAG system
            search_results = rag_service.pipeline.retriever.search(self.selected_test_data.question)
            generated_answer = rag_service.pipeline.response_generator.generate_response(
                self.selected_test_data.question,
                search_results
            )
            
            # Evaluate with metrics
            evaluator = Evaluator(datastore=rag_service.pipeline.datastore)
            eval_result = evaluator.evaluate(
                query=self.selected_test_data.question,
                response=generated_answer,
                expected_answer=self.selected_test_data.expected_answer,
                relevant_doc_ids=self.selected_test_data.relevant_doc_ids
            )
            
            # Get retrieved chunks with relevance status
            retrieved_chunks = []
            retrieved_ids = eval_result.retrieved_doc_ids or []
            relevant_ids_set = set(eval_result.relevant_doc_ids or [])
            
            # Get the actual content for each retrieved chunk
            retrieved_docs_with_ids = rag_service.pipeline.datastore.search_with_ids(
                self.selected_test_data.question, 
                top_k=self.top_k
            )
            
            for rank, (content, source_id) in enumerate(retrieved_docs_with_ids[:self.top_k], 1):
                retrieved_chunks.append(RetrievedChunk(
                    content=content,
                    source_id=source_id,
                    is_relevant=source_id in relevant_ids_set,
                    rank=rank
                ))
            
            # Create result object
            self.current_result = EvaluationResult(
                question=eval_result.question,
                generated_answer=self.clean_answer(eval_result.response),
                expected_answer=eval_result.expected_answer,
                is_correct=eval_result.is_correct,
                reasoning=eval_result.reasoning or "No reasoning provided",
                precision=eval_result.precision or 0.0,
                recall=eval_result.recall or 0.0,
                mrr=eval_result.mrr or 0.0,
                retrieved_count=len(eval_result.retrieved_doc_ids or []),
                relevant_count=len(eval_result.relevant_doc_ids or []),
                retrieved_chunks=retrieved_chunks
            )
            
            print(f"✅ Evaluation complete: {'✓ Correct' if eval_result.is_correct else '✗ Incorrect'}")
            
        except Exception as e:
            self.error_message = f"Evaluation error: {str(e)}"
            print(f"Error in evaluation: {e}")
            import traceback
            traceback.print_exc()
        
        finally:
            self.is_evaluating = False
    
    def clear_evaluation(self):
        """Clear current evaluation."""
        self.selected_question = ""
        self.selected_test_data = None
        self.current_result = None
        self.error_message = ""
        self.expanded_chunks = {}

