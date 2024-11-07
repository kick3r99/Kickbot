import lightbulb
import matplotlib.pyplot as plt
import re
import hikari
import os


loader = lightbulb.Loader()
number_pattern = re.compile(r"^\d+( \d+)*$")

#plot function to be called
def plot(data1, data2, chart_choice):
    if chart_choice == "bar":
      chart =  plt.bar(data1, data2)
      plt.savefig('data/fig.png')
    elif chart_choice == "plot":
      chart = plt.plot(data1, data2)
      plt.savefig('data/fig.png')
    return


#plot command
@loader.command
class Ping(lightbulb.SlashCommand, name="plot", description="plot data using matplotlib. Seperate data using spaces"):
    data1 = lightbulb.string("firstdataset", "data")
    data2 = lightbulb.string("seconddataset", "data")
    chart = lightbulb.string(
        "plot",
        "the type of plot to use",
        choices = [lightbulb.Choice("bar", "bar"), lightbulb.Choice("plot", "plot")])

    @lightbulb.invoke
    async def invoke(self, ctx: lightbulb.Context) -> None:
        if not number_pattern.match(self.data1) or not number_pattern.match(self.data2):
            await ctx.respond("Nuh uh")
            return

        else:
            #chartdata TODO add more input options (color, title, label, etc.)
            chart_choice = self.chart
            data1_numbers = list(map(int, self.data1.split()))
            data2_numbers = list(map(int, self.data2.split()))
            plot(data1_numbers, data2_numbers, chart_choice)
            plotimg = hikari.File("data/fig.png")


            plotemb = (hikari.Embed(title = f"",description = f"").set_image(plotimg))


            await ctx.respond(plotemb)
            os.remove("data/fig.png")