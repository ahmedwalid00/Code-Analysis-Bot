from langchain.chains.base import Chain
from langchain_core.vectorstores import VectorStoreRetriever # Use core import
from langchain.memory import ConversationSummaryBufferMemory
from typing import Dict, List, Any
import os

# Import the LCEL chains defined in CustomChainProperties
from .CustomChainProperties import initial_chain, refine_chain_step

class CodeAnalysisChain(Chain):
    memory: ConversationSummaryBufferMemory
    # No longer need refine_qa_chain attribute
    # refine_qa_chain: Chain
    retriever: VectorStoreRetriever
    initial_chain: Any # Type hint for the initial LCEL chain
    refine_chain_step: Any # Type hint for the refine step LCEL chain

    input_key: str = "question"
    output_key: str = "answer"

    @property
    def input_keys(self) -> List[str]:
        return [self.input_key]

    @property
    def output_keys(self) -> List[str]:
        return [self.output_key]

    def _call(self, inputs: dict[str, Any]) -> Dict[str, Any]:
        question = inputs[self.input_key]
        memory_variables = self.memory.load_memory_variables(inputs)
        chat_history = memory_variables.get("chat_history", "") # Get history string

        retrieved_docs = self.retriever.invoke(question)

        if not retrieved_docs:
            print("Warning: No relevant code snippets found.")
            # Handle no documents found - Option 1: Return specific message
            no_context_answer = "I couldn't find any relevant code snippets in the provided documents to answer your question based on the current context."
            # Save only the input question to memory if desired, or skip saving
            # self.memory.save_context(inputs, {self.output_key: no_context_answer})
            return {self.output_key: no_context_answer}
            # Option 2: Proceed with only history (might hallucinate) - not shown here

        # --- LCEL Refine Loop ---
        current_answer = ""

        # 1. Initial Step with the first document
        initial_inputs = {
            "question": question,
            "chat_history": chat_history,
            "context": retrieved_docs[0] # Pass the first Document object
        }
        current_answer = self.initial_chain.invoke(initial_inputs)

        # 2. Refine Steps with remaining documents
        for i, doc in enumerate(retrieved_docs[1:]):
            refine_inputs = {
                "question": question,
                "chat_history": chat_history,
                "existing_answer": current_answer, # Pass the answer from the previous step
                "context": doc # Pass the current Document object
            }
            current_answer = self.refine_chain_step.invoke(refine_inputs)


        # --- End LCEL Refine Loop ---

        final_answer = current_answer # The final answer after all steps

        # Save context to memory
        self.memory.save_context(inputs, {self.output_key: final_answer})

        return {self.output_key: final_answer}