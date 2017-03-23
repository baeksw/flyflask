# -*- coding:utf-8 -*-
import os
# os.environ["FLASK_APP"] = "flaskr"
# os.environ["FLASK_DEBUG"] = "1"
'''
author : Baek Seung Woo
'''
__version__ = '0.0.1'

from komafly.cmm.application import *
from komafly.ktr.controller import *

app.root_path = os.path.dirname(os.path.abspath(__file__))

# Sample HTTP error handling
@app.errorhandler(404)
def not_found(error):
    return render_template('404.html'), 404


from komafly.ktr.controller import mode_ktr as ktr_module

app.register_blueprint(ktr_module)
