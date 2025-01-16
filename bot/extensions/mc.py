import lightbulb
import re
import bot
import hikari
from mcstatus import  JavaServer

loader = lightbulb.Loader()

@loader.command
class McJava(lightbulb.SlashCommand, name="javaservercheck", description="pinganmcserver"):
    server = lightbulb.string("serverip", "serverip")
    @lightbulb.invoke
    async def invoke(self, ctx: lightbulb.Context) -> None:
        #make this check for specific formatting later
        lookup = JavaServer.lookup(self.server)
        status = lookup.status()
        #This rounds the latency
        latency = round(status.latency, 2)
        # replaces § followed by anything with nothing
        # \s finds whitespace characters + means as many as possible then replaces them with a single space
        description = re.sub(r"\s+"," ",re.sub(r"§.","", status.description).replace("\n", ""))

        emb = ((hikari.Embed(timestamp=bot.time(), title=self.server)
        # Embed info from mc server
               .set_image(status.icon)
               .add_field(name="Description", value=description)
               .add_field(name="Latency", value=str(latency) + "ms")
               .add_field(name="Version", value=status.version.name)
               .add_field(name="Players", value=f"{status.players.online}" + "/" + f"{status.players.max}"))
               .set_footer(text=f"Requested by {ctx.member.display_name}",
                icon=ctx.member.avatar_url))
        await ctx.respond(emb)