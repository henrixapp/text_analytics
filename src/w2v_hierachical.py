from dataloader.dataloader import DataLoader
from pipeline.data_access import DataSetSource, PDReduce
from pipeline.generics import IterableApply, Lambda, PDSample
from pipeline.pipeline import Fork, Pass, Pipeline
from pipeline.preprocessing import AlphaNumericalizer, ApplyJSON, Dropper, Lower, NLTKPorterStemmer, OutOfDistributionRemover, Replacer, Split, StopWordsRemoval
from sklearn.feature_extraction.text import TfidfVectorizer
from nltk.corpus import stopwords
import scipy.cluster.hierarchy as shc
import matplotlib.pyplot as plt
from pipeline.analysis import IngredientsPerStepsOccurrence, IngredientsPerStepsOccurrenceBySimilarity, PhraserStep, W2VStep


def pipeline():
    p = Pipeline(
        "word2vecSum",
        steps=[
            DataSetSource(datasets=[DataLoader.RECIPENLG]),
            Dropper(columns_causing_drop=['steps']),
            OutOfDistributionRemover(),
            PDSample(250000),
            PDReduce(['name', 'steps', 'NER']),
            Fork("calc w2v and pass names",
                 steps=[
                     Pipeline("2",
                              steps=[
                                  Fork("ingredientmapping",
                                       steps=[
                                           Pipeline("zutaten zerstoeren",
                                                    steps=[
                                                        PDReduce("NER"),
                                                        IterableApply(
                                                            ApplyJSON(),
                                                            verbosity=True),
                                                        PhraserStep(),
                                                        Fork("3",
                                                             steps=[
                                                                 W2VStep(8),
                                                                 Pass(),
                                                             ]),
                                                    ],
                                                    verbosity=True),
                                           Pipeline("spacy steps",
                                                    steps=[
                                                        PDReduce("steps"),
                                                        IterableApply(
                                                            IterableApply(
                                                                Split(" ")),
                                                            verbosity=True)
                                                    ])
                                       ]),
                                  IngredientsPerStepsOccurrenceBySimilarity(
                                      activation_function=lambda x: x)
                              ]),
                     PDReduce("name")
                 ]),
            #ZipList()
        ],
        verbosity=True)
    return p.process(True)


def main():
    '''
    Implements a very basic baseline approach which can be used to compare more sophisticated approaches to.
    Uses ... dataset, does pre-processing and computes TF-IDF features which are then used by ... clustering algorithm.
    '''
    data, _ = pipeline()
    w2v, names = data

    plt.figure(figsize=(10, 7))
    plt.title("Recipes Dendrogram based on W2V")
    dend = shc.dendrogram(shc.linkage(w2v[:100], method='ward'),
                          labels=list(names[:100]),
                          leaf_font_size=8)

    plt.tight_layout()
    plt.show()


if __name__ == "__main__":
    main()