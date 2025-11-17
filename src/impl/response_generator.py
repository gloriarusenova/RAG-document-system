from typing import List
from interface.base_response_generator import BaseResponseGenerator
from util.invoke_ai import invoke_ai
from util.extract_xml import extract_xml_tag


# --- NEW, ADVANCED SYSTEM PROMPT WITH CHAIN-OF-THOUGHT ---
ADVANCED_SYSTEM_PROMPT = """
You are a highly intelligent and meticulous AI assistant. Your task is to answer the user's question based ONLY on the provided context.

Follow these steps carefully:
1. **Chain of Thought:** First, write a step-by-step reasoning of how you will answer the question based on the provided context. Analyze the context and the question. Explain which parts of the context are relevant and how they combine to form the answer. Use the <reasoning> XML tag for this part.
2. **Final Answer:** After your reasoning, provide the final, concise answer to the user's question. Use the <result> XML tag for this part.

If the context does not contain the information needed to answer the question, state that clearly in your reasoning and in the final answer. Do not make up information.

Context:
{context}
"""


class ResponseGenerator(BaseResponseGenerator):
    def generate_response(self, query: str, context: List[str]) -> str:
        """Generate a response using OpenAI's chat completion with Chain-of-Thought reasoning."""
        # Join the context chunks into a single string with separators
        context_str = "\n---\n".join(context)
        
        # Use the new advanced prompt with context formatting
        system_prompt = ADVANCED_SYSTEM_PROMPT.format(context=context_str)
        
        # Get the full response with reasoning
        response_content = invoke_ai(
            system_message=system_prompt,
            user_message=query
        )

        # Extract only the final answer from the XML response
        final_answer = extract_xml_tag(response_content, "result")

        if final_answer is None:
            # Fallback if the model doesn't follow instructions
            print("⚠️  Warning: Model didn't follow XML format, using full response")
            return response_content.strip()
            
        return final_answer.strip()
