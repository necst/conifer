# This source file comes from the Conifer open-source project
# (https://github.com/thesps/conifer)

import numpy as np
from .converter import addParentAndDepth, padTree
from ..model import model
from .sklearn_rule_exporter import generateDecisionTree as exportRules
import io


def convert_bdt(bdt, feature_cols):
    ensembleDict = {'max_depth': bdt.max_depth, 'n_trees': bdt.n_estimators,
                    'n_features': bdt.n_features_,
                    'n_classes': bdt.n_classes_, 'trees': [],
                    'init_predict': bdt._raw_predict_init(np.zeros(bdt.n_features_).reshape(1, -1))[0].tolist(),
                    'norm': 1}
    for trees in bdt.estimators_:
        treesl = []
        for tree in trees:
            tree = treeToDict(bdt, tree.tree_)
            tree = padTree(ensembleDict, tree)
            # NB node values are multiplied by the learning rate here, saving work in the FPGA
            tree['value'] = (np.array(tree['value'])[:, 0, 0]
                             * bdt.learning_rate).tolist()
            tree['rules'] = rules
            treesl.append(tree)
        ensembleDict['trees'].append(treesl)

    return ensembleDict


def convert_decision_tree(bdt, feature_cols):
    ensembleDict = {'max_depth': bdt.max_depth, 'n_trees': 1,
                    'n_features': bdt.n_features_,
                    'n_classes': bdt.n_classes_, 'trees': [],
                    'init_predict': [0] * bdt.n_classes_,
                    'norm': 1}

    rules = treeToRules(bdt, feature_cols, bdt.classes_)
    tree = treeToDict(bdt, bdt.tree_)
    tree = padTree(ensembleDict, tree)
    tree['rules'] = rules
    ensembleDict['trees'].append([tree])
    return ensembleDict


def convert_random_forest(bdt, feature_cols):
    ensembleDict = {'max_depth': bdt.max_depth, 'n_trees': bdt.n_estimators,
                    'n_features': bdt.n_features_,
                    'n_classes': bdt.n_classes_, 'trees': [],
                    'init_predict': [0] * bdt.n_classes_,
                    'norm': 1}
    for tree in bdt.estimators_:
        treesl = []
        rules = treeToRules(tree, feature_cols, bdt.classes_)
        tree = treeToDict(bdt, tree.tree_)
        tree = padTree(ensembleDict, tree)
        # Random forest takes the mean prediction, do that here
        # Also need to scale the values by their sum
        v = np.array(tree['value'])
        tree['value'] = (v / v.sum(axis=2)[:, np.newaxis] /
                         bdt.n_estimators)[:, 0, 0].tolist()
        tree['rules'] = rules
        treesl.append(tree)
        ensembleDict['trees'].append(treesl)

    return ensembleDict


def convert(bdt, feature_cols=None):
    if 'GradientBoosting' in bdt.__class__.__name__:
        return convert_bdt(bdt, feature_cols)
    elif 'RandomForest' in bdt.__class__.__name__:
        return convert_random_forest(bdt, feature_cols)
    elif 'DecisionTreeClassifier' in bdt.__class__.__name__:
        return convert_decision_tree(bdt, feature_cols)


def treeToDict(bdt, tree):
    # Extract the relevant tree parameters
    treeDict = {'feature': tree.feature.tolist(
    ), 'threshold': tree.threshold.tolist(), 'value': tree.value.tolist()}
    treeDict['children_left'] = tree.children_left.tolist()
    treeDict['children_right'] = tree.children_right.tolist()
    treeDict = addParentAndDepth(treeDict)
    return treeDict


def treeToRules(bdt, feature_cols, classes):
    rules = io.StringIO()
    exportRules(bdt, feature_cols, classes, rules, '')
    res = rules.getvalue()
    rules.close()
    return res
