# Function to rephrase a follow up question
def rephrase_question(chat_history, question):
    """
    Given the following conversation and a follow up question, rephrase the follow up question to be a standalone question.
    :param chat_history: str, the conversation history
    :param question: str, the follow up question
    :return: str, the standalone question
    """
    CONDENSE_PROMPT = """Given the following conversation and a follow up question, rephrase the follow up question to be a standalone question.
    
    Chat History:
    {chat_history}
    Follow Up Input: {question}
    Standalone question:"""
    
    # check if the follow up question is a continuation of a previous question
    if question.startswith("What do you mean by"):
        # extract the previous question
        temp = question.split(" ")
        prev_question = " ".join(temp[5:])
        
        # rephrase the previous question to be standalone
        standalone_question = f"What does \"{prev_question}\" mean?"
    else:
        # add a generic "What do you mean?" to the follow up question to make it standalone
        standalone_question = f"What do you mean by \"{question}\"?"
        
    # insert the conversation history and standalone question into the prompt and return
    return CONDENSE_PROMPT.format(chat_history=chat_history, question=standalone_question)