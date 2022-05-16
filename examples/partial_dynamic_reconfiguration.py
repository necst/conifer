# Copyright 2022 Novel, Emerging Computing System Technologies Laboratory 
#                (NECSTLab), Politecnico di Milano

# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at

#     http://www.apache.org/licenses/LICENSE-2.0

# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

from sklearn.datasets import load_iris
from sklearn.ensemble import GradientBoostingClassifier
import entree
import datetime

iris = load_iris()
X, y = iris.data, iris.target

clf = GradientBoostingClassifier(n_estimators=6, learning_rate=1.0,
                                 max_depth=3, random_state=0).fit(X, y)

# Create an entree config
# NOTE: if not set, the nJobs will be set to total number of cores minus two
cfg = entree.backends.xilinxhls.auto_config()
# Set the output directory to something unique
cfg['ProjectName'] = 'iris_PDR_Vivado_GB'
cfg['OutputDir'] = 'prj_{}'.format(
    # int(datetime.datetime.now().timestamp())
    cfg['ProjectName']
)
cfg['XilinxPart'] = "xczu3eg-sbva484-1-i"
cfg['XilinxBoard'] = "avnet.com:ultra96v2:part0:1.2"
cfg['ClockPeriod'] = "10"
cfg['PDR'] = True
cfg['Banks'] = "2"
cfg['TreesPerBank'] = "3"
cfg['nJobs'] = "12"


model = entree.model(clf, entree.converters.sklearn,
                      entree.backends.xilinxhls, cfg)
model.compile()

# # Run HLS C Simulation and get the output
y_hls = model.decision_function(X)
y_skl = clf.decision_function(X)

# # Synthesize the model
model.build(export=True)
