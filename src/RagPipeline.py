from src.RagOperations import loadig_data , splitting_data_to_chunks , get_retriever
# Import the memory and the NEW LCEL chains
from src.CustomChainProperties import memory , initial_chain, refine_chain_step
from src.CustomChain import CodeAnalysisChain

#getting final chain to the conversation
def final_chain(file_path):

    #loadig data
    data = loadig_data(file_path=file_path)

    #splitting data
    chunks = splitting_data_to_chunks(docs=data)

    #getting retriever
    retriever = get_retriever(chunks=chunks)

    # Instantiate the custom chain, passing the LCEL chains
    chat_bot_chain = CodeAnalysisChain(
        memory=memory,
        retriever=retriever,
        initial_chain=initial_chain,       # Pass the initial chain
        refine_chain_step=refine_chain_step # Pass the refine step chain
        # remove refine_qa_chain=refine_chain
    )

    return chat_bot_chain