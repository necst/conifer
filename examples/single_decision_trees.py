# This source file comes from the Conifer open-source project 
# (https://github.com/thesps/conifer)

from sklearn.datasets import load_iris
from sklearn.tree import DecisionTreeClassifier
import entree
import datetime

iris = load_iris()
X, y = iris.data, iris.target

X1, y1 = X[:int(len(X)/2)], y[:int(len(y)/2)]
X2, y2 = X[int(len(X)/2):], y[int(len(y)/2):]

clf1 = DecisionTreeClassifier(max_depth=8, random_state=0).fit(X1, y1)
clf2 = DecisionTreeClassifier(max_depth=8, random_state=0).fit(X2, y2)

# Create a conifer config
cfg = entree.backends.generic_cpp.auto_config()
# Set the output directory to something unique
cfg['OutputDir'] = 'prj_{}'.format(int(datetime.datetime.now().timestamp()))
cfg['FeatureList'] = iris.feature_names

model = entree.model(
    [clf1, clf2], 
    entree.converters.sklearn,
    entree.backends.generic_cpp, 
    cfg
)

model.compile()

