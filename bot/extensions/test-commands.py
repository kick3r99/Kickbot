import lightbulb

loader = lightbulb.Loader()


@loader.command
class Echo(lightbulb.SlashCommand, name="echo", description="Repeats the given text"):
    text: str = lightbulb.string("text", "The text to repeat")

    @lightbulb.invoke
    async def invoke(self, ctx: lightbulb.Context) -> None:
        await ctx.respond(self.text)

@loader.command
class Ping(lightbulb.SlashCommand, name="ping", description="Checks the bot is alive"):
    
    @lightbulb.invoke
    async def invoke(self, ctx: lightbulb.Context) -> None:
        await ctx.respond("Pong!")