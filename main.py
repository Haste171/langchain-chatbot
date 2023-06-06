import interactions
import os
from dotenv import load_dotenv
from interactions import Client
load_dotenv()

token = os.environ.get('BOT_TOKEN')

bot = interactions.Client(token=token)

def extensions(client: Client, directory: str):
    modules = [
        module[:-3]
        for module in os.listdir(f"./{directory}")
        if module not in "__init__.py" and module[-3:] == ".py"
    ]

    if modules:
        print(f"Importing extensions: {len(modules)}, {', '.join(modules)}")
    else:
        print("Could not import any extensions!")

    for cog in modules:
        try:
            client.load(f"modules.{cog}")
        except Exception:
            print(f"Could not load a {directory} extension: {cog}", exc_info=True)

extensions(bot, "modules")

 
bot.start()