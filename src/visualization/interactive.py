import matplotlib.pyplot as plt
import mplcursors
from sklearn.manifold import TSNE
import matplotlib.colors as mcolors

COLOR_LIST = [
    '#e6194b', '#3cb44b', '#ffe119', '#4363d8', '#f58231', '#911eb4',
    '#46f0f0', '#f032e6', '#bcf60c', '#fabebe', '#008080', '#e6beff',
    '#9a6324', '#fffac8', '#800000', '#aaffc3', '#808000', '#ffd8b1',
    '#000075', '#808080', '#ffffff', '#000000'
]


class Tooltipped2DScatterPlot():
    """
    Creates two dimensional scatter plot which shows names when you hover over data points.
    Expects data to be 2D array-like structure with coordinates for each data point.
    """
    def __init__(self,
                 data,
                 names,
                 labels,
                 title="Recipe Clusters",
                 extras=None):
        self.data = data
        self.names = names
        self.labels = labels
        self.color_list = list(mcolors.XKCD_COLORS)
        self.colors = [self.color_list[label] for label in self.labels]
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
            recipe_name = self.names[sel.target.index]
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


class TooltippedTSNEPlot():
    def __init__(self,
                 data,
                 names,
                 labels,
                 title="Recipe Clusters",
                 extras=None):
        self.data = data
        self.names = names
        self.labels = labels
        self.color_list = list(mcolors) if len(set(
            self.labels)) > 20 else COLOR_LIST
        self.colors = [self.color_list[label] for label in self.labels]
        self.title = title
        self.extras = extras

    def perform_tSNE(self):
        self.embedded = TSNE(n_components=2).fit_transform(self.data)

    def plot(self):
        self.perform_tSNE()
        fig, ax = plt.subplots()
        plt.subplots_adjust(right=0.5)
        plt.axis('off')
        ax.scatter(*self.embedded.T, c=self.colors)
        ax.set_title(self.title)

        # these are matplotlib.patch.Patch properties
        props = dict(boxstyle='round',
                     facecolor='white',
                     edgecolor='white',
                     alpha=1)

        for i, top_terms in enumerate(self.extras):
            ax.text(1.05,
                    0.05 + i * 0.08,
                    top_terms,
                    transform=ax.transAxes,
                    fontsize=14,
                    verticalalignment='top',
                    bbox=props,
                    color=self.color_list[i])

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
            recipe_name = self.names[sel.target.index]
            # processed_steps = self.extras[
            # sel.target.index] if self.extras else ""
            processed_steps = ''

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
                    "{}:\n\n{}".format(recipe_name, processed_steps),
                    transform=ax.transAxes,
                    fontsize=14,
                    verticalalignment='top',
                    bbox=props)

        crs.connect("add", hover)

        plt.show()
