import os
import json
from utils.ingest import ingest
from utils.query import query

from dotenv import load_dotenv
load_dotenv()

from colorama import init, Fore, Style
init()

openai_api_key = os.environ.get('OPENAI_API_KEY')
pinecone_api_key = os.environ.get('PINECONE_API_KEY')
pinecone_environment = os.environ.get('PINECONE_ENVIRONMENT')
pinecone_index = os.environ.get('PINECONE_INDEX')
pinecone_namespace ='testing-pdf-0001'

startup = f"""{Fore.WHITE}Using the following credentials:{Fore.WHITE}
OpenAI API Key: {Fore.RED}{openai_api_key}{Fore.WHITE}
Pinecone API Key: {Fore.BLUE}{pinecone_api_key}{Fore.WHITE}
Pinecone Environment: {Fore.BLUE}{pinecone_environment}{Fore.WHITE}
Pinecone Index: {Fore.BLUE}{pinecone_index}{Fore.WHITE}
Pinecone Namespace: {Fore.GREEN}{pinecone_namespace}{Fore.WHITE}
"""

demo = f"""{Fore.WHITE}Using the following credentials:{Fore.WHITE}
OpenAI API Key: {Fore.RED}...{Fore.WHITE}
Pinecone API Key: {Fore.BLUE}...{Fore.WHITE}
Pinecone Environment: {Fore.BLUE}...{Fore.WHITE}
Pinecone Index: {Fore.BLUE}...{Fore.WHITE}
Pinecone Namespace: {Fore.GREEN}...{Fore.WHITE}
"""
print(demo)

r = input('Do you want to ingest? (Y/N): ')

os.system('cls')
if r == 'Y':
    ingest_response = ingest(openai_api_key=openai_api_key, pinecone_api_key=pinecone_api_key, pinecone_environment=pinecone_environment, pinecone_index=pinecone_index, pinecone_namespace=pinecone_namespace)
    print(ingest_response)
elif r == 'N':
    print('Using already ingested namespace.')
else: 
    print('No method given, passing')
    pass

process = query(openai_api_key=openai_api_key, pinecone_api_key=pinecone_api_key, pinecone_environment=pinecone_environment, pinecone_index=pinecone_index, pinecone_namespace=pinecone_namespace)

def chat_loop():
    chat_history = []
    while True:
        query = input("Please enter your question (or type 'exit' to end): ")
        if query.lower() == 'exit':
            break
        result = process({"question": query, "chat_history": chat_history})
        response_dict = {
            'answer': result["answer"],
            'sources': result['source_documents']
        }
        print(f'{Fore.BLUE}{Style.BRIGHT}AI:{Fore.RESET}{Style.NORMAL} {result["answer"]}')
        chat_history.append((query, result["answer"]))

        # Write chat history to a JSON file
        with open('chat_history.json', 'w') as json_file:
            json.dump(chat_history, json_file, ensure_ascii=False, indent=4)
chat_loop()