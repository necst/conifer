# This source file comes from the Conifer open-source project
# (https://github.com/thesps/conifer)

import itertools
import numpy as np
from .converter import addParentAndDepth, padTree
from ..model import model
from .sklearn_rule_exporter import generateDecisionTree as exportRules
import io


def convert_bdt(bdt, feature_cols, enable_padding):
    classes = bdt.classes_.tolist()

    ensembleDict = {'max_depth': bdt.max_depth, 'n_trees': bdt.n_estimators,
                    'n_features': bdt.n_features_,
                    'n_classes': bdt.n_classes_, 'trees': [],
                    'init_predict': bdt._raw_predict_init(np.zeros(bdt.n_features_).reshape(1, -1))[0].tolist(),
                    'classes': classes,
                    'norm': 1}
    

    for trees in bdt.estimators_:
        treesl = []
        for tree in trees:
            tree = treeToDict(bdt, tree.tree_)
            if enable_padding:
                tree = padTree(ensembleDict, tree)
            # NB node values are multiplied by the learning rate here, saving work in the FPGA
            tree['value'] = (np.array(tree['value'])[:, 0, 0]
                             * bdt.learning_rate).tolist()
            tree['rules'] = None #TODO: Extend rule support for Gradient Boosting
            treesl.append(tree)
        ensembleDict['trees'].append(treesl)

    return ensembleDict


def convert_decision_tree(bdt, feature_cols, enable_padding):
    if len(bdt) == 1:
        n_features = bdt[0].n_features_
        n_classes = bdt[0].n_classes_
        classes = bdt[0].classes_.tolist()
    elif len(bdt) > 1:
        if any(treeA.n_features_ != treeB.n_features_ for treeA in bdt for treeB in bdt):
            raise Exception("Unsupported: Decision Tree Classifiers with different meta-parameters")
        n_features = bdt[0].n_features_
        classes = list(dict.fromkeys(itertools.chain(*[tree.classes_ for tree in bdt])))
        n_classes = len(classes)
    else:
        raise Exception("No Decision Tree Classifier was supplied")

    ensembleDict = {'max_depth': max(tree.max_depth for tree in bdt),
                    'n_trees': len(bdt),
                    'n_features': n_features,
                    'n_classes': n_classes, 
                    'trees': [],
                    'init_predict': [0] * n_classes,
                    'norm': 1,
                    'classes': classes}

    for tree in bdt:
        local_classes = tree.classes_
        rules = treeToRules(tree, feature_cols, classes)
        tree = treeToDict(None, tree.tree_)
        if enable_padding:
            tree = padTree(ensembleDict, tree)
        tree['value'] = list(
            map(
                lambda x: classes.index(local_classes[x]), 
                map(
                    lambda x: x[0].index(max(x[0])), 
                    tree['value']
                )
            )
        )
        tree['rules'] = rules
        ensembleDict['trees'].append([tree])

    ensembleDict['direct'] = True
    
    return ensembleDict


def convert_random_forest(bdt, feature_cols, enable_padding):
    ensembleDict = {'max_depth': bdt.max_depth, 'n_trees': bdt.n_estimators,
                    'n_features': bdt.n_features_,
                    'n_classes': bdt.n_classes_, 'trees': [],
                    'init_predict': [0] * bdt.n_classes_,
                    'classes': bdt.classes_.tolist(),
                    'norm': 1}
    for tree in bdt.estimators_:
        treesl = []
        rules = treeToRules(tree, feature_cols, bdt.classes_)
        tree = treeToDict(bdt, tree.tree_)
        if enable_padding:
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


def convert(bdt, feature_cols = None, enable_padding = True):
    if 'GradientBoosting' in bdt.__class__.__name__:
        #TODO: Implement support for Gradient Boosting
        raise Exception("Gradient Boosting Classifier is not supported")
        #return convert_bdt(bdt, feature_cols, enable_padding)
    elif 'RandomForest' in bdt.__class__.__name__:
        #TODO: Implement support for Random Forest
        raise Exception("Random Forest Classifier is not supported")
        #return convert_random_forest(bdt, feature_cols, enable_padding)
    elif type(bdt) is list and all('DecisionTreeClassifier' in tree.__class__.__name__ for tree in bdt):
        return convert_decision_tree(bdt, feature_cols, enable_padding)
    else:
        raise Exception(f"Unrecognized Sklearn Classifier: {type(bdt)}")


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
