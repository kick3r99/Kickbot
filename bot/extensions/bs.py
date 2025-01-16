import os

import atproto_client.exceptions
import hikari
import lightbulb
from atproto import Client
from dotenv import load_dotenv
from profanity_check import predict
import random
from datetime import datetime

import bot

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

# use these in place of username and avatar calls
# allows it to be universal and work with any login
handle = bsclient.me.handle
avatar = bsclient.me.avatar

#bsky post command
@loader.command
class BskyPost(lightbulb.SlashCommand, name="blueskypost", description="posts to bsky"):
    text: str = lightbulb.string("text", "The text to post")

    @lightbulb.invoke
    async def invoke(self, ctx: lightbulb.Context) -> None:
        #profanity prevention using profanity_check
        censor_bsky = predict([self.text])
        if censor_bsky > 0.7:
            await ctx.respond("Please avoid Profanity")
            #post to bluesky with the text, and include an embed with the link to post
        else:
            post = bsclient.send_post(self.text)
            link = f'https://bsky.app/profile/{handle}/post/{post.uri.split('/')[-1]}'
            emb = (hikari.Embed(
                timestamp=bot.time(),
                url=link,
                title=f"Your post has been posted.")
            .set_author(
                name=handle,
                url=f"https://bsky.app/profile/{handle}",
                icon=avatar
            )
            .set_footer(
                text=f"Requested by {ctx.member.display_name}",
                icon=ctx.member.avatar_url,
            )
            )
            await ctx.respond(emb)



#bsky follow command
@loader.command
class BskyFollow(lightbulb.SlashCommand, name="blueskyfollow", description="follow someone on bsky"):
    user: str = lightbulb.string("user", "the users username")

#Try to follow user inputted, otherwise output either user not found or rate limited error
    @lightbulb.invoke
    async def invoke(self, ctx: lightbulb.Context) -> None:
        try:
            follow = self.user

            profile = bsclient.get_profile(follow)
            bsclient.follow(profile.did)

            femb = (hikari.Embed(
                timestamp=bot.time(),
                title=f"Successfully followed {follow}")
            .set_author(
                name=handle,
                url=f"https://bsky.app/profile/{handle}/follows",
                icon=avatar
            )
            .set_footer(
                text=f"Requested by {ctx.member.display_name}",
                icon=ctx.member.avatar_url,
            )
            )
            #error handling for unfound profile, rate limit, and other
            await ctx.respond(femb)
        except atproto_client.exceptions.BadRequestError:
            await ctx.respond(f"Error following user: Profile not Found")
        except atproto_client.exceptions.RequestException:
            await ctx.respond("Rate Limited")
        except Exception as e:
            await ctx.respond(f"Unexpected error: {str(e)}")



#bsky feed
@loader.command
class BskyFeed(lightbulb.SlashCommand, name="blueskyfeed", description="feed me cookie"):
    @lightbulb.invoke
    async def invoke(self, ctx: lightbulb.Context) -> None:
        #choose a numbe between 0 and 30 and grab the post in bot's bs feed related to that number
        rng = random.randint(0, 30)
        timeline = bsclient.get_timeline(algorithm='reverse-chronological')
        feed_view = timeline.feed[rng]
        action = '[New post]'
        if feed_view.reason:
            action_by = feed_view.reason.by.handle
            action = f'Reposted by @{action_by}'
        post = feed_view.post.record
        authorfeed = feed_view.post.author


#clause incase post has an image
        image_url = None
        post_embed = getattr(post, "embed", None)
        if post_embed:
            if hasattr(post_embed, "images") and post_embed.images:
                # Construct the image URL using the DID and content hash (CID)
                image_url = f"https://cdn.bsky.app/img/feed_thumbnail/plain/{authorfeed.did}/{post_embed.images[0].image.ref.link}@jpeg"

        raw_timestamp = post.created_at  # ISO 8601 string
        formatted_timestamp = datetime.fromisoformat(raw_timestamp.replace("Z", "+00:00")).strftime(
            "%b %d %Y at %I:%M %p")
        #embed shenanigans
        feemb = (hikari.Embed(
            title = action,
            description=f"{post.text}",
        )
        .set_author(
            name=authorfeed.handle,
            url=f"https://bsky.app/profile/{authorfeed.handle}",
            icon=authorfeed.avatar
        )
        .set_footer(
            icon=ctx.member.avatar_url,
            text=f'Posted on {formatted_timestamp}'
        ))

        # Only set image if a URL was found
        if image_url:
            feemb.set_image(image_url)


        await ctx.respond(feemb)

