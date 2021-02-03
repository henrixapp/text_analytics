from matplotlib.pyplot import step
from pipeline.counters import MostCommonCounter
from pipeline.pipeline import Fork, Pass, Pipeline

from pipeline.pipeline import Pipeline
from pipeline.data_access import DataSetSource, JSONSink, PDReduce
from pipeline.generics import First, Flatten, IterableApply, Lambda, Sample, TransformList, Unique, ZipList
from pipeline.preprocessing import ApplyJSON, Lower, OutOfDistributionRemover, SpacyStep, Split, StopWordsRemoval
from pipeline.analysis import IngredientsPerStepsOccurrence, KMeansClusterer, PhraserStep, VectorizeAndSum, W2VStep


def pipeline():
    p = Pipeline("recipennlg",
                 steps=[
                     DataSetSource(datasets=["recipenlg"]),
                     PDReduce("NER"),
                     IterableApply(ApplyJSON()),
                     IterableApply(IterableApply(Lower())),
                     PhraserStep(),
                     JSONSink("recipenlg-phrased.json")
                 ],
                 verbosity=True)
    p.process(True)


def pipeline2():
    p = Pipeline("word2vec",
                 steps=[
                     DataSetSource(datasets=["recipenlg"]),
                     PDReduce("NER"),
                     First(500000),
                     IterableApply(ApplyJSON()),
                     IterableApply(IterableApply(Lower())),
                     PhraserStep(),
                     W2VStep(4)
                 ],
                 verbosity=True)
    return p.process(True)


def pipeline3():
    p = Pipeline("recipennlg",
                 steps=[
                     DataSetSource(datasets=["recipenlg"]),
                     PDReduce("NER"),
                     First(500000),
                     IterableApply(ApplyJSON()),
                     Flatten(),
                     IterableApply(Lower()),
                     MostCommonCounter()
                 ],
                 verbosity=True)
    return p.process(True)


def pipeline4():
    p = Pipeline("word2vecSum",
                 steps=[
                     DataSetSource(datasets=["recipenlg"]),
                     First(50000),
                     Fork("2",
                          steps=[
                              Pipeline(
                                  "vec2sum",
                                  steps=[
                                      PDReduce("NER"),
                                      IterableApply(ApplyJSON()),
                                      IterableApply(IterableApply(Lower())),
                                      PhraserStep(),
                                      Fork("3",
                                           steps=[
                                               Pipeline("1",
                                                        steps=[W2VStep(4)]),
                                               Pipeline("2", steps=[Pass()]),
                                           ]),
                                      VectorizeAndSum()
                                  ]),
                              Pipeline("name",
                                       steps=[PDReduce("name")],
                                       verbosity=True)
                          ]),
                     ZipList()
                 ],
                 verbosity=True)
    return p.process(True)


def pipeline5():
    p = Pipeline(
        "word2vecSum",
        steps=[
            DataSetSource(datasets=["food-com"]),
            OutOfDistributionRemover(),
            First(50000),
            Fork("2",
                 steps=[
                     Pipeline("vec2sum",
                              steps=[
                                  PDReduce("ingredients"),
                                  IterableApply(IterableApply(Lower())),
                                  PhraserStep(),
                                  Fork("3", steps=[
                                      W2VStep(8),
                                      Pass(),
                                  ]),
                                  VectorizeAndSum(),
                                  Fork("kmeans",
                                       steps=[Pass(),
                                              KMeansClusterer(4)]),
                                  ZipList()
                              ],
                              verbosity=True),
                     Pipeline("name", steps=[PDReduce("name")], verbosity=True)
                 ]),
            ZipList(),
            #looking for common text
            TransformList(key=lambda x: x[0][1], value=lambda x: x[1]),
            IterableApply(
                Pipeline("per cluster",
                         steps=[
                             IterableApply(Pipeline(
                                 "cleanup",
                                 steps=[SpacyStep(),
                                        StopWordsRemoval()]),
                                           verbosity=True),
                             Flatten(),
                             IterableApply(Lambda(lambda x: x.text)),
                             MostCommonCounter(),
                             Lambda(lambda m: m.most_common(5))
                         ]))
        ],
        verbosity=True)
    return p.process(True)


def pipeline6():
    p = Pipeline(
        "word2vecSum",
        steps=[
            DataSetSource(datasets=["recipenlg"]),
            OutOfDistributionRemover(),
            First(50000),
            Fork("recept",
                 steps=[
                     Pipeline("2",
                              steps=[
                                  Fork("ingredientmapping",
                                       steps=[
                                           Pipeline(
                                               "zutaten zerstoeren",
                                               steps=[
                                                   PDReduce("ingredients"),
                                                   IterableApply(
                                                       IterableApply(Lower())),
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
                                  IngredientsPerStepsOccurrence(),
                                  Fork("kmeans",
                                       steps=[Pass(),
                                              KMeansClusterer(4)]),
                                  ZipList()
                              ]),
                     PDReduce("name")
                 ]),
            ZipList(),
            # now we group them
            TransformList(key=lambda x: x[0][1], value=lambda x: x[1]),
            IterableApply(
                Pipeline("per cluster",
                         steps=[
                             IterableApply(Pipeline(
                                 "cleanup",
                                 steps=[SpacyStep(),
                                        StopWordsRemoval()]),
                                           verbosity=True),
                             Flatten(),
                             IterableApply(Lambda(lambda x: x.text)),
                             MostCommonCounter(),
                             Lambda(lambda m: m.most_common(5))
                         ]))
        ],
        verbosity=True)
    return p.process(True)


if __name__ == "__main__":
    '''
    Gets ingredients of whats cooking and recipenlg datasets and dumps them into json files.
    Does the same with the combined list from both datasets.
    '''
    #pipeline6()