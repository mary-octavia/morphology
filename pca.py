# -*- coding: utf-8 -*-
"""
Runs some simple unsupervised visualisation tricks
on the corpus of romanian infinitives. For now, we
do PCA and NMF, with different settings.
Created on Tue Apr 12 19:02:07 2011
Largest values in the first PC correspond to:

"""
import re
import string
import random
import codecs
import numpy as np

import matplotlib.pyplot as pl
import mpl_toolkits.mplot3d.axes3d as p3
from scipy.sparse import vstack
from time import time
from sklearn import metrics
from itertools import cycle
from sklearn.cluster import AffinityPropagation
from sklearn.decomposition import RandomizedPCA, SparsePCA, NMF, PCA, TruncatedSVD
from sklearn.cluster import KMeans, AffinityPropagation, AgglomerativeClustering
from sklearn.neighbors import KNeighborsClassifier
from sklearn.feature_extraction.text import CountVectorizer, TfidfVectorizer
from sklearn.pipeline import Pipeline, make_pipeline
from sklearn.preprocessing import scale, Binarizer, Normalizer
from sklearn.pipeline import Pipeline
from sklearn import naive_bayes
from sklearn.metrics import classification_report, accuracy_score, recall_score, precision_score, f1_score
from sklearn.cross_validation import KFold, LeaveOneOut, StratifiedKFold
from sklearn.grid_search import GridSearchCV
from sklearn.svm import LinearSVC
from sklearn.dummy import DummyClassifier

def get_preprocessor(suffix=''):
    def preprocess(unicode_text):
        return unicode(unicode_text.strip().lower() + suffix)
    return preprocess

def load_data(filename='subst-all_labeled_8forms.csv', labels=False):
    infinitives, y = [], []
    with codecs.open(filename, 'r', encoding='utf-8') as f:
        for line in f:
            if labels:
                inf, label = line.split("\t")
            else:
                inf = line
            infinitives.append(inf)
            if labels:
                y.append(int(label))
    infinitives = list(set(infinitives))
    infinitives, y = np.array(infinitives), np.array(y, dtype=np.int)
    if labels:
        return infinitives, y
    else:
        return infinitives   


def extract_features(words, n, count=False):
    vectorizer = CountVectorizer(analyzer='char', ngram_range=(n, n), binary=count, preprocessor=get_preprocessor('$'))

    transformed_words = vectorizer.fit_transform(words).toarray()
    transformed_words = np.array(transformed_words, dtype=np.float)
    # if not count:
    #     transformed_words[transformed_words > 0] = 1.0
    return transformed_words, vectorizer 


def plot_projection(model, infinitives, title, labels, ngram=5):
    fig = pl.figure()
    # Binary model: n-gram appears or not
    for i in range(1, ngram):  # n-gram length (1 to 3)    
        pl.subplot(2, 2, i)
        data, _ = extract_features(infinitives, i, False)
        projected_data = model.fit(data).transform(data)
        pl.scatter(projected_data[:, 0], projected_data[:, 1], c=labels)
        pl.title('Binary %d-grams' % i)
    # pl.show()
    pl.savefig("rpca_binary_1-"+str(ngram-1)+"gram-wsuffix.png", format='png', dpi=300)
    # Frequency model: count the occurences
    for i in range(1, ngram):
        pl.subplot(2, 2, i)
        data, _ = extract_features(infinitives, i, True)
        projected_data = model.fit(data).transform(data)
        pl.scatter(projected_data[:, 0], projected_data[:, 1], c=labels)
        pl.title('Count %d-grams' % i)
    fig.text(.5, .95, title, horizontalalignment='center')
    # fig.legend("la", "lala", "lalala")
    print "lala"
    # pl.show()
    pl.savefig("rpca_count_1-"+str(ngram-1)+"gram-wsuffix.png", format='png', dpi=300)


def k_clusters(nclust, infinitives):
    data, _ = extract_features(infinitives, 3, False)
    kmeans = KMeans(n_clusters=nclust).fit(data)
    f = codecs.open("clusters.txt", "w", encoding="utf-8")
    print kmeans.inertia_
    nn = KNeighborsClassifier(1).fit(data, np.zeros(data.shape[0]))
    _, idx = nn.kneighbors(kmeans.cluster_centers_)
    for inf in infinitives[idx.flatten()]:
        f.write(inf+"\n")
    f.close()

def affinity(infinitives, y):
    print "Extracting features..."
    X, _= extract_features(infinitives, 3, False)
    X_norms = np.sum(X * X, axis=1)
    S = -X_norms[:, np.newaxis] - X_norms[np.newaxis, :] + 2 * np.dot(X, X.T)
    p = 10 * np.median(S)
    print "Fitting affinity propagation clustering..."
    af = AffinityPropagation().fit(S, p)
    indices = af.cluster_centers_indices_
    for i, idx in enumerate(indices):
        print i, infinitives[idx].encode("utf8")

    n_clusters_ = len(indices)

    print "Fitting PCA..."
    X = RandomizedPCA(2).fit(X).transform(X)    
    
    print "Plotting..."
    pl.figure(1)
    pl.clf()
    
    colors = cycle('bgrcmyk')
    for k, col in zip(range(n_clusters_), colors):
        class_members = af.labels_ == k
        cluster_center = X[indices[k]]
        pl.plot(X[class_members,0], X[class_members,1], col+'.')
        pl.plot(cluster_center[0], cluster_center[1], 'o', markerfacecolor=col,
                                         markeredgecolor='k', markersize=14)
        for x in X[class_members]:
            pl.plot([cluster_center[0], x[0]], [cluster_center[1], x[1]], col) 

    pl.title('Estimated number of clusters: %d' % n_clusters_)
    # pl.show()
    pl.savefig("affinity_clusters_"+"20000"+"4gram.png", format='png', dpi=300)

def print_results_to_file(estimator, name, labels):
    f = codecs.open("kmeanscores.txt", "w", encoding="utf-8")
    f.write('init    inertia    homo   compl  v-means     ARI AMI')
    f.write("\n")
    f.write(name + " ")
    f.write(str(estimator.inertia_) +" ")
    f.write(str(metrics.homogeneity_score(labels, estimator.labels_))+" ")
    f.write(str(metrics.completeness_score(labels, estimator.labels_))+ " ")
    f.write(str(metrics.v_measure_score(labels, estimator.labels_))+ " ")
    f.write(str(metrics.adjusted_rand_score(labels, estimator.labels_))+ " ")
    f.write(str(metrics.adjusted_mutual_info_score(labels,  estimator.labels_))+ " ")
    f.close()

def visualize_kclusters(data, n_labels, labels):
    # Visualize the results on PCA-reduced data
    # reduced_data = PCA(n_components=2).fit_transform(data)
    # pca = PCA(n_components=2).fit(data)
    # reduced_data = pca.transform(data)
    # reduced_data = data #for legacy reasons
    svd = TruncatedSVD(2)
    normalizer = Normalizer(copy=False)
    lsa = make_pipeline(svd, normalizer)
    # lsa = Pipeline([('svd',svd),('normalizer',normalizer)])
    reduced_data = lsa.fit_transform(data)
    
    kmeans = KMeans(init='k-means++', n_clusters=n_labels, n_init=1)
    kmeans.fit(reduced_data)

    print_results_to_file(kmeans, "k-means++", labels)

    # Step size of the mesh. Decrease to increase the quality of the VQ.
    h = .004     # point in the mesh [x_min, m_max]x[y_min, y_max].

    # Plot the decision boundary. For that, we will assign a color to each
    x_min, x_max = reduced_data[:, 0].min() - 1, reduced_data[:, 0].max() + 1
    y_min, y_max = reduced_data[:, 1].min() - 1, reduced_data[:, 1].max() + 1
    xx, yy = np.meshgrid(np.arange(x_min, x_max, h), np.arange(y_min, y_max, h))
    # print "xx: ", xx, "yy:", yy

    # Obtain labels for each point in mesh. Use last trained model.
    Z = kmeans.predict(np.c_[xx.ravel(), yy.ravel()])

    # Put the result into a color plot
    Z = Z.reshape(xx.shape)
    plt.figure(1)
    plt.clf()
    plt.imshow(Z, interpolation='nearest',
               extent=(xx.min(), xx.max(), yy.min(), yy.max()),
               cmap=plt.cm.Pastel1,
               aspect='auto', origin='lower')

    plt.scatter(reduced_data[:, 0], reduced_data[:, 1], c=labels)
    # Plot the centroids as a blue X
    centroids = kmeans.cluster_centers_
    plt.scatter(centroids[:, 0], centroids[:, 1],
                marker='x', s=169, linewidths=3,
                color='w', zorder=10)

    # plt.title('K-means clustering on all the articles (PCA-reduced data)\n'
    #           'Centroids are marked with white cross')
    plt.title('K-means clustering on all the nouns (PCA-reduced data)\n'
              'Centroids are marked with white cross')
    plt.xlim(x_min, x_max)
    plt.ylim(y_min, y_max)
    plt.xticks(())
    plt.yticks(())
    # plt.show()
    # plt.legend()
    plt.savefig("kmeans3.png")
    return kmeans, reduced_data

if __name__ == '__main__':
    fin='subst_all-labeled_8forms.txt'
    infinitives, y= load_data(fin, True)
    X, _= extract_features(infinitives, 4, False)

    affinity(infinitives[:20000], y)    
    # plot_projection(RandomizedPCA(n_components=2), infinitives, "RandomizedPCA projection of uninflected nouns", y)
    # plot_projection(PCA(n_components=2), infinitives, "PCA projection of uninflected nouns", y)
    # plot_projection(NMF(n_components=2, tol=0.01, init="nndsvda"), infinitives,"NMF projection of infinitives")
    # k_clusters(10, infinitives)
    # visualize_kclusters(X, len(y), y)

    # print infinitives[0]
    # data, vect = extract_features(infinitives, 2, True)
    # print vect.vocabulary.keys()
    # for token, idx in vect.vocabulary.items():
    #     if idx in data[0].nonzero()[0]:
    #         print token