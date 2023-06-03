import asyncio, os, tempfile, aiohttp, pinecone
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.embeddings.openai import OpenAIEmbeddings
from langchain.vectorstores import Pinecone
from urllib.parse import urljoin
from bs4 import BeautifulSoup

pinecone_api_key = os.environ.get('PINECONE_API_KEY')
pinecone_env = os.environ.get('PINECONE_ENV')
pinecone_index = os.environ.get('PINECONE_INDEX')

async def download_file(session, url, output_directory):
    async with session.get(url) as response:
        if response.status == 200:
            file_name = os.path.join(output_directory, os.path.basename(url))
            file_content = await response.read()
            with open(file_name, 'wb') as file:
                file.write(file_content)
            # print(f"Downloaded: {url}")
        else:
            print(f"Failed to download: {url}")

async def ingest_docs(url, namespace, openai_api_key):
    base_url = url

    # Create a temporary directory
    with tempfile.TemporaryDirectory() as temp_dir:
        async with aiohttp.ClientSession() as session:
            async with session.get(base_url) as response:
                if response.status == 200:
                    soup = BeautifulSoup(await response.text(), "html.parser")
                    tasks = []

                    # Search for HTML files in the navbar
                    for link in soup.find_all("a", {"class": "reference internal"}):
                        file_url = urljoin(base_url, link['href'])
                        if file_url.endswith('.html'):
                            tasks.append(download_file(session, file_url, temp_dir))

                    await asyncio.gather(*tasks)
                else:
                    print("Failed to retrieve the page.")

        from langchain.document_loaders.readthedocs import ReadTheDocsLoader

        class MyReadTheDocsLoader(ReadTheDocsLoader):
            """My custom ReadTheDocsLoader."""

            def _clean_data(self, data: str) -> str:
                from bs4 import BeautifulSoup

                soup = BeautifulSoup(data, **self.bs_kwargs)

                # default tags
                html_tags = [
                    ("div", {"role": "main"}),
                    ("main", {"id": "main-content"}),
                    ("body", {})
                ]

                text = None

                # reversed order. check the custom one first
                for tag, attrs in html_tags[::-1]:
                    text = soup.find(tag, attrs)
                    # if found, break
                    if text is not None:
                        break

                if text is not None:
                    text = text.get_text()
                else:
                    text = ""

                # trim empty lines
                return "\n".join([t for t in text.split("\n") if t])

        loader = MyReadTheDocsLoader(temp_dir, features='html.parser', encoding='utf-8')
        docs = loader.load()
        text_splitter = RecursiveCharacterTextSplitter(chunk_size=2000, chunk_overlap=100)
        texts = text_splitter.split_documents(docs)
        # print(docs)

        pinecone.init(
            api_key=pinecone_api_key,
            environment=pinecone_env
        )
        embeddings = OpenAIEmbeddings(model='text-embedding-ada-002', openai_api_key=openai_api_key)
        Pinecone.from_documents(texts, embeddings, index_name=pinecone_index, namespace=namespace)
        # print('loaded!')