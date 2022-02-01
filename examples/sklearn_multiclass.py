# This source file comes from the Conifer open-source project 
# (https://github.com/thesps/conifer)

from sklearn.datasets import load_iris
from sklearn.ensemble import RandomForestClassifier
import entree
import datetime

iris = load_iris()
X, y = iris.data, iris.target

clf = RandomForestClassifier(n_estimators=8,
                                 max_depth=3, random_state=0).fit(X, y)

# Create a entree config
cfg = entree.backends.generic_cpp.auto_config()
# Set the output directory to something unique
cfg['OutputDir'] = 'prj_{}'.format(int(datetime.datetime.now().timestamp()))
cfg['FeatureList'] = iris.feature_names
cfg['ClassList'] = iris.target_names

model = entree.model(clf, entree.converters.sklearn,
                      entree.backends.generic_cpp, cfg)
model.compile()

