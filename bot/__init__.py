import os
import datetime
import hikari
import lightbulb
from dotenv import load_dotenv
from bot import extensions
#date function for convenience's sake
def time():
    date = datetime.datetime.now().astimezone(datetime.timezone(datetime.timedelta(hours=-5)))
    return date
# Key pathing
BASEDIR = os.path.abspath(os.path.dirname(__file__))
load_dotenv(os.path.join(BASEDIR, '.env'))
Key = os.getenv("API_KEY")
# Hikari __init__
bot = hikari.GatewayBot(Key)
# Lightbulb __init__
client = lightbulb.client_from_app(bot)


@bot.listen(hikari.StartingEvent)
async def on_starting(_: hikari.StartingEvent) -> None:
    # Load the commands
    await client.load_extensions_from_package(extensions)
    # Start the client - causing the commands to be synced with discord
    await client.start()
