<p align="center">
<br><br><br>
<a https://github.com/Haste171/langchain-chatbot/stargazers"><img src="https://cdn.discordapp.com/attachments/1095427515717267658/1102434550782632016/f.png" width="760px" length="400"></a>
<br><br><br>
</p>

<p align="center">
<b>Efficiently use Langchain for Complex Tasks</b>
</p>

<p align=center>
<a href="https://github.com/Haste171/langchain-chatbot/releases"><img src="https://badgen.net/github/release/Haste171/langchain-chatbot">
<a href="https://gitHub.com/Haste171/langchain-chatbot/graphs/commit-activity"><img src="https://img.shields.io/badge/Maintained%3F-yes-green.svg">
<a href="https://github.com/Haste171/langchain-chatbot/blob/master/LICENSE"><img src="https://img.shields.io/github/license/Haste171/langchain-chatbot">
<a href="https://discord.gg/KgmN4FPxxT"><img src="https://dcbadge.vercel.app/api/server/KgmN4FPxxT?compact=true&style=flat"></a>

</a>

<!-- *The LangChain Chatbot is an AI chat interface for the open-source library LangChain. It provides conversational answers to questions about vector ingested documents.* -->
<!-- *Existing repo development is at a freeze while we develop a langchain chat bot website :)* -->


# 🚀 Installation

## User-Setup
You can either join the [Discord](https://discord.gg/8vzXR9MGyc) server to use the bot or invite the [Langchain Chatbot](https://discord.com/api/oauth2/authorize?client_id=1113492778899476533&permissions=8&scope=bot) to your own server.

*If not you can following to steps below to setup your own Langchain Chatbot*

## Dev-Setup
Prerequisites:
- [Git](https://git-scm.com/downloads) - Free
- [Docker](https://www.docker.com/products/docker-desktop/) - Free
- [Discord Bot](https://discord.com/developers/applications) - Free
- [Mongo Database](https://youtu.be/dnEfQhjZgw0?t=326) - Free
- [Pinecone Database](https://youtu.be/tp0bQNDtLPc?t=48) - Free
- [OpenAI API Key](https://platform.openai.com/account/api-keys) - Billing Required

### Setup
```
git clone https://github.com/Haste171/langchain-chatbot.git
cd langchain-chatbot
pip install -r requirements.txt
```
### Run the FastAPI Application
Ensure you have installed FastAPI and Uvicorn, then run the following commands:
```
uvicorn app.main:app --reload
```
This will start the FastAPI server, making the Langchain Chatbot API available at `http://localhost:8000` where you can send request to the endpoints specified.

Reference [example.env](https://github.com/Haste171/langchain-chatbot/blob/main/example.env) to create `.env` file
```python
BOT_TOKEN=
MONGO_URI=
PINECONE_API_KEY=
PINECONE_INDEX=
PINECONE_ENV=
```

*Recommended to use a Docker Container for Deployment*
```
docker build -t langchain-chatbot .
docker run -d langchain-chatbot
```

# 

✅ FastAPI based Web API Integration
✅ Ingest and Query through RESTful Endpoints🔧 Key Features

✅ Credential Manager (OpenAI Keys)

✅ Space Manager (Ingestions)

✅ Documentation Ingester (For readthedocs.io sites)


Soon:
- Compatibility with multiple files types (Llama Index)
- Compatibility with offline models (HuggingFace, Vicuna, Alpaca)
- Re-adding PDF Ingester Will be implemented along with docx, doc, excel, etc.

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

# 💻 Interface
![fixed-prev](https://cdn.discordapp.com/attachments/1114412425115086888/1114420571833376768/image.png)
![fixed-prev](https://cdn.discordapp.com/attachments/1114412425115086888/1114421482429354065/image.png)

Maintained by Developers of [legalyze.ai](https://legalyze.ai)

# 📄 API Usage
Here's how you can interact with the API:

### Ingest Data
Send a POST request to `/ingest` to ingest data:
```python
import requests
response = requests.post('http://localhost:8000/ingest')
print(response.json())
```
Expect a confirmation response that the data has been ingested.

### Query Data
Send a GET request to `/query/{question}` with your question:
```python
import requests
question = 'What is the answer to my question?'
response = requests.get(f'http://localhost:8000/query/{question}')
print(response.json())
```

### Chat History
Retrieve the chat history by sending a GET request to `/chat_history`:
```python
import requests
response = requests.get('http://localhost:8000/chat_history')
print(response.json())
```

These endpoints will allow you to ingest, query, and view the history of interactions with the Langchain Chatbot API.