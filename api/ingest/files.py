from langchain.schema import Document
from langchain.embeddings.openai import OpenAIEmbeddings
from langchain.vectorstores import Qdrant

embeddings = OpenAIEmbeddings()

print('SOON!')

# vectorstore = Qdrant.from_documents(
#     docs,
#     embeddings,
#     location=":memory:",  # Local mode with in-memory storage only
#     collection_name="my_documents",
# )