from interface.base_evaluator import BaseEvaluator, EvaluationResult
from interface.base_datastore import BaseDatastore
from util.invoke_ai import invoke_ai
from util.extract_xml import extract_xml_tag
from util.metrics_calculator import MetricsCalculator
from typing import Optional, List

SYSTEM_PROMPT = """
You are a system that evaluates the correctness of a response to a question.
The question will be provided in <question>...</question> tags.
The response will be provided in <response>...</response> tags.
The expected answer will be provided in <expected_answer>...</expected_answer> tags.

The response doesn't have to exactly match all the words/context the expected answer. It just needs to be right about
the answer to the actual question itself.

Evaluate whether the response is correct or not, and return your reasoning in <reasoning>...</reasoning> tags.
Then return the result in <result>...</result> tags — either as 'true' or 'false'.
"""


class Evaluator(BaseEvaluator):
    def __init__(self, datastore: Optional[BaseDatastore] = None):
        """
        Initialize the evaluator with optional datastore for metrics calculation.
        
        Args:
            datastore: Optional datastore for calculating retrieval metrics.
                      If None, only basic evaluation is performed (backward compatible).
        """
        self.datastore = datastore

    def evaluate(
        self, query: str, response: str, expected_answer: str,
        relevant_doc_ids: Optional[List[str]] = None
    ) -> EvaluationResult:
        """
        Evaluate a response with optional retrieval metrics calculation.
        
        Args:
            query: The question being evaluated
            response: The generated response
            expected_answer: The expected answer
            relevant_doc_ids: Optional list of relevant document IDs for metrics calculation
            
        Returns:
            EvaluationResult with basic evaluation and optional metrics
        """
        # Perform the original evaluation (preserves backward compatibility)
        user_prompt = f"""
        <question>\n{query}\n</question>
        <response>\n{response}\n</response>
        <expected_answer>\n{expected_answer}\n</expected_answer>
        """

        response_content = invoke_ai(
            system_message=SYSTEM_PROMPT, user_message=user_prompt
        )

        reasoning = extract_xml_tag(response_content, "reasoning")
        result = extract_xml_tag(response_content, "result")
        print(response_content)

        if result is not None:
            is_correct = result.lower() == "true"
        else:
            is_correct = False
            reasoning = f"No result found: ({response_content})"

        # Create base result (preserves original functionality)
        result = EvaluationResult(
            question=query,
            response=response,
            expected_answer=expected_answer,
            is_correct=is_correct,
            reasoning=reasoning,
        )

        # Add metrics calculation if datastore and relevant_doc_ids are provided
        if self.datastore is not None and relevant_doc_ids is not None:
            try:
                # Get retrieved documents with IDs
                retrieved_docs_with_ids = self.datastore.search_with_ids(query, top_k=30)
                retrieved_ids = [doc_id for _, doc_id in retrieved_docs_with_ids]
                
                # Calculate metrics
                metrics = MetricsCalculator.calculate_retrieval_metrics(
                    retrieved_ids, relevant_doc_ids
                )
                
                # Add metrics to result
                result.retrieved_doc_ids = retrieved_ids
                result.relevant_doc_ids = relevant_doc_ids
                result.precision = metrics["precision"]
                result.recall = metrics["recall"]
                result.mrr = metrics["mrr"]
                
                print(f"📊 Retrieval Metrics - Precision: {metrics['precision']:.3f}, "
                      f"Recall: {metrics['recall']:.3f}, MRR: {metrics['mrr']:.3f}")
                      
            except Exception as e:
                print(f"⚠️  Warning: Could not calculate retrieval metrics: {e}")
                # Continue with basic evaluation only

        return result
