from langchain.chains.question_answering import load_qa_chain
from langchain.memory import ConversationSummaryBufferMemory
from langchain_core.prompts import PromptTemplate
from src.prompts import *
from langchain_community.chat_models.openai import ChatOpenAI
from langchain_core.runnables import RunnablePassthrough, RunnableLambda
from langchain_core.output_parsers import StrOutputParser



output_parser = StrOutputParser()
#Building the refine chain 
# document_content_prompt = PromptTemplate(
#     input_variables=["page_content"],
#     template="{page_content}"
# )

initial_prompt_template = PromptTemplate(template=initial_prompt,
                                          input_variables=['chat_history' , 'context' , 'question'])
refine_prompt_template = PromptTemplate(template=refine_prompt,
                                        input_variables=['chat_history' , 'context' , 'question', 'existing_answer'])

llm = ChatOpenAI(temperature=0.4)
# refine_chain = load_qa_chain(llm=llm , 
#                              chain_type='refine',
#                              question_prompt=initital_prompt_template,
#                              refine_prompt=refine_prompt_template,
#                              document_prompt=document_content_prompt,
#                              document_variable_name="context",
#                              initial_response_name="existing_answer",
#                              input_key="question",
#                              output_key="answer"
#                              )

initial_chain = (
    # Prepare context correctly - expects a Document object as input
    RunnablePassthrough.assign(
        context=lambda x: x['context'].page_content # Extract page_content from the Document
    )
    | initial_prompt_template
    | llm
    | output_parser
)

refine_chain_step = (
    RunnablePassthrough.assign(
         context=lambda x: x['context'].page_content # Extract page_content from the Document
    )
    | refine_prompt_template
    | llm
    | output_parser
)

#Making the chain's memory
memory = ConversationSummaryBufferMemory(
llm=llm, # LLM used for summarization
max_token_limit=1000, # Adjust based on your LLM's context window and desired history length
memory_key="chat_history",
input_key="question", # Matches the input key for our custom chain
output_key="answer", # Matches the output key for our custom chain
return_messages=False # Return history as a string
)


