import interactions
from interactions import Client, CommandContext
from utils.mongo_db import MongoDBHandler

embed_color = 0xfd7c42
handler = MongoDBHandler('database')

class Credentials(interactions.Extension):
    def __init__(self, client):
        self.client: Client = client

    @interactions.extension_command()
    async def credentials(self, ctx: CommandContext): # Make sure the type of variable is the same 
        await ctx.defer(ephemeral=True)
        embed = interactions.Embed(title='Credentials', color=embed_color)
        try:
            r = handler.get_user_credentials(user_id=str(ctx.author.id))
            if r:
                openai_api_key = r['credentials']['openai_api_key']
                embed.add_field(name='OpenAI API Key', value=f'`{openai_api_key}`', inline=True)
            elif r == None:
                embed.add_field(name="Error", value='No credentials set! Use `/set_credentials`.', inline=True)
            await ctx.send(embeds=embed, ephemeral=True)
        except Exception as e:
           print(e)

def setup(client):
    Credentials(client)
