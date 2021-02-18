from pipeline.pipeline import PipelineStep, Head


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
    def __init__(self, save_dir="./"):
        super().__init__("CuisineConfMat")
        self.save_dir = save_dir
        self.saved_img = []

    def process(self, data, head=Head()):
        head.addInfo(self.name, "Cuisine Cofusion Matrix")

        n_cls = len(data)  # Number of different classifications
        # Classification Names, first seperate Head infos, then splice real names from identifiers
        cls_names = head._infos[-((6 + 1) * 2):][1:-2:2]
        print(cls_names)

        return self.saved_img, head