import interactions, sys, uuid
from utils.mongo_db import MongoDBHandler
from utils.ingest_docs import ingest_docs
from interactions import Client, CommandContext
from dotenv import load_dotenv
from datetime import datetime

embed_color = 0xfd7c42
sys.path.append('../')
handler = MongoDBHandler('database')
load_dotenv()

class IngestDocs(interactions.Extension):
    def __init__(self, client):
        self.client: Client = client

    @interactions.extension_command()
    @interactions.option(name="url", description="A url to a readthedocs.io website.", type=str, required=True)
    @interactions.option(name="space_name", description="Space name to save ingestion to", type=str, required=True)
    async def ingest_docs(self, ctx: CommandContext, url: str, space_name: str): # Make sure the type of variable is the same 
        await ctx.defer()
        try: 
            creds = handler.get_user_credentials(user_id=str(ctx.author.id))
            if creds:
                openai_key = creds['credentials']['openai_api_key']
                try:
                    random_uuid = str(uuid.uuid4())
                    embed = interactions.Embed(title='Ingesting', description=f'Attempting to ingest url. *This might take a while*', color=embed_color)
                    await ctx.send(embeds=embed)
                    print('Attempting to ingest')
                    await ingest_docs(url=url, namespace=random_uuid, openai_api_key=openai_key)
                    current_time = datetime.now()
                    handler.handle_data(user_id=str(ctx.author.id), user_name=str(ctx.author.name), space_name=space_name, space_id=random_uuid, ingest_url=url, ingested_time=current_time)
                    embed = interactions.Embed(title='Success', description=f'{url}\n**Space Name:** `{space_name}`\n**Space ID:** `{random_uuid}`\n**Time:** `{current_time}`', color=embed_color)
                    await ctx.send(embeds=embed)
                except Exception as e:
                    print(e)
            elif creds == None:
                embed = interactions.Embed(title='No Credentials', description=f'[OpenAI API Key](https://platform.openai.com/account/api-keys) needs to be set.', color=embed_color)
                embed.add_field(name="Error", value='No credentials set! Use `/set_credentials`.', inline=True)
                await ctx.send(embeds=embed)
            else:
                pass
        except Exception as e:
            print(e)
            

def setup(client):
    IngestDocs(client)
