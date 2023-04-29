# LangChain Chatbot

The LangChain Chatbot is an AI assistant for the open-source library LangChain. It provides conversational answers to questions about the ingested documents.

## Key Features

- Conversational answers with chat history
- Compatibility for PDF documents (more soon)

## Usage

To use the LangChain Chatbot, follow these steps:

Prequisties:
- Bare Minimum Coding Experience in Python
- Pinecone Account with a Pinecone Index Created
- OpenAI Account with an OpenAI API KEY (Billing Setup)

Steps:
1. Clone the repository
2. Install the required dependencies using `pip install -r requirements.txt`
3. Set the required environment variables for the OpenAI and Pinecone APIs
4. Place documents you want to chat with in the 'docs' folder (There is already one there for example)
5. Run the chatbot using `python chatbot.py`

*It is highly recommended to use a virtual environment for using this project*

*By default there will be a preset namespace in `chatbot.py` on line `16` that you may want to change based on the documents ingested*

## Contributing

If you would like to contribute to the LangChain Chatbot, please follow these steps:

1. Fork the repository
2. Create a new branch for your feature or bug fix
3. Write tests for your changes
4. Implement your changes and ensure that all tests pass
5. Submit a pull request

## Credits

The LangChain Chatbot was developed by [Haste171](https://github.com/Haste171) with much inspiration from [Mayo](https://twitter.com/mayowaoshin) with the [GPT4 & LangChain Chatbot for large PDF docs](https://github.com/mayooear/gpt4-pdf-chatbot-langchain). This project is mainly a port to Python from the Mayo chatbot.

## License

The LangChain Chatbot is released under the [MIT License](https://opensource.org/licenses/MIT).

## Preview
![preview_1](https://user-images.githubusercontent.com/34923485/235280558-9e7ebe85-6cf3-45fb-b063-dd3b3705c5de.png)
![preview_2](https://user-images.githubusercontent.com/34923485/235280562-ab4685dc-fe5a-46b5-925d-4fe2670f2618.png)

