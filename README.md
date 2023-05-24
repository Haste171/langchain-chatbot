<p align="center">
<br><br><br>
<a https://github.com/Haste171/langchain-chatbot/stargazers"><img src="https://cdn.discordapp.com/attachments/1095427515717267658/1102434550782632016/f.png" width="760px" length="400"></a>
<br><br><br>
</p>

<p align="center">
<b>Efficiently use Langchain for Complex Tasks</b>

Existing repo development is at a freeze while we develop a langchain chat bot website :)
</p>

<p align=center>
<a href="https://github.com/Haste171/langchain-chatbot/releases"><img src="https://badgen.net/github/release/Haste171/langchain-chatbot">
<a href="https://gitHub.com/Haste171/langchain-chatbot/graphs/commit-activity"><img src="https://img.shields.io/badge/Maintained%3F-yes-green.svg">
<a href="https://github.com/Haste171/langchain-chatbot/blob/master/LICENSE"><img src="https://img.shields.io/github/license/Haste171/langchain-chatbot">
<a href="http://makeapullrequest.com"><img src="https://img.shields.io/badge/PRs-welcome-brightgreen.svg?style=flat-square">

</a>

<!-- *The LangChain Chatbot is an AI chat interface for the open-source library LangChain. It provides conversational answers to questions about vector ingested documents.* -->
<!-- *Existing repo development is at a freeze while we develop a langchain chat bot website :)* -->

Maintained by Developers of [legalyze.ai](https://legalyze.ai)

# 🚀 Installation

## Pre-Setup
Prerequisites:
- [Python](https://www.python.org/downloads/)
- [Git](https://git-scm.com/downloads)
- [OpenAI API Key](https://platform.openai.com/)

## Setup
```
git clone https://github.com/Haste171/langchain-chatbot.git
```

*Recommended to use a virtual environment*
```
pip install -r requirements.txt
```

Reference [example.env](https://github.com/Haste171/langchain-chatbot/blob/main/example.env) to create credentials file
```python
OPENAI_API_KEY=
PINECONE_API_KEY=
PINECONE_ENVIRONMENT=
PINECONE_INDEX=
```

**Run Terminal Interface**
```
python chatbot.py
```

**Run Chat Interface**
```
streamlit run streamlit.py
```

## In-App Usage
<details>
  <summary>Click to expand</summary>

  ## Terminal

  For usage of the terminal interface place files in the docs folder to be ingested

  Once Files are ingested one can choose to ingest more files in future usage or just query the existing vector database

  ## Chat Interface

  For usage of the chat interface upload files directly to the `Browse Files` section

  ## All
  - Temperature:
  The amount of creativity/burstiness the AI will use when querying files
  - Sources:
  The amount of sources the AI will base it's answer off of and use for context


  
</details>


# 🔧 Key Features

- Conversational answers with chat history
- Compatibility for PDF documents (more soon)
- Local and external vector database compatibility 

Soon:
- Externally hosted user accessible chat interface 
- Compatibility with multiple files types (Llama Index)
- Compatibility with offline models (HuggingFace, Vicuna, Alpaca)

# 💻 Contributing

If you would like to contribute to the LangChain Chatbot, please follow these steps:

1. Fork the repository
2. Create a new branch for your feature or bug fix
3. Write tests for your changes
4. Implement your changes and ensure that all tests pass
5. Submit a pull request

# 📝 Credits

The LangChain Chatbot was developed by [Haste171](https://github.com/Haste171) with much inspiration from [Mayo](https://twitter.com/mayowaoshin) with the [GPT4 & LangChain Chatbot for large PDF docs](https://github.com/mayooear/gpt4-pdf-chatbot-langchain). This project is mainly a port to Python from the Mayo chatbot.

# 🔨 License

The LangChain Chatbot is released under the [MIT License](https://opensource.org/licenses/MIT).

# 💻 Terminal
![preview_1](https://user-images.githubusercontent.com/34923485/235280558-9e7ebe85-6cf3-45fb-b063-dd3b3705c5de.png)
![preview_2](https://user-images.githubusercontent.com/34923485/235280562-ab4685dc-fe5a-46b5-925d-4fe2670f2618.png)

# 💻 Interface
![fixed-prev](https://user-images.githubusercontent.com/34923485/235337390-1b9bf06a-2512-4e22-87c7-8559533eb9d3.png)
