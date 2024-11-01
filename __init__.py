import hikari
from dotenv import load_dotenv
import lightbulb
import os

#Key pathing
BASEDIR = os.path.abspath(os.path.dirname(__file__))
load_dotenv(os.path.join(BASEDIR, '.env'))
Key = os.getenv("API_KEY")
#Hikari
bot = hikari.GatewayBot(Key)

#Lightbulb
client = lightbulb.client_from_app(bot)
bot.subscribe(hikari.StartingEvent, client.start)

#Ping Command
@client.register()
class Ping(
    lightbulb.SlashCommand,
    name = "pingvalid",
    description="sigma",
):
    @lightbulb.invoke
    async def invoke(self, ctx: lightbulb.Context) -> None:
        await ctx.repsond("PONG")



bot.run()