import interactions
from interactions import Client, CommandContext
from dotenv import load_dotenv
from utils.mongo_db import MongoDBHandler
import sys

sys.path.append('../')
handler = MongoDBHandler('database')
embed_color = 0xfd7c42

load_dotenv()

class Help(interactions.Extension):
    def __init__(self, client):
        self.client: Client = client

    @interactions.extension_command()
    async def help(self, ctx: CommandContext): # Make sure the type of variable is the same 
        await ctx.defer(ephemeral=True)
        embed = interactions.Embed(title='Help', color=embed_color)
        embed.set_author(name="GitHub [Click Here]", url="https://github.com/Haste171/langchain-chatbot", icon_url="https://cdn.discordapp.com/attachments/1114412425115086888/1114413065933439058/25231.png")
        embed.add_field(name="/help", value='List of commands and descriptions.', inline=True)
        embed.add_field(name="/set_credentials", value='Set your external credentials to use bot.', inline=True)
        embed.add_field(name="/credentials", value='View your credentials.', inline=True)
        embed.add_field(name="/ingest_docs", value='Ingest readthedocs.io documentation website.', inline=True)
        embed.add_field(name="/spaces", value='View a list of your ingested documentation websites.', inline=True)
        embed.add_field(name="/spaces", value='Delete a ingested documentation website.', inline=True)
        embed.add_field(name="/query_docs", value='Query an ingested documentation website.', inline=True)
        await ctx.send(embeds=embed, ephemeral=True)


def setup(client):
    Help(client)
