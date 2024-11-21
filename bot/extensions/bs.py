import os
from profanity_check import predict
import lightbulb
from atproto import Client
from dotenv import load_dotenv

# atproto is bsky api fyi
# getting pass and user from .env
BASEDIR = os.path.abspath(os.path.dirname(__file__))
load_dotenv(os.path.join(BASEDIR, '.env'))
User = os.getenv("BSuser")
Pass = os.getenv("BSpass")

# login
bsclient = Client()
bsclient.login(User, Pass)
# bsclient.send_post(text='Hello World!')

loader = lightbulb.Loader()


@loader.command
class Bsky(lightbulb.SlashCommand, name="bsky", description="posts to bsky"):
    text: str = lightbulb.string("text", "The text to post")

    @lightbulb.invoke
    async def invoke(self, ctx: lightbulb.Context) -> None:
        censor_bsky = predict([self.text])
        if censor_bsky > 0.7:
            await ctx.respond("Please avoid Profanity")
        else:
            bsclient.send_post(self.text)
            await ctx.respond("Your post has been posted")
