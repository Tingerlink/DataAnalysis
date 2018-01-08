from sklearn.naive_bayes import GaussianNB
from sklearn import svm
from sklearn import neighbors
from sklearn.tree import DecisionTreeClassifier

import numpy as np


def naive_bayes_classifier(learn_set, test_set):
    clf = GaussianNB()

    learn_output = []
    for row in learn_set[1]:
        output_row = []
        for cell in row:
            output_row.append(unicode(cell))
        learn_output.append(output_row)

    clf.fit(learn_set[0], np.ravel(learn_output))

    output_vector = []

    for row in test_set[0]:
        t = [clf.predict([row])[0]]
        output_vector.append(t)

    count_true = 0
    for i in range(0, len(learn_set[0])):
        if clf.predict([learn_set[0][i]]) == learn_output[i]:
            count_true += 1

    count_false = len(learn_set[0]) - count_true

    return [output_vector, count_true, count_false]


def SVM(learn_set, test_set):
    output_vector = []

    learn_output = []
    for row in learn_set[1]:
        output_row = []
        for cell in row:
            output_row.append(unicode(cell))
        learn_output.append(output_row)

    C = 1.0  # SVM regularization parameter
    clf = svm.SVC(kernel='poly', degree=3, C=C).fit(learn_set[0], np.ravel(learn_output))

    for row in test_set[0]:
        trr = [clf.predict([row])[0]]
        output_vector.append(trr)

    count_true = 0
    for i in range(0, len(learn_set[0])):
        if clf.predict([learn_set[0][i]]) == learn_output[i]:
            count_true += 1

    count_false = len(learn_set[0]) - count_true

    return [output_vector, count_true, count_false]


def classification_tree(learn_set, test_set):
    output_vector = []

    learn_output = []
    for row in learn_set[1]:
        output_row = []
        for cell in row:
            output_row.append(unicode(cell))
        learn_output.append(output_row)

    clf = DecisionTreeClassifier().fit(learn_set[0], np.ravel(learn_output))

    for row in test_set[0]:
        trr = [clf.predict([row])[0]]
        output_vector.append(trr)

    count_true = 0

    for i in range(0, len(learn_set[0])):
        if clf.predict([learn_set[0][i]]) == learn_output[i]:
            count_true += 1

    count_false = len(learn_set[0]) - count_true

    return [output_vector, count_true, count_false]


def nearest_neighbors_classification(learn_set, test_set):
    output_vector = []

    learn_output = []
    for row in learn_set[1]:
        output_row = []
        for cell in row:
            output_row.append(unicode(cell))
        learn_output.append(output_row)

    n_neighbors = 15

    clf = neighbors.KNeighborsClassifier(n_neighbors, weights='uniform')

    clf.fit(learn_set[0], np.ravel(learn_output))

    for row in test_set[0]:
        trr = [clf.predict([row])[0]]
        output_vector.append(trr)

    count_true = 0
    for i in range(0, len(learn_set[0])):
        if clf.predict([learn_set[0][i]]) == learn_output[i]:
            count_true += 1

    count_false = len(learn_set[0]) - count_true

    return [output_vector, count_true, count_false]
