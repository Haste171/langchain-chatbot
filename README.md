<p align="center">
<br><br><br>
<a https://github.com/Haste171/langchain-chatbot/stargazers"><img src="https://github.com/Haste171/langchain-chatbot/assets/34923485/9bc2b4a3-f19e-4ca0-9a4b-f6db4715ae38" width="760px" length="400"></a>
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
Join the [Discord](https://discord.gg/8vzXR9MGyc) server for help

## Dev-Setup
Prerequisites:
- [Git](https://git-scm.com/downloads) - Free
- [Pinecone Database](https://youtu.be/tp0bQNDtLPc?t=48) - Free
- [OpenAI API Key](https://platform.openai.com/account/api-keys) - Billing Required

### Setup
```
git clone https://github.com/Haste171/langchain-chatbot.git
```

Reference [example.env](https://github.com/Haste171/langchain-chatbot/blob/main/example.env) to create `.env` file
```python
OPENAI_API_KEY=
PINECONE_API_KEY=
PINECONE_ENV=
PINECONE_INDEX=
```

### Install Requirements

```python
poetry install
```

### Activate Environment
```python
poetry shell
```

### Run Startup
```python
python3 startup.py
```


# 🔧 Key Features

✅ Interactive Ingestion UI for files 

✅ Chat UI with source, temperature, vector_k, and other parameter changing abilities

✅ More features coming very soon


Soon:
- Compatibility with many more files types 
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

# 💻 Interface
![fixed-prev](https://cdn.discordapp.com/attachments/1114412425115086888/1216256420253794325/Screenshot_2024-03-09_at_11.28.25_PM.png?ex=65ffba0f&is=65ed450f&hm=c089e312073c773c886576187322799ba9007421cb8def40e05213805f61e338&)
![fixed-prev](https://cdn.discordapp.com/attachments/1114412425115086888/1216256419989422110/Screenshot_2024-03-09_at_11.28.37_PM.png?ex=65ffba0f&is=65ed450f&hm=c097a636e2ceef752620e7554880174d6ba81c1281fb15df8b6d1b6c1dd22916&)

Maintained by Developers of [legalyze.ai](https://legalyze.ai)
