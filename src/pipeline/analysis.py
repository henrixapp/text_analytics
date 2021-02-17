from pipeline.pipeline import PipelineStep, Head
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.feature_extraction.text import TfidfTransformer
import numpy as np

from gensim.models.phrases import Phrases, Phraser
from gensim.models import Word2Vec

import numpy as np

from sklearn.cluster import KMeans
from sklearn.neighbors import NearestCentroid

def hash(astring):
    return ord(astring[0])


class TFIDFStep(PipelineStep):
    """
    TODO Which data preprocessing has to be done before?
    """
    def __init__(self):
        super().__init__("tfidf")

    def process(self, data, head=Head()):
        transformer = TfidfTransformer().fit_transform(data)
        head.addInfo("tfidf")
        tfidf = np.mean(
            transformer, axis=0
        )  ### Don't forget that you need the tfidf values for a single word averaged across documents ####
        return tfidf, head


class PhraserStep(PipelineStep):
    """
    Generates a phrased version of the inputted text., input is flattened
    expects str step data [[str]]
    """
    def __init__(self, min_count=5):
        super().__init__("phraser")
        self._mincount = min_count

    def process(self, data, head=Head()):
        head.addInfo(self.name, str(self._mincount))
        new_lines = [[w for w in sent] for sent in data]
        phrases = Phrases(new_lines, min_count=self._mincount)
        return [phrases[[w for w in sent]] for sent in data], head


from gensim.models.callbacks import CallbackAny2Vec


# taken from https://stackoverflow.com/questions/54422810/tracking-loss-and-embeddings-in-gensim-word2vec-model
class MonitorCallback(CallbackAny2Vec):
    def __init__(self, test_words):
        self._test_words = test_words

    def on_epoch_end(self, model):
        print("Model loss:", model.get_latest_training_loss())  # print loss


monitor = MonitorCallback(["word", "I", "less"])  # monitor with demo words


class W2VStep(PipelineStep):
    """
    This step returns a W2V instance of the inputed data
    """
    def __init__(self, workers, dim=30):
        super().__init__("w2v")
        self._workers = workers
        self._size = dim

    def process(self, data, head=Head()):
        head.addInfo(self.name, "")
        w2v = Word2Vec(
            data,
            #hashfxn=hash,
            workers=self._workers,
            size=self._size,
            negative=20,
            min_count=5,
            window=10,
            sample=6e-5,
            alpha=0.03,
            min_alpha=0.0001,
            iter=0  # in newer versions the iter keyword changed to epoch
        )
        w2v.build_vocab(data,
                        update=True)  ### your code ### # maybe use vocab here?
        w2v.train(data,
                  total_examples=w2v.corpus_count,
                  epochs=100,
                  callbacks=[monitor])
        w2v.init_sims(replace=True)
        return w2v, head


class VectorizeAndSum(PipelineStep):
    """
    Custom install
    """
    def __init__(self):
        super().__init__("vectorize")

    def process(self, data, head=Head()):
        head.addInfo(self.name, "")
        dim = len(data[0].wv[list(data[0].wv.vocab.keys())[0]])
        return [
            x if x.ndim > 0 else np.zeros(dim) for x in [
                np.sum([
                    data[0].wv[w]
                    for w in words if w in data[0].wv.vocab.keys()
                ],
                       axis=0) for words in data[1]
            ]
        ], head


class KMeansClusterer(PipelineStep):
    """
    Clusters the given Data in K sects.
    Returns 
    """
    def __init__(self, k):
        self._k = k
        super().__init__("kmeans")

    def process(self, data, head=Head()):
        head.addInfo(self.name, str(self._k))
        kmeans = KMeans(n_clusters=self._k,
                        random_state=0).fit(np.stack(data, axis=0))
        return kmeans.labels_, head


class IngredientsPerStepsOccurrence(PipelineStep):
    """
    In this step we compute the first occurrence of an ingredient in all steps of a recipe. This should incorporate the factor that we mean it is irrelevant when special ingredients are added to a recipe, it is more important which ingredients are added first.
    """
    def __init__(self,
                 activation_function=lambda x: 1 - x
                 ):  #-np.log(2 - x) is also a try worth
        self.activation_function = activation_function
        super().__init__("IngredientsPerStepsOccurrence")

    def process(self, data, head=Head()):
        head.addInfo(self.name, "")
        ingredients_per_recipe = data[0][1]
        word2vec = data[0][0]
        steps_per_recipe = data[1]
        recipe_ingredients = []

        for i, ingredients in enumerate(ingredients_per_recipe):
            steps = steps_per_recipe[i]
            ingredients_per_recipe_occurrence = []
            for ingredient in ingredients:
                found = False
                for j, step in enumerate(steps):
                    if ingredient in step:
                        found = True
                        ingredients_per_recipe_occurrence.append(
                            float(j + 1) / len(steps))
                        break
                if not found:
                    ingredients_per_recipe_occurrence.append(0)
            recipe_ingredients += [ingredients_per_recipe_occurrence]

        dim = len(word2vec.wv[list(word2vec.wv.vocab.keys())[0]])
        result = [
            x if x.ndim > 0 else np.zeros(dim) for x in [
                np.sum([
                    word2vec.wv[w] *
                    self.activation_function(recipe_ingredients[j][i])
                    for i, w in enumerate(words)
                    if w in word2vec.wv.vocab.keys()
                ],
                       axis=0)
                for j, words in enumerate(ingredients_per_recipe)
            ]
        ]

        return result, head


class IngredientsPerStepsOccurrenceBySimilarity(PipelineStep):
    """
    In this step we compute the first occurrence of an ingredient in all steps of a recipe by similarity score. This should incorporate the factor that we mean it is irrelevant when special ingredients are added to a recipe, it is more important which ingredients are added first.
    """
    def __init__(self,
                 activation_function=lambda x: 1 - x
                 ):  #-np.log(2 - x) is also a try worth
        self.activation_function = activation_function
        super().__init__("IngredientsPerStepsOccurrenceBySimilarity")

    def process(self, data, head=Head()):
        head.addInfo(self.name, "")
        ingredients_per_recipe = data[0][1]
        word2vec = data[0][0]
        steps_per_recipe = data[1]
        recipe_ingredients = []

        for i, ingredients in enumerate(ingredients_per_recipe):
            steps = steps_per_recipe[i]
            ingredients_per_recipe_occurrence = []
            for ingredient in ingredients:
                score = 0
                step_j = 0
                for j, step in enumerate(steps):
                    if ingredient in word2vec.wv.vocab.keys():
                        for word in step:
                            if word in word2vec.wv.vocab.keys(
                            ) and word2vec.wv.similarity(ingredient,
                                                         word) > score:
                                step_j = j
                                score = word2vec.wv.similarity(
                                    ingredient, word)
                ingredients_per_recipe_occurrence.append(
                    float(step_j + 1) / len(steps))
            recipe_ingredients += [ingredients_per_recipe_occurrence]

        dim = len(word2vec.wv[list(word2vec.wv.vocab.keys())[0]])
        result = [
            x if x.ndim > 0 else np.zeros(dim) for x in [
                np.sum([
                    word2vec.wv[w] *
                    self.activation_function(recipe_ingredients[j][i])
                    for i, w in enumerate(words)
                    if w in word2vec.wv.vocab.keys()
                ],
                       axis=0)
                for j, words in enumerate(ingredients_per_recipe)
            ]
        ]

        return result, head

class CuisineNearestCentroid(PipelineStep):
    """
    Classification using scikit-learn implementation of NearestCentroid.

    Input: Training-Test Split of (w2v, cuisine (onehot, encode), names)
    Output: Data-Tuple constisting of:
                NCclf: Trained NearestCentroid Classifier
                acc: Accuracy on the test set
                test_clf: predicted classes of test_set
                test_onehot: ground_truth classes of test_set
                test_encode: Encoding vector to names
                test_names: Names of cuisines
    """
    def __init__(self):
        super().__init__("CuisineNearestCentroid")

    def process(self, data, head=Head()):
        head.addInfo(self.name, "cuisineNearestCentroid")

        NCclf = NearestCentroid()

        training, test = data
        training_w2v, training_cuisine, training_name = training
        training_w2v = np.array(training_w2v)
        training_onehot, training_encode = training_cuisine
        training_onehot = np.array(training_onehot)
        test_w2v, test_cuisine, test_name = test
        test_w2v = np.array(test_w2v)
        test_onehot, test_encode = test_cuisine
        test_onehot = np.array(test_onehot)

        assert (training_encode == test_encode).all(), "Something went wrong in a step before. Encoding vectores are not the same!"

        NCclf.fit(training_w2v, training_onehot)

        test_clf = NCclf.predict(test_w2v)

        acc = np.sum(test_clf == test_onehot)/len(test_clf)
        print(f"With {len(training_encode)} different cuisines NearestCentroid gets an accuray of {acc*100}% on the test set.")

        data = (NCclf, acc, test_clf, test_onehot, test_encode, test_name)

        return data, head