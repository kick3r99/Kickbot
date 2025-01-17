import lightbulb
from bs4 import BeautifulSoup
import itertools
import bot
import requests
import hikari
from profanity_check import predict

loader = lightbulb.Loader()

#This function searches for the inputted search term and outputs the first image it finds
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

#img search command here
@loader.command
class Search(lightbulb.SlashCommand, name="img_search", description="imgsearch"):
    search_term = lightbulb.string("searchterm", "searchterm")

    @lightbulb.invoke
    async def invoke(self, ctx: lightbulb.Context) -> None:
        filter_search_term = predict([self.search_term])
        if filter_search_term > 0.7:
            await ctx.respond("Please avoid Profanity")
        else:
            search_term = self.search_term
            img = serch(self.search_term)[1]
            emb = (hikari.Embed(timestamp=bot.time(),title=f"Prompt: {search_term}").set_image(img)
            .set_footer(
                text=f"Requested by {ctx.member.display_name}",
                icon=ctx.member.avatar_url,
            ))
            await ctx.respond(emb)




#reddit
def getdata(url):
    r = requests.get(url)
    return r.text
#reddiscrape command, atm takes in a reddit link and pastes its contents to discord
@loader.command
class RedditScrape(lightbulb.SlashCommand, name="reddit_scrape", description="scrapes a reddit post"):
    url = lightbulb.string("redditurl", "paste url here")
    @lightbulb.invoke
    async def invoke(self, ctx: lightbulb.Context) -> None:
        reddit = getdata(self.url)
        empty = ""
        red = BeautifulSoup(reddit, 'html.parser')

        for item in red.find_all('div', class_='text-neutral-content'):
            redfinal = empty + item.get_text()
            redlist = itertools.batched(redfinal, 1024)

            emb = (hikari.Embed(timestamp=bot.time(), title=f"Reddit Post")
            .set_footer(
            text=f"{self.url}",
            icon=ctx.member.avatar_url,
            ))

            for i in redlist:
                emb.add_field(name = "⠀", value = "".join(i), inline = False)



            await ctx.respond(emb)



