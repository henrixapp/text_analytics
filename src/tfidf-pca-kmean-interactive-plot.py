from dataloader.dataloader import DataLoader
from pipeline.pipeline import Fork, Pipeline
from pipeline.data_access import DataSetSource, PDReduce
from pipeline.generics import IterableApply, Lambda, PDSample
from pipeline.preprocessing import AlphaNumericalizer, Dropper, Lower, NLTKPorterStemmer, OutOfDistributionRemover, Replacer, Split, StopWordsRemoval
from visualization.interactive import Tooltipped2DScatterPlot
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from nltk.corpus import stopwords
from sklearn.decomposition import PCA
from sklearn.cluster import KMeans


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
    return p.process(True)


data, header = pipeline()
names, steps = data

vectorizer = TfidfVectorizer(min_df=10)
tfidf = vectorizer.fit_transform(steps)
terms = vectorizer.get_feature_names()
print(terms)
print(tfidf.shape)

highest_indices = tfidf.todense().argsort(axis=1)[:3]
extras = [
    " ".join([terms[index] for index in recipe.tolist()[0]])
    for recipe in highest_indices.T
]

pca = PCA(n_components=2)
reduced_data = pca.fit_transform(tfidf.todense())
data = reduced_data.T

kmeans = KMeans(init='k-means++', n_clusters=10, n_init=10)
kmeans.fit(reduced_data)
classes = kmeans.predict(reduced_data)

labels = list(names)
class_colors = np.array(["red", "green", "blue", "yellow", "brown"] * 2)
plot = Tooltipped2DScatterPlot(data, labels, class_colors[classes],
                               "Recipe Clusters", extras)
plot.plot()