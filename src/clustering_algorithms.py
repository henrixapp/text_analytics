from dataloader.dataloader import DataLoader
from pipeline.data_access import DataSetSource, PDReduce
from pipeline.generics import IterableApply, Lambda, PDSample
from pipeline.pipeline import Fork, Pipeline
from pipeline.preprocessing import AlphaNumericalizer, Dropper, Lower, NLTKPorterStemmer, OutOfDistributionRemover, Replacer, Split, StopWordsRemoval
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.cluster import DBSCAN, OPTICS, SpectralClustering, KMeans
from sklearn.decomposition import PCA, TruncatedSVD
from sklearn.metrics import silhouette_score, davies_bouldin_score, calinski_harabasz_score
from nltk.corpus import stopwords
from visualization.interactive import Tooltipped2DScatterPlot, TooltippedEmbeddingPlot
import numpy as np
'''
Implements a very basic baseline approach which can be used to compare more sophisticated approaches to.
Uses epirecipes dataset, does pre-processing and computes TF-IDF features which are then used by different clustering algorithms.
Optionally you can perfrom dimensionality reduction using TruncatedSVD and even plot the results interactively.
'''


def pipeline():
    p = Pipeline(
        "basline",
        steps=[
            DataSetSource(datasets=[DataLoader.EPIRECIPES]),
            Dropper(columns_causing_drop=['steps']),
            OutOfDistributionRemover(),
            # PDSample(2000),
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
                                                            'transfer', 'cut',
                                                            'prepar'
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


### Clustering algorithms ###


def kmeans(data):
    kmeans_clustering = KMeans(n_clusters=7).fit(data)
    labels = kmeans_clustering.labels_
    return labels


def dbscan(data):
    db_clustering = DBSCAN(eps=5, min_samples=20).fit(data)
    labels = db_clustering.labels_
    return labels


def optics(data):
    optics_clustering = OPTICS(min_samples=2).fit(data)
    labels = optics_clustering.labels_
    return labels


def spectral(data):
    spectral_clustering = SpectralClustering(n_clusters=7).fit(data)
    labels = spectral_clustering.labels_
    return labels


### plotting functions ###


def plot_clusters_in_2D(data, names, labels):
    # for 2D scatter plots using PCA
    pca = PCA(n_components=2)
    reduced_data = pca.fit_transform(data)

    plot = Tooltipped2DScatterPlot(reduced_data.T, list(names), labels)
    plot.plot()


def plot_clusters_with_embedding(data,
                                 names,
                                 labels,
                                 extras=None,
                                 embedding='UMAP'):
    # for plotting using embeddings (either UMAP or tSNE)

    plot = TooltippedEmbeddingPlot(data, list(names), labels, extras=extras)
    if embedding == 'UMAP':
        plot.plot_UMAP()
    else:
        plot.plot_tSNE()


### evaluation functions ###


def top_terms_per_cluster(terms, tfidf, labels, top_n=10):
    # tfidf must be dense
    # for each cluster compute top_n highest tfidf scores after sum and normalization
    top_terms_lists = []
    for clusterid in list(set(labels)):
        cluster_indices = np.argwhere(labels == clusterid)
        tfidf_per_cluster = np.sum(
            tfidf[cluster_indices],
            axis=0) / cluster_indices.shape[0]  #normalise
        top_term_indices = np.asarray(
            tfidf_per_cluster)[0].argsort()[-top_n:][::-1]
        top_terms_list = [terms[id] for id in top_term_indices]
        # print(top_terms_list)
        top_terms_lists += [", ".join(top_terms_list)]
    return top_terms_lists


def report_metrics(data, labels):
    # reports three metrics which can be computed independent from ground truth labels

    print(f"""
            Clustering Metrics:
            Silhouette score: {silhouette_score(data, labels, metric='euclidean'):.2f}
            Calinski-Harabasz Index: {calinski_harabasz_score(data, labels):.2f}
            Davies-Bouldin Index: {davies_bouldin_score(data, labels):.2f}
        """)


def main():
    data, _ = pipeline()
    names, steps = data

    # TF-IDF Vectorization
    vectorizer = TfidfVectorizer(min_df=5)
    tfidf = vectorizer.fit_transform(steps)
    terms = vectorizer.get_feature_names()
    # print(terms)
    # print(tfidf.shape)
    dense_tfidf = tfidf.todense()
    data = dense_tfidf

    # Dimensionality reduction
    svd = TruncatedSVD(n_components=10, n_iter=7, random_state=42)
    svd.fit(tfidf.T)
    # print(svd.components_.shape)
    data = svd.components_.T

    for clustering_algorithm in [kmeans, optics, spectral]:
        print(str(clustering_algorithm))
        # Clustering
        labels = clustering_algorithm(data)
        # print(labels.shape)
        print(labels)

        # Find top terms per cluster
        #top_terms = top_terms_per_cluster(terms, dense_tfidf, labels)
        # print(top_terms)

        # Plot
        #plot_clusters_with_embedding(data, names, labels, extras=top_terms)

        # Report metrics
        report_metrics(data, labels)


if __name__ == "__main__":
    main()