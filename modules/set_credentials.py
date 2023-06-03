import interactions
from interactions import Client, CommandContext
from utils.mongo_db import MongoDBHandler
import openai

embed_color = 0xfd7c42

handler = MongoDBHandler('database')

def test_api_key(api_key):
    openai.api_key = api_key

    try:
        response = openai.Completion.create(
            engine='davinci',
            prompt='Hello, World!',
            max_tokens=5
        )

        if response['choices'][0]['text']:
            return True
        else:
            return False
    except Exception as e:
        return False

class SetCredentials(interactions.Extension):
    def __init__(self, client):
        self.client: Client = client

    @interactions.extension_command()
    @interactions.option(name="openai_api_key", description="Your OpenAI API Key.", type=str, required=True)
    async def set_credentials(self, ctx: CommandContext, openai_api_key): # Make sure the type of variable is the same 
        await ctx.defer(ephemeral=True)

        is_valid = test_api_key(openai_api_key)

        if is_valid:
            embed = interactions.Embed(title='Set Credentials', color=embed_color)
            try:
                creds = handler.create_user_credentials(user_id=str(ctx.author.id), user_name='test_username', openai_api_key=openai_api_key)
                print(creds)
                r = handler.get_user_credentials(user_id=str(ctx.author.id))
                openai_api_key = r['credentials']['openai_api_key']
                embed.add_field(name='OpenAI API Key', value=f'`{openai_api_key}`', inline=True)
                await ctx.send(embeds=embed, ephemeral=True)
            except Exception as e:
                print(e)
        else:
            embed = interactions.Embed(title='Error', description='API Key is Invalid!', color=embed_color)
            await ctx.send(embeds=embed, ephemeral=True)
def setup(client):
    SetCredentials(client)
