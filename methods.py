#!-*-coding:utf-8-*-

NAIVE_BAYES = 0
SVM = 1
DECISION_TREE = 2
NEAREST_NEIGHBORS = 3

METHOD_NAMES = [u'Наивный Байесовский классификатор',
                u'Метод опорных векторов',
                u'Дерево решений',
                u'Метод k-ближайших соседей']


def get_method_name_by_id(_id):
    return METHOD_NAMES[_id]
