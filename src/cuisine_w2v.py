from dataloader.dataloader import DataLoader
from pipeline.data_access import DataSetSource, PDReduce
from pipeline.generics import PDSample
from pipeline.pipeline import Fork, Pass, Pipeline
from pipeline.preprocessing import OneHotEnc, CuisineSetSplit
from pipeline.analysis import VectorizeAndSum, W2VStep, CuisineNearestNeighbors, CuisineNearestCentroid, CuisineMLP, CuisineGaussian, CuisineDecisionTree, CuisineRandomForest, CuisineAdaBoost
from pipeline.visualization import CuisineConfMat, CuisineHist

import numpy as np


def pipeline():
    p = Pipeline(
        "cuisine",
        steps=[
            DataSetSource(datasets=[DataLoader.WHATS_COOKING]),
            #PDSample(50, 65510),
            PDReduce(['name', 'cuisine', 'ingredients']),
            Fork(  # Pre-Procesing Fork
                "calc w2v, one hot, and pass names",
                steps=[
                    Pipeline("2",
                             steps=[
                                 Fork("ingredientmapping",
                                      steps=[
                                          Pipeline("zutaten zerstoeren",
                                                   steps=[
                                                       PDReduce("ingredients"),
                                                       Fork("3",
                                                            steps=[
                                                                W2VStep(8, 20),
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
            CuisineSetSplit(training=80),
            Fork(  # Pre-Procesing Fork
                "First data retention for histogram phase",
                steps=[
                    Pass(),
                    Pipeline(
                        "2",
                        steps=[
                            Fork(  # Classification Fork
                                "calc classifiers on split dataset",
                                steps=[
                                    CuisineNearestNeighbors(n_neighbors=10),
                                    CuisineNearestCentroid(),
                                    CuisineDecisionTree(),
                                    CuisineRandomForest(n_estimators=100),
                                    CuisineAdaBoost(n_estimators=50),
                                    #CuisineGaussian(),
                                    CuisineMLP(hidden_layer_sizes=(10, 15, 20),
                                               max_iter=2000),
                                ]),
                            Fork(
                                "Second data retention for histogram phase",
                                steps=[
                                    Pass(),
                                    CuisineConfMat(
                                        show_plot=False),  # ConfMat Viz
                                ]),
                        ]),
                ]),
            CuisineHist(),
        ],
        verbosity=True)
    return p.process(True)


def main():
    '''
    Implements different approaches to learn a ingredients to cuisine embedding and analyzes it.
    '''
    data, head = pipeline()

    #print(len(data[0]))


if __name__ == "__main__":
    main()