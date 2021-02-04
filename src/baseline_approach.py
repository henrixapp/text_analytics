from dataloader.dataloader import DataLoader
from pipeline.data_access import DataSetSource, PDReduce
from pipeline.generics import IterableApply, Lambda, PDSample
from pipeline.pipeline import Fork, Pipeline
from pipeline.preprocessing import AlphaNumericalizer, Dropper, Lower, NLTKPorterStemmer, OutOfDistributionRemover, Replacer, Split, StopWordsRemoval
from sklearn.feature_extraction.text import TfidfVectorizer
from nltk.corpus import stopwords
import scipy.cluster.hierarchy as shc
import matplotlib.pyplot as plt


def pipeline():
    p = Pipeline(
        "basline",
        steps=[
            DataSetSource(datasets=[DataLoader.EPIRECIPES]),
            Dropper(columns_causing_drop=['steps']),
            OutOfDistributionRemover(),
            PDSample(200),
            PDReduce(['name', 'steps']),
            Fork(
                "split names and steps",
                steps=[
                    Pipeline("names branch", steps=[PDReduce('name')]),
                    Pipeline(
                        "steps branch",
                        steps=[
                            PDReduce('steps'),
                            IterableApply(
                                Pipeline(
                                    "work on recipes",
                                    steps=[
                                        IterableApply(
                                            Pipeline(
                                                "work on steps",
                                                steps=[
                                                    Lower(),
                                                    Replacer(rules={"\n": ""}),
                                                    Split(rule=" "),
                                                    IterableApply(
                                                        Pipeline(
                                                            "work on words",
                                                            steps=[
                                                                AlphaNumericalizer(
                                                                ),
                                                                NLTKPorterStemmer(
                                                                ),
                                                            ])),
                                                    StopWordsRemoval(
                                                        tooling="nltk",
                                                        additional_stopwords=
                                                        stopwords.words(
                                                            'english')),
                                                    Lambda(
                                                        lambda x: " ".join(x)),
                                                ])),
                                        Lambda(lambda x: " ".join(x)),
                                    ])),
                        ])
                ]),
        ],
        verbosity=True)
    return p.process(
        True)  #set data to true as we provided data with DataSetSource step


def main():
    '''
    Implements a very basic baseline approach which can be used to compare more sophisticated approaches to.
    Uses ... dataset, does pre-processing and computes TF-IDF features which are then used by ... clustering algorithm.
    '''
    data, _ = pipeline()
    names, steps = data

    vectorizer = TfidfVectorizer(min_df=5)
    tfidf = vectorizer.fit_transform(steps)
    print(vectorizer.get_feature_names())
    print(tfidf.shape)

    plt.figure(figsize=(10, 7))
    plt.title("Recipes Dendrogram based on TFIDF")
    dend = shc.dendrogram(shc.linkage(tfidf.todense(), method='ward'),
                          labels=list(names),
                          leaf_font_size=8)

    plt.tight_layout()
    plt.show()


if __name__ == "__main__":
    main()