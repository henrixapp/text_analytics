import matplotlib.pyplot as plt
import mplcursors


class Tooltipped2DScatterPlot():
    """
    Creates two dimensional scatter plot which shows labels when you hover over data points.
    Expects data to be 2D array-like structure with coordinates for each data point.
    """
    def __init__(self,
                 data,
                 labels,
                 colors,
                 title="Recipe Clusters",
                 extras=None):
        self.data = data
        self.labels = labels
        self.colors = colors
        self.title = title
        self.extras = extras

    def plot(self):
        fig, ax = plt.subplots()
        plt.subplots_adjust(right=0.5)
        ax.scatter(*self.data, c=self.colors)
        ax.set_title(self.title)

        # these are matplotlib.patch.Patch properties
        props = dict(boxstyle='round',
                     facecolor='white',
                     edgecolor='white',
                     alpha=1)

        # place a text box in upper left in axes coords
        ax.text(1.05,
                0.95,
                "Recipe Information",
                transform=ax.transAxes,
                fontsize=14,
                verticalalignment='top',
                bbox=props)

        crs = mplcursors.cursor(ax, hover=True)

        def hover(sel):
            recipe_name = self.labels[sel.target.index]
            processed_steps = self.extras[
                sel.target.index] if self.extras else ""

            sel.annotation.set_text('{}'.format(recipe_name))
            ax.text(
                1.05,
                0.95,
                "                                                                                                                                                                       \n                                                                                                                                                        ",
                transform=ax.transAxes,
                fontsize=14,
                verticalalignment='top',
                bbox=props)
            ax.text(1.05,
                    0.95,
                    "{}:\n{}".format(recipe_name, processed_steps),
                    transform=ax.transAxes,
                    fontsize=14,
                    verticalalignment='top',
                    bbox=props)

        crs.connect("add", hover)

        plt.show()