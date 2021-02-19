from dataloader.dataloader import DataLoader
from pipeline.data_access import DataSetSource, PDReduce
from pipeline.generics import IterableApply, Lambda, PDSample
from pipeline.pipeline import Fork, Pipeline
from pipeline.preprocessing import AlphaNumericalizer, Dropper, Lower, NLTKPorterStemmer, OutOfDistributionRemover, Replacer, Split, StopWordsRemoval
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.cluster import DBSCAN, OPTICS, SpectralClustering, KMeans
from sklearn.decomposition import PCA
from nltk.corpus import stopwords
import matplotlib.colors as mcolors
from visualization.interactive import Tooltipped2DScatterPlot
import numpy as np


def pipeline():
    p = Pipeline(
        "basline",
        steps=[
            DataSetSource(datasets=[DataLoader.EPIRECIPES]),
            Dropper(columns_causing_drop=['steps']),
            OutOfDistributionRemover(),
            PDSample(2000),
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
                                                            'english') +
                                                        [
                                                            'minut', 'add',
                                                            'heat', 'pepper',
                                                            'ingredi',
                                                            'combin', 'salt',
                                                            'stir', 'cook',
                                                            'tablespoon',
                                                            'larg', 'cup',
                                                            'transfer', 'cut'
                                                        ]),
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


def kmeans(tfidf, names, terms):
    kmeans_clustering = KMeans(n_clusters=6).fit(tfidf)
    labels = kmeans_clustering.labels_

    top_terms_per_cluster(terms, tfidf.todense(), labels)
    plot_clusters_in_2D(tfidf, names, labels)


def dbscan(tfidf, names, terms):
    db_clustering = DBSCAN(eps=.5, min_samples=2).fit(tfidf)
    labels = db_clustering.labels_

    plot_clusters_in_2D(tfidf, names, labels)


def optics(tfidf, names, terms):
    optics_clustering = OPTICS(min_samples=2).fit(tfidf.todense())
    labels = optics_clustering.labels_

    plot_clusters_in_2D(tfidf, names, labels)


def spectral(tfidf, names, terms):
    spectral_clustering = SpectralClustering(
        n_clusters=10, n_components=20).fit(tfidf.todense())
    labels = spectral_clustering.labels_

    top_terms_per_cluster(terms, tfidf.todense(), labels)
    plot_clusters_in_2D(tfidf, names, labels)


def plot_clusters_in_2D(tfidf, names, labels):
    pca = PCA(n_components=2)
    reduced_data = pca.fit_transform(tfidf.todense())
    data = reduced_data.T

    color_list = list(mcolors.XKCD_COLORS)
    colors = [color_list[label] for label in labels]

    plot = Tooltipped2DScatterPlot(data, list(names), colors)
    plot.plot()


def top_terms_per_cluster(terms, tfidf, labels, top_n=10):
    # tfidf must be dense
    # for each cluser compute 5 highest tfidf scores after sum and normalization
    for clusterid in list(set(labels)):
        cluster_indices = np.argwhere(labels == clusterid)
        tfidf_per_cluster = np.sum(
            tfidf[cluster_indices],
            axis=0) / cluster_indices.shape[0]  #normalise
        top_term_indices = np.asarray(
            tfidf_per_cluster)[0].argsort()[-top_n:][::-1]
        print([terms[id] for id in top_term_indices])


def main():
    '''
    Implements a very basic baseline approach which can be used to compare more sophisticated approaches to.
    Uses ... dataset, does pre-processing and computes TF-IDF features which are then used by ... clustering algorithm.
    '''
    data, _ = pipeline()
    names, steps = data

    vectorizer = TfidfVectorizer(min_df=5)
    tfidf = vectorizer.fit_transform(steps)
    terms = vectorizer.get_feature_names()
    print(terms)
    print(tfidf.shape)

    kmeans(tfidf, names, terms)


if __name__ == "__main__":
    # print(type(stopwords.words('english') + ['tom']))
    main()