from pipeline.pipeline import PipelineStep, Head
import os
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
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