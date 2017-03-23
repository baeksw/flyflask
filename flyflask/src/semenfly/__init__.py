# -*- coding:utf-8 -*-
'''
author : Baek Seung Woo
'''
__version__ = '0.0.1'
import os
# os.environ["FLASK_APP"] = "flaskr"
# os.environ["FLASK_DEBUG"] = "1"

from semenfly.application import *
from semenfly.cmm.controllers import * 

app.root_path = os.path.dirname(os.path.abspath(__file__))

# Sample HTTP error handling
@app.errorhandler(404)
def not_found(error):
    return render_template('404.html'), 404

from semenfly.cmm.controllers import mod_cmm 
from semenfly.cod.controllers import mod_cod 

app.register_blueprint(mod_cmm)
app.register_blueprint(mod_cod)

import flask_restless as rest

# Create the Flask-Restless API manager.
manager = rest.APIManager(app, session=db.session)
# manager.create_api(CM_CODER, methods=['GET', 'POST', 'DELETE'])


