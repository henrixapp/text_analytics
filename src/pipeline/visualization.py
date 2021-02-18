from pipeline.pipeline import PipelineStep, Head
import os
import warnings
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns


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
            Confusion Matrices as list
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

            sns.set(style="darkgrid")
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
                             ("confmat_" + clf_names[i] + ".jpg")).replace(
                                 " ", ""))
            plt.savefig(self.saved_img[-1], dpi=300)
            plt.close()

        data = self.saved_img, conf_mats
        return data, head


class CuisineHist(PipelineStep):
    """
    Implementation of Plotting Pipeline for Cuisine Histograms. Histograms for the distribution of the whole dataset, the training and test set as well as each classified set will be generated.
    Using matplotlib and seaborn in background.

    Important notice. Only works right directly behind one classifier or a fork of multiple classifiers.

    Input:  Training-Test Split consistig of (w2v, cuisine (onehot, encode), names)
            Fork List consisting of:
                (Fork List of) n-Data-Tuple consisting of:
                    *clf: Trained Classifier
                    acc: Accuracy on the test set
                    test_clf: predicted classes of test_set
                    test_onehot: ground_truth classes of test_set
                    test_encode: Encoding vector to names
                    test_names: Names of cuisine
                ConfMat-Tuple consisting of:
                    List of saved matplotlib diagrams save locations
                    Confusion Matrices as list
    Output: List of saved matplotlib diagrams save locations
    """
    def __init__(self, save_dir="./viz/", show_plot=False):
        super().__init__("CuisineHist")
        self.save_dir = save_dir
        self.show_plot = show_plot
        self.saved_img = []

        if not os.path.exists(save_dir): os.mkdir(save_dir)

    def process(self, data, head=Head()):
        head.addInfo(self.name, "Cuisine Histograms")
        # Data Extraction
        split_data, (clfs_data, _) = data
        (_, (train_oh, names_encode), _), (_, (test_oh, _), _) = split_data
        names_encode = np.append(
            names_encode, np.repeat('Not found', (20 - len(names_encode))))

        # Histograms for whole Dataset and Train/Test Split
        train_set = np.array(train_oh)
        test_set = np.array(test_oh)
        data_sets = {
            "Training Set": train_set,
            "Test Set": test_set,
            "Data Set": np.append(train_set, test_set)
        }
        for set_name in data_sets.keys():
            bins = np.bincount(data_sets[set_name], minlength=20)

            fig, ax = plt.subplots(figsize=(11, 10))
            ax.barh(names_encode, bins)
            plt.xlabel('Count')
            plt.title(f'Histogram of {set_name}')
            if self.show_plot: plt.show()
            self.saved_img.append(
                os.path.join(self.save_dir,
                             ("hist_" + set_name + ".jpg")).replace(" ", ""))
            plt.savefig(self.saved_img[-1], dpi=300)
            plt.close()

        # Histograms for predicted classes of different clfs
        n_clf = len(clfs_data)
        clf_names = head._infos[-((6 + 2) * 2):][1:-2:2]

        for i, clf_data in enumerate(clfs_data):
            _, _, test_clf, _, _, _ = clf_data
            bins = np.bincount(test_clf, minlength=20)

            fig, ax = plt.subplots(figsize=(11, 10))
            ax.barh(names_encode, bins)
            plt.xlabel('Count')
            plt.title(
                f'Histogram of classification of test set with {clf_names[i]}')
            if self.show_plot: plt.show()
            self.saved_img.append(
                os.path.join(self.save_dir,
                             ("hist_" + clf_names[i] + ".jpg")).replace(
                                 " ", ""))
            plt.savefig(self.saved_img[-1], dpi=300)
            plt.close()

        return self.saved_img, head