import interactions
from interactions import Client, CommandContext
from dotenv import load_dotenv
from utils.mongo_db import MongoDBHandler
import sys

sys.path.append('../')
handler = MongoDBHandler('database')
embed_color = 0xfd7c42

load_dotenv()

class Spaces(interactions.Extension):
    def __init__(self, client):
        self.client: Client = client

    @interactions.extension_command()
    async def spaces(self, ctx: CommandContext): # Make sure the type of variable is the same 
        await ctx.defer()
        spaces = handler.list_spaces(user_id=str(ctx.author.id))
        embed = interactions.Embed(title='Spaces', color=embed_color)
        try:
            for space in spaces:
                space_name = space['space_name']
                space_id = space['space_id']
                ingested_url = space['ingested_url']
                ingested_time = space['ingested_time']
                embed.add_field(name=space_name, value=f'{ingested_url}\n**ID:** `{space_id}`\n**Time:** `{ingested_time}`', inline=False)
        except Exception as e:
           embed.add_field(name="Error", value='No Spaces Found', inline=True)
           print(e)
        await ctx.send(embeds=embed)

def setup(client):
    Spaces(client)
