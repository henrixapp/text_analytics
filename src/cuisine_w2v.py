from dataloader.dataloader import DataLoader
from pipeline.data_access import DataSetSource, PDReduce
from pipeline.generics import IterableApply, Lambda, PDSample, ZipList
from pipeline.pipeline import Fork, Pass, Pipeline
from pipeline.preprocessing import AlphaNumericalizer, ApplyJSON, Dropper, ExtractSentenceParts, Lower, NLTKPorterStemmer, OneHotEnc, OutOfDistributionRemover, Replacer, SpacyStep, Split, StopWordsRemoval, CuisineSetSplit
from pipeline.analysis import IngredientsPerStepsOccurrence, IngredientsPerStepsOccurrenceBySimilarity, PhraserStep, VectorizeAndSum, W2VStep, CuisineNearestCentroid, CuisineMLP, CuisineGaussian

import numpy as np


def pipeline():
    p = Pipeline(
        "cuisine",
        steps=[
            DataSetSource(datasets=[DataLoader.WHATS_COOKING]),
            PDSample(10000, 65510),
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
                                                                W2VStep(8, 10),
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
            # Output from for is w2v, cuisine (onehot, encoding), names
            CuisineSetSplit(training=80),  # Splits dataset into training and test set
            Fork(  # Classification Fork
                "calc NearestCentroid and MLP on split dataset",
                steps=[
                    CuisineNearestCentroid(),
                    # TODO NearestNeighbors, Decision Tree and other
                    CuisineGaussian(),
                    CuisineMLP(hidden_layer_sizes=(10, 25, 10),
                               max_iter=20000),
                ])
        ],
        verbosity=True)
    return p.process(True)


def main():
    '''
    Implements different approaches to learn a ingredients to cuisine embedding and analyzes it.
    '''
    data, _ = pipeline()


if __name__ == "__main__":
    main()