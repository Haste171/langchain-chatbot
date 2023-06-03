import interactions
from interactions import Client, CommandContext
from dotenv import load_dotenv
from utils.mongo_db import MongoDBHandler
import sys

sys.path.append('../')
handler = MongoDBHandler('database')
embed_color = 0xfd7c42

load_dotenv()

class DeleteSpace(interactions.Extension):
    def __init__(self, client):
        self.client: Client = client

    @interactions.extension_command()
    @interactions.option(name="space_id", description="The ID of the space you want to delete.", type=str, required=True)
    async def delete_space(self, ctx: CommandContext, space_id: str):
        await ctx.defer()
        embed = interactions.Embed(title='Delete Space', color=embed_color)
        try:
            user_id = str(ctx.author.id)
            space_name = handler.get_space_name(user_id=user_id, space_id=space_id)
            r = handler.delete_space(user_id=user_id, space_id=space_id)
            embed.add_field(name="Status", value=f"Successfully deleted!\n**Space name:** `{space_name}`\n**Space ID:** `{space_id}`", inline=True)
        except ValueError as e:
            embed.add_field(name="Error", value=str(e), inline=True)
            print(e)
        await ctx.send(embeds=[embed])


def setup(client):
    DeleteSpace(client)
