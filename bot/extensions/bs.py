import os
from profanity_check import predict
import lightbulb
from atproto import Client
from dotenv import load_dotenv
import hikari
import  bot
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
            post = bsclient.send_post(self.text)
            link = f'https://bsky.app/profile/botiusmaximus.bsky.social/post/{post.uri.split('/')[-1]}'
            emb = (hikari.Embed(
            timestamp=bot.time(),
            url = link,
            title=f"Your post has been posted.").
            set_footer(
            text=f"Requested by {ctx.member.display_name}",
            icon=ctx.member.avatar_url,
                )
            )
            await ctx.respond(emb)

