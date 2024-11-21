import lightbulb
from bs4 import BeautifulSoup
import bot
import requests
import hikari
import os

loader = lightbulb.Loader()

def serch(search_term):
    url = "https://www.google.ca/search?q=SearchTerm&tbm=isch"
    url = url.split("SearchTerm")
    url = url[0] + search_term + url[1]
    page = requests.get(url)
    soup = BeautifulSoup(page.content, 'html.parser')
    image_tags = soup.find_all('img')
    links = []
    for image_tag in image_tags:
        links.append(image_tag['src'])
    return links


@loader.command
class Search(lightbulb.SlashCommand, name="imgsearch", description="imgsearch"):
    search_term = lightbulb.string("searchterm", "searchterm")
    @lightbulb.invoke
    async def invoke(self, ctx: lightbulb.Context) -> None:
        img = serch(self.search_term)[1]
        emb = hikari.Embed(timestamp=bot.time()).set_image(img).set_footer(
            text=f"Requested by {ctx.member.display_name}",
            icon=ctx.member.avatar_url,
        )
        await ctx.respond(emb)
