# This source file comes from the Conifer open-source project 
# (https://github.com/thesps/conifer)

import pytest
import util

@pytest.fixture
def train_skl():
    # Example BDT creation from: https://scikit-learn.org/stable/modules/ensemble.html
    from sklearn.datasets import make_hastie_10_2
    from sklearn.ensemble import GradientBoostingClassifier

    # Make a random dataset from sklearn 'hastie'
    X, y = make_hastie_10_2(random_state=0)
    X_train, X_test = X[:2000], X[2000:]
    y_train, y_test = y[:2000], y[2000:]

    # Train a BDT
    clf = GradientBoostingClassifier(n_estimators=20, learning_rate=1.0,
        max_depth=3, random_state=0).fit(X_train, y_train)

    return clf, X_test, y_test
    
@pytest.fixture
def hls_convert(train_skl):
    import entree
    import datetime

    clf, X, y = train_skl

    # Create a entree config
    cfg = entree.backends.vivadohls.auto_config()
    cfg['Precision'] = 'ap_fixed<32,16,AP_RND,AP_SAT>'
    # Set the output directory to something unique
    cfg['OutputDir'] = 'prj_{}'.format(int(datetime.datetime.now().timestamp()))
    cfg['XilinxPart'] = 'xcu250-figd2104-2L-e'

    # Create and compile the model
    model = entree.model(clf, entree.converters.sklearn, entree.backends.vivadohls, cfg)
    model.compile()
    return model

@pytest.fixture
def vhdl_convert(train_skl):
    import entree
    import datetime

    clf, X, y = train_skl

    # Create a entree config
    cfg = entree.backends.vivadohls.auto_config()
    cfg['Precision'] = 'ap_fixed<32,16>'
    # Set the output directory to something unique
    cfg['OutputDir'] = 'prj_{}'.format(int(datetime.datetime.now().timestamp()))
    cfg['XilinxPart'] = 'xcu250-figd2104-2L-e'

    # Create and compile the model
    model = entree.model(clf, entree.converters.sklearn, entree.backends.vhdl, cfg)
    model.compile()
    return model

@pytest.fixture
def predict(train_skl, hls_convert):
    clf, X, y = train_skl
    model = hls_convert
    return util.predict(clf, X, y, model)

def test_skl_hls_predict(predict):
    import numpy as np
    y_hls, y_skl = predict
    assert np.all(np.isclose(y_hls, y_skl, rtol=1e-2, atol=1e-2))

def test_skl_build(hls_convert):
    model = hls_convert
    model.build()
    assert True

def test_hdl_predict(train_skl, vhdl_convert):
    clf, X, y = train_skl
    model = vhdl_convert
    return util.predict(clf, X, y, model)

def test_hdl_build(vhdl_convert):
    model = vhdl_convert
    model.build()
    assert True


