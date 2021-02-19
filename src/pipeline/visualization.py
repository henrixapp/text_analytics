from pipeline.pipeline import PipelineStep, Head
import os
import warnings
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.manifold import TSNE
from sklearn.cluster import KMeans

import matplotlib.colors as mcolors
import matplotlib as mpl
import pandas as pd

sns.set(style="darkgrid")


class CuisineConfMat(PipelineStep):
    """
    Implementation of Plotting Pipeline for Cuisine Confusion Matrices. Using matplotlib and seaborn in background.

    Important notice. Only works right directly behind one classifier or a fork of multiple classifiers.

    Input: (Fork List of) n-Data-Tuple consting of:
            *clf: Trained Classifier
            acc: Accuracy on the test set
            test_clf: predicted classes of test_set
            test_onehot: ground_truth classes of test_set
            test_encode: Encoding vector to names
            test_names: Names of cuisine
    Output: List of saved matplotlib diagrams save locations
    """
    def __init__(self, save_dir="./viz/", show_plot=False):
        super().__init__("CuisineConfMat")
        self.save_dir = save_dir
        self.show_plot = show_plot
        self.saved_img = []

        if not os.path.exists(save_dir): os.mkdir(save_dir)

    def process(self, data, head=Head()):
        head.addInfo(self.name, "Cuisine Cofusion Matrix")

        n_clf = len(data)  # Number of different classifications
        # Classification Names, first seperate Head infos, then splice real names from identifiers
        clf_names = head._infos[-((6 + 1) * 2):][1:-2:2]
        conf_mats = []  # Added for testing purposes
        for i, clf_data in enumerate(data):
            _, acc, test_clf, test_onehot, test_encode, test_names = clf_data

            conf_mat_test = np.zeros((len(test_encode), len(test_encode)))
            for test, gt in zip(test_clf, test_onehot):
                conf_mat_test[test, gt] += 1
            # Division by 0 warning can be ignored because of stability against it inside of numpy and an output in these colums of NaN
            with warnings.catch_warnings():
                warnings.simplefilter("ignore")
                conf_mat_test = np.transpose(
                    np.transpose(conf_mat_test) / conf_mat_test.sum(1))
            conf_mats.append(conf_mat_test)

            figure = plt.figure(figsize=(14, 12))
            sns.heatmap(conf_mat_test,
                        annot=True,
                        fmt=".2f",
                        vmin=0,
                        vmax=1,
                        xticklabels=test_encode,
                        yticklabels=test_encode,
                        square=True)
            plt.ylabel('True label')
            plt.xlabel('Predicted label')
            plt.title(
                f'Confusion Matrix of {clf_names[i]} with accuracy {acc*100:.2f}%'
            )
            if self.show_plot: plt.show()
            self.saved_img.append(
                os.path.join(self.save_dir,
                             (clf_names[i] + ".jpg")).replace(" ", ""))
            plt.savefig(self.saved_img[-1], dpi=300)
            plt.close()

        data = self.saved_img, conf_mats
        return data, head


mStyles = [
    ".", ",", "o", "v", "^", "<", ">", "1", "2", "3", "4", "8", "s", "p", "P",
    "*", "h", "H", "+", "x", "X", "D", "d", "|", "_", 0, 1, 2, 3, 4, 5, 6, 7,
    8, 9, 10, 11
]


class VisualizeBoundaries(PipelineStep):
    def __init__(self, numberOfVis):
        self.numberOfVis = numberOfVis
        super().__init__("visualize boundaries")

    def process(self, data, head=Head()):
        """
          """
        words_vec = data[0][0][:self.numberOfVis]
        dim = len(words_vec[0])

        embs = np.empty((0, dim), dtype='f')  # to save all the embeddings
        word_labels = data[1][:self.numberOfVis]
        label_1 = data[0][1][:self.numberOfVis]
        label_2 = data[0][2][:self.numberOfVis]
        for vec in words_vec:
            if vec.ndim > 0:
                embs = np.append(embs, [vec], axis=0)

        np.set_printoptions(suppress=True)
        Y = TSNE(
            n_components=2, random_state=42, perplexity=30,
            n_iter=5000).fit_transform(
                embs)  # with  n_components=2, random_state=42, perplexity=15
        # Sets everything up to plot
        df = pd.DataFrame({
            'x': [x for x in Y[:, 0]],
            'y': [y for y in Y[:, 1]],
            'words':
            word_labels,
            'color': [list(mcolors.XKCD_COLORS)[i] for i in label_2],
            'marker1': [mStyles[i] for i in label_1]
        })
        fig, _ = plt.subplots()
        fig.set_size_inches(10, 10)

        #Basic plot
        for s in mStyles:
            p1 = sns.regplot(data=df[df["marker1"] == s],
                             x="x",
                             y="y",
                             marker=s,
                             fit_reg=False,
                             scatter_kws={
                                 's': 40,
                                 'facecolors': df[df["marker1"] == s]["color"]
                             })
        # adds annotations one by one with a loop
        # for line in range(0, df.shape[0]):
        #     p1.text(df["x"][line],
        #             df['y'][line],
        #             '  ' + df["words"][line].title(),
        #             horizontalalignment='left',
        #             verticalalignment='bottom',
        #             size='medium',
        #             color=df['color'][line],
        #             weight='normal').set_size(15)

        plt.xlim(Y[:, 0].min() - 50, Y[:, 0].max() + 50)
        plt.ylim(Y[:, 1].min() - 50, Y[:, 1].max() + 50)

        plt.title('t-SNE visualization for {} elements'.format(
            str(self.numberOfVis)))
        plt.show()
