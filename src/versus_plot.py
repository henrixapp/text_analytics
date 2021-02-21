from pipeline.pipeline import Fork, Pass, Pipeline
from pipeline.data_access import DataSetSource, PDReduce, PickleDump, PickleLoad
from pipeline.preprocessing import CuisineSetSplit, Lower, OneHotEnc, OutOfDistributionRemover, Split
from pipeline.generics import First, IterableApply, Lambda, ZipList
from pipeline.analysis import CuisineMLP, IngredientsPerStepsOccurrenceBySimilarity, KMeansClusterer, KMeansNew, PhraserStep, VectorizeAndSum, W2VStep
from pipeline.visualization import VisualizeBoundaries
from dataloader.dataloader import DataLoader


def train_pipeline():
    p = Pipeline(
        "cuisine",
        steps=[
            DataSetSource(datasets=[DataLoader.WHATS_COOKING]),
            PDReduce(['name', 'cuisine', 'ingredients']),
            Fork(  # Pre-Procesing Fork
                "calc w2v, one hot, and pass names",
                steps=[
                    Pipeline(
                        "2",
                        steps=[
                            Fork(
                                "ingredientmapping",
                                steps=[
                                    Pipeline(
                                        "zutaten zerstoeren",
                                        steps=[
                                            PDReduce("ingredients"),
                                            Fork(
                                                "3",
                                                steps=[
                                                    Pipeline(
                                                        name="store",
                                                        steps=[
                                                            W2VStep(8, 20),
                                                            PickleDump(
                                                                "w2v_model.pickle"
                                                            )
                                                        ]),
                                                    Pass(),
                                                ]),
                                            VectorizeAndSum()
                                        ],
                                        verbosity=True),
                                ]),
                        ]),
                    Pipeline("onehot_cuisine",
                             steps=[
                                 PDReduce("cuisine"),
                                 OneHotEnc(),
                             ]),
                    PDReduce("name")
                ]),
            # Output from fork is w2v, cuisine (onehot, encoding), names
            # Splits dataset into training and test set
            CuisineSetSplit(training=99),
            Pipeline(  # Classification Pipeline
                "calc classifiers on split dataset",
                steps=[
                    CuisineMLP(hidden_layer_sizes=(10, 15, 20), max_iter=2000),
                    Lambda(lambda x: x[0]),
                    PickleDump("mlpclf.pickle")
                ])
        ],
        verbosity=True)
    return p.process(True)


def test_pipeline():
    p = Pipeline(
        "word2vecSum",
        steps=[
            DataSetSource(datasets=["whats-cooking"]),
            Fork(
                "recept",
                steps=[
                    Pipeline(
                        "KMeans",
                        steps=[
                            Pipeline(
                                "zutaten zerstoeren",
                                steps=[
                                    PDReduce("ingredients"
                                             ),  # TODO Clean, or make NER
                                    IterableApply(IterableApply(Lower())),
                                    Fork("3",
                                         steps=[
                                             PickleLoad("w2v_model.pickle"),
                                             Pass(),
                                         ]),
                                    VectorizeAndSum()
                                ],
                                verbosity=True),
                            Fork(
                                "kmeans",
                                steps=[
                                    Pass(),  # Value by pass
                                    Pipeline(name="kMeansClusterer",
                                             steps=[KMeansClusterer(20)]),
                                    Pipeline(
                                        name="cuisine MLP",
                                        steps=[
                                            Fork("Load MLP from Pickle",
                                                 steps=[
                                                     PickleLoad(
                                                         "mlpclf.pickle"),
                                                     Pass(),
                                                 ]),
                                            Lambda(  # do the prediction
                                                lambda x: x[0].predict(x[1]))
                                        ])
                                ]),
                        ]),
                    PDReduce("name")
                ]),
            VisualizeBoundaries(100)
        ],
        verbosity=True)
    pi = Pipeline("test",
                  steps=[
                      Fork("nothin",
                           steps=[
                               PDReduce("1"),
                               PDReduce("3"),
                               Pipeline("inner",
                                        steps=[PDReduce(3),
                                               PDReduce(5)])
                           ])
                  ])
    open("test.dot", "w").write(p.visualize_digraph())
    return  #p.process(True)


if __name__ == "__main__":
    test_pipeline()