import lightbulb
loader = lightbulb.Loader()
from profanity_check import predict

@loader.command
class Echo(lightbulb.SlashCommand, name="echo", description="echoes what is inputted"):
    echo = lightbulb.string('echo', 'echoes what is inputted')
    @lightbulb.invoke
    async def invoke(self, ctx: lightbulb.Context) -> None:
        filter_echo = predict([self.echo])
        if filter_echo > 0.7:
            await ctx.respond("Please avoid Profanity")
        else:
            await ctx.respond(self.echo)


@loader.command
class Ping(lightbulb.SlashCommand, name="ping", description="Checks the bot is alive"):
    
    @lightbulb.invoke
    async def invoke(self, ctx: lightbulb.Context) -> None:
        await ctx.respond(ctx.user.mention)