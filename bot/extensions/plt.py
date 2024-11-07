import os
import re

import hikari
import lightbulb
import matplotlib.pyplot as plt

loader = lightbulb.Loader()
number_pattern = re.compile(r"^\d+( \d+)*$")


# plot function to be called
def plot(data1, data2):
    plt.clf()
    plt.bar(data1, data2)
    plt.savefig('data/fig.png')
    return


# plot command
@loader.command
class Plot(lightbulb.SlashCommand, name="plot", description="plot data using matplotlib. Seperate data using spaces"):
    data1 = lightbulb.string("firstdataset", "data")
    data2 = lightbulb.string("seconddataset", "data")

    @lightbulb.invoke
    async def invoke(self, ctx: lightbulb.Context) -> None:
        if not number_pattern.match(self.data1) or not number_pattern.match(self.data2):
            await ctx.respond("Please provide valid number sequences")
            return

        data1_numbers = list(map(int, self.data1.split()))
        data2_numbers = list(map(int, self.data2.split()))

        if len(data1_numbers) != len(data2_numbers):
            await ctx.respond("Both datasets must have the same length")
            return

        try:
            plot(data1_numbers, data2_numbers)
            plotimg = hikari.File("data/fig.png")
            # footer copied from old code
            plotemb = hikari.Embed().set_image(plotimg).set_footer(
                text=f"Requested by {ctx.member.display_name}",
                icon=ctx.member.avatar_url)
            await ctx.respond(plotemb)
        # error handling wow!
        except Exception as e:
            await ctx.respond(f"An error occurred while creating the plot: {str(e)}")

        finally:
            # Clean up the file if it exists
            if os.path.exists("data/fig.png"):
                os.remove("data/fig.png")
