import numpy as np
import matplotlib.pyplot as plt
#%matplotlib inline
import seaborn as sns
import sys
from sklearn.manifold import TSNE
from sklearn.cluster import KMeans

import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import pandas as pd
import matplotlib.colors as mcolors


def tsneplot(model, word):
    """ Plot in seaborn the results from the t-SNE dimensionality reduction for the top 10 most similar and dissimilar words
    """
    #embs = np.empty((0, 100), dtype='f')# to save all the embeddings
    word_labels = [word]
    color_list = ['green']

    embs = np.array([model.wv[word]])  # adds the vector of the query word

    close_words = model.wv.most_similar(
        word)  # gets list of most similar words
    far_words = model.wv.similar_by_word(
        word, topn=15000, restrict_vocab=15000)[-10:]  #TODO check this line

    # adds the vector for each of the closest words to the array
    for wrd_score in close_words:
        #print(wrd_score)
        wrd_vector = model.wv[wrd_score[0]]  #get the vector
        word_labels.append(wrd_score[0])
        color_list.append('blue')
        embs = np.append(embs, [wrd_vector], axis=0)

    # adds the vector for each of the furthest words to the array
    for wrd_score in far_words:
        wrd_vector = model.wv[wrd_score[0]]  #get the vector
        word_labels.append(wrd_score[0])
        color_list.append('red')
        embs = np.append(embs, [wrd_vector], axis=0)

    np.set_printoptions(suppress=True)
    Y = TSNE(n_components=2, random_state=42, perplexity=15).fit_transform(
        embs)  # with  n_components=2, random_state=42, perplexity=15

    # Sets everything up to plot
    df = pd.DataFrame({
        'x': [x for x in Y[:, 0]],
        'y': [y for y in Y[:, 1]],
        'words': word_labels,
        'color': color_list
    })

    fig, _ = plt.subplots()
    fig.set_size_inches(10, 10)

    # Basic plot
    p1 = sns.regplot(data=df,
                     x="x",
                     y="y",
                     fit_reg=False,
                     marker="o",
                     scatter_kws={
                         's': 40,
                         'facecolors': df['color']
                     })

    # adds annotations one by one with a loop
    for line in range(0, df.shape[0]):
        p1.text(df["x"][line],
                df['y'][line],
                '  ' + df["words"][line].title(),
                horizontalalignment='left',
                verticalalignment='bottom',
                size='medium',
                color=df['color'][line],
                weight='normal').set_size(15)

    plt.xlim(Y[:, 0].min() - 50, Y[:, 0].max() + 50)
    plt.ylim(Y[:, 1].min() - 50, Y[:, 1].max() + 50)

    plt.title('t-SNE visualization for {}'.format(word.title()))


def tsne3d(model, word):
    fig = plt.figure()
    ax = fig.add_subplot(111, projection='3d')
    """ Plot in seaborn the results from the t-SNE dimensionality reduction for the top 10 most similar and dissimilar words
    """
    #embs = np.empty((0, 100), dtype='f')# to save all the embeddings
    word_labels = [word]
    color_list = ['green']

    embs = np.array([model.wv[word]])  # adds the vector of the query word

    close_words = model.wv.most_similar(
        word)  # gets list of most similar words
    far_words = model.wv.similar_by_word(
        word, topn=15000, restrict_vocab=15000)[-10:]  #TODO check this line

    # adds the vector for each of the closest words to the array
    for wrd_score in close_words:
        #print(wrd_score)
        wrd_vector = model.wv[wrd_score[0]]  #get the vector
        word_labels.append(wrd_score[0])
        color_list.append('blue')
        embs = np.append(embs, [wrd_vector], axis=0)

    # adds the vector for each of the furthest words to the array
    for wrd_score in far_words:
        wrd_vector = model.wv[wrd_score[0]]  #get the vector
        word_labels.append(wrd_score[0])
        color_list.append('red')
        embs = np.append(embs, [wrd_vector], axis=0)

    np.set_printoptions(suppress=True)
    Y = TSNE(n_components=3, random_state=42, perplexity=15).fit_transform(
        embs)  # with  n_components=2, random_state=42, perplexity=15

    # Sets everything up to plot
    xs = [x for x in Y[:, 0]]
    ys = [y for y in Y[:, 1]]
    zs = [y for y in Y[:, 2]]

    ax.scatter(xs, ys, zs)


def tsneplot_words(data):
    """ Plot in seaborn the results from the t-SNE dimensionality reduction for the top 10 most similar and dissimilar words
    """
    embs = np.empty((0, 30), dtype='f')  # to save all the embeddings
    word_labels = []
    color_list = []
    for vec, w in data:
        if vec.ndim > 0:
            word_labels += [w]
            color_list += ["green"]
            embs = np.append(embs, [vec], axis=0)
    # embs = np.array([model.wv[word] for  word in words]) # adds the vector of the query word

    # close_words = model.wv.most_similar(word) # gets list of most similar words
    # far_words = model.wv.similar_by_word(word,topn=15000,restrict_vocab=15000)[-10:] #TODO check this line

    # # adds the vector for each of the closest words to the array
    # for wrd_score in close_words:
    #     #print(wrd_score)
    #     wrd_vector =  model.wv[wrd_score[0]]#get the vector
    #     word_labels.append(wrd_score[0])
    #     color_list.append('blue')
    #     embs = np.append(embs, [wrd_vector], axis=0)

    # # adds the vector for each of the furthest words to the array
    # for wrd_score in far_words:
    #     wrd_vector = model.wv[wrd_score[0]] #get the vector
    #     word_labels.append(wrd_score[0])
    #     color_list.append('red')
    #     embs = np.append(embs, [wrd_vector], axis=0)

    np.set_printoptions(suppress=True)
    Y = TSNE(n_components=2, random_state=42, perplexity=30,
             n_iter=5000).fit_transform(
                 embs)  # with  n_components=2, random_state=42, perplexity=15
    kmeans = KMeans(n_clusters=20, random_state=0).fit(Y[:])
    # Sets everything up to plot
    df = pd.DataFrame({
        'x': [x for x in Y[:, 0]],
        'y': [y for y in Y[:, 1]],
        'words':
        word_labels,
        'color': [list(mcolors.XKCD_COLORS)[i] for i in kmeans.labels_]
    })

    fig, _ = plt.subplots()
    fig.set_size_inches(10, 10)

    # Basic plot
    p1 = sns.regplot(data=df,
                     x="x",
                     y="y",
                     fit_reg=False,
                     marker="o",
                     scatter_kws={
                         's': 40,
                         'facecolors': df['color']
                     })

    # adds annotations one by one with a loop
    for line in range(0, df.shape[0]):
        p1.text(df["x"][line],
                df['y'][line],
                '  ' + df["words"][line].title(),
                horizontalalignment='left',
                verticalalignment='bottom',
                size='medium',
                color=df['color'][line],
                weight='normal').set_size(15)

    plt.xlim(Y[:, 0].min() - 50, Y[:, 0].max() + 50)
    plt.ylim(Y[:, 1].min() - 50, Y[:, 1].max() + 50)

    plt.title('t-SNE visualization for {}'.format(str(50)))
    return kmeans, Y


def tsneplot_words2(data):
    """ Plot in seaborn the results from the t-SNE dimensionality reduction for the top 10 most similar and dissimilar words
    """
    embs = np.empty((0, 30), dtype='f')  # to save all the embeddings
    word_labels = []
    color_list = []
    for (vec, color), w in data:
        if vec.ndim > 0:
            word_labels += [w]
            color_list += [list(mcolors.XKCD_COLORS)[color]]
            embs = np.append(embs, [vec], axis=0)
    # embs = np.array([model.wv[word] for  word in words]) # adds the vector of the query word

    # close_words = model.wv.most_similar(word) # gets list of most similar words
    # far_words = model.wv.similar_by_word(word,topn=15000,restrict_vocab=15000)[-10:] #TODO check this line

    # # adds the vector for each of the closest words to the array
    # for wrd_score in close_words:
    #     #print(wrd_score)
    #     wrd_vector =  model.wv[wrd_score[0]]#get the vector
    #     word_labels.append(wrd_score[0])
    #     color_list.append('blue')
    #     embs = np.append(embs, [wrd_vector], axis=0)

    # # adds the vector for each of the furthest words to the array
    # for wrd_score in far_words:
    #     wrd_vector = model.wv[wrd_score[0]] #get the vector
    #     word_labels.append(wrd_score[0])
    #     color_list.append('red')
    #     embs = np.append(embs, [wrd_vector], axis=0)

    np.set_printoptions(suppress=True)
    Y = TSNE(n_components=2, random_state=42, perplexity=30,
             n_iter=5000).fit_transform(
                 embs)  # with  n_components=2, random_state=42, perplexity=15
    kmeans = KMeans(n_clusters=8, random_state=0).fit(Y[:])
    # Sets everything up to plot
    df = pd.DataFrame({
        'x': [x for x in Y[:, 0]],
        'y': [y for y in Y[:, 1]],
        'words':
        word_labels,
        'color':
        color_list,
        'color2': [list(mcolors.XKCD_COLORS)[i] for i in kmeans.labels_]
    })

    fig, _ = plt.subplots()
    fig.set_size_inches(10, 10)

    # Basic plot
    # p1 = sns.regplot(data=df,
    #                  x="x",
    #                  y="y",
    #                  fit_reg=False,
    #                  marker="o",
    #                  scatter_kws={
    #                      's': 40,
    #                      'facecolors': df['color']
    #                  })
    p1 = sns.regplot(data=df[df['color'] == df['color2']],
                     x="x",
                     y="y",
                     fit_reg=False,
                     marker="x",
                     scatter_kws={
                         's': 40,
                         'facecolors': df[df['color'] == df['color2']]['color']
                     })
    # adds annotations one by one with a loop
    for line in range(0, df.shape[0]):
        p1.text(df["x"][line],
                df['y'][line],
                '  ' + df["words"][line].title(),
                horizontalalignment='left',
                verticalalignment='bottom',
                size='medium',
                color=df['color'][line],
                weight='normal').set_size(15)

    plt.xlim(Y[:, 0].min() - 50, Y[:, 0].max() + 50)
    plt.ylim(Y[:, 1].min() - 50, Y[:, 1].max() + 50)

    plt.title('t-SNE visualization for {}'.format(str(50)))
    return kmeans, Y