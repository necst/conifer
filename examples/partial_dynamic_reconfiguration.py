from sklearn.datasets import load_iris
from sklearn.ensemble import GradientBoostingClassifier
import conifer
import datetime

iris = load_iris()
X, y = iris.data, iris.target

clf = GradientBoostingClassifier(n_estimators=6, learning_rate=1.0,
                                 max_depth=3, random_state=0).fit(X, y)

# Create a conifer config
cfg = conifer.backends.xilinxhls.auto_config()
# Set the output directory to something unique
cfg['ProjectName'] = 'iris_PDR_Vivado_GB'
cfg['OutputDir'] = 'prj_{}'.format(
    # int(datetime.datetime.now().timestamp())
    cfg['ProjectName']
)
cfg['XilinxPart'] = "xc7z020clg400-1"
cfg['XilinxBoard'] = "tul.com.tw:pynq-z2:part0:1.0"
cfg['ClockPeriod'] = "10"
cfg['PDR'] = True
cfg['Banks'] = "2"
cfg['TreesPerBank'] = "3"


model = conifer.model(clf, conifer.converters.sklearn,
                      conifer.backends.xilinxhls, cfg)
model.compile()

# # Run HLS C Simulation and get the output
y_hls = model.decision_function(X)
y_skl = clf.decision_function(X)

# # Synthesize the model
model.build(export=True)
