# Adding commentaries to each function

# Given content
QA_PROMPT = """You are a helpful AI assistant. Use the following pieces of context to answer the question at the end.
If you don't know the answer, just say you don't know. DO NOT try to make up an answer.
If the question is not related to the context, politely respond that you are tuned to only answer questions that are related to the context.
Use as much detail when as possible when responding.

{context}

Question: {question}
Helpful answer in markdown format:"""

# Main function
def ai_assistant(context, question):
    """This is the main function that takes in context and question and returns a response"""

    # Checking if the question is related to the context
    if context in question:
        # Splitting the question into words
        words = question.split()

        # Checking if the question is a "what" question
        if words[0].lower() == "what":
            # If the question is a "what" question, return the context
            response = f"The {words[-1]} is {context}"
        else:
            # If the question is not a "what" question, return a statement
            response = "I'm sorry, I cannot answer that question"

    else:
        # If the question is not related to the context, ask for a related question
        response = "I'm sorry, please ask a question related to the given context"

    return response

# Testing the function
context = "The capital of France is Paris"
question = "What is the capital of France?"
print(QA_PROMPT.format(context=context, question=question))
print(ai_assistant(context, question))