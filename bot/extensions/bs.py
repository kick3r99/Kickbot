import lightbulb
from atproto import Client
import os
from dotenv import load_dotenv
#atproto is bsky api fyi
#getting pass and user from .env
BASEDIR = os.path.abspath(os.path.dirname(__file__))
load_dotenv(os.path.join(BASEDIR, '.env'))
User = os.getenv("BSuser")
Pass = os.getenv("BSpass")

#login
bsclient = Client()
bsclient.login(User, Pass)
# bsclient.send_post(text='Hello World!')

loader = lightbulb.Loader()

@loader.command
class Echo(lightbulb.SlashCommand, name="bsky", description="posts to bsky"):
    text: str = lightbulb.string("text", "The text to post")

    @lightbulb.invoke
    async def invoke(self, ctx: lightbulb.Context) -> None:
        await ctx.respond(bsclient.send_post(self.text))