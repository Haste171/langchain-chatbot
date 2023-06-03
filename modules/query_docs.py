import os, sys
import interactions
from utils.mongo_db import MongoDBHandler
from utils.llm_query import llm_query
from interactions import Client, CommandContext
from dotenv import load_dotenv

sys.path.append('../')
handler = MongoDBHandler('database')
embed_color = 0xfd7c42
load_dotenv()

class QueryDocs(interactions.Extension):
    def __init__(self, client):
        self.client: Client = client

    @interactions.extension_command()
    @interactions.option(name="query", description="A query message for the llm", type=str, required=True) # Makes sure to ask for the variable when using the command
    @interactions.option(name="space_id", description="The ID of the space you want to query.", type=str, required=True)
    async def query_docs(self, ctx: CommandContext, query: str, space_id: str): # Make sure the type of variable is the same
        await ctx.defer(ephemeral=True)
        chat_history = []
        try: 
            creds = handler.get_user_credentials(user_id=str(ctx.author.id))
            if creds:
                ownership = handler.check_ownership(user_id=str(ctx.author.id), space_id=space_id)
                if ownership:
                    openai_key = creds['credentials']['openai_api_key']
                    try:
                        q = llm_query(namespace=space_id, openai_api_key=openai_key)
                        result = q({"question": query, "chat_history": chat_history})
                        source_documents = result['source_documents']
                        # Parse the source documents for display
                        parsed_documents = []
                        for doc in source_documents:
                            parsed_doc = {
                                "page_content": doc.page_content,
                                "metadata": {
                                    "author": doc.metadata.get("author", ""),
                                    "creationDate": doc.metadata.get("creationDate", ""),
                                    "creator": doc.metadata.get("creator", ""),
                                    "file_path": doc.metadata.get("file_path", ""),
                                    "format": doc.metadata.get("format", ""),
                                    "keywords": doc.metadata.get("keywords", ""),
                                    "modDate": doc.metadata.get("modDate", ""),
                                    "page_number": doc.metadata.get("page_number", 0),
                                    "producer": doc.metadata.get("producer", ""),
                                    "source": doc.metadata.get("source", ""),
                                    "subject": doc.metadata.get("subject", ""),
                                    "title": doc.metadata.get("title", ""),
                                    "total_pages": doc.metadata.get("total_pages", 0),
                                    "trapped": doc.metadata.get("trapped", "")
                                }
                            }
                            parsed_documents.append(parsed_doc)
                        # print(parsed_documents)
                        embed = interactions.Embed(title='Query Results', description=f'{result["answer"]}\n\n', color=embed_color)
                        for i, doc in enumerate(parsed_documents, start=1):
                            source = doc['metadata']['source']
                            source_name = os.path.basename(source)
                            embed.add_field(name=f"Source {i}", value=f'{source_name}', inline=True)

                        source_count = len(parsed_documents)
                        embed.set_footer(text=f"Total Sources: {source_count}")


                        embed.add_field(name="Query", value=f'**{query}**', inline=False)
                        await ctx.send(embeds=embed)
                    except Exception as e:
                        print(e)
                        # embed = interactions.Embed(title='Fatal Error', description=f'Error:\n```python\n{e}\n```', color=embed_color)
                        # await ctx.send(embeds=embed)
                else:
                    embed = interactions.Embed(title='Error', description=f'User does not contain given space ID.', color=embed_color)
                    await ctx.send(embeds=embed)
            elif creds == None:
                embed = interactions.Embed(title='No Credentials', description=f'[OpenAI API Key](https://platform.openai.com/account/api-keys) needs to be set.', color=embed_color)
                embed.add_field(name="Error", value='No credentials set! Use `/set_credentials`.', inline=True)
                await ctx.send(embeds=embed, ephemeral=True)
            else:
                pass
        except Exception as e:
            print(e)


def setup(client):
    QueryDocs(client)
