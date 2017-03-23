# -*- coding:utf-8 -*-
import os
# os.environ["FLASK_APP"] = "flaskr"
# os.environ["FLASK_DEBUG"] = "1"
from fucor.cod.models import CM_CODER,CM_METHOD,CM_PARAMS,CM_TABLE
'''
author : Baek Seung Woo
'''
__version__ = '0.0.1'

from fucor.application import *
from fucor.cmm.controllers import * 

app.root_path = os.path.dirname(os.path.abspath(__file__))

# Sample HTTP error handling
@app.errorhandler(404)
def not_found(error):
    return render_template('404.html'), 404

from fucor.cmm.controllers import mod_cmm 
from fucor.cod.controllers import mod_cod 

app.register_blueprint(mod_cmm)
app.register_blueprint(mod_cod)

import flask_restless as rest

# Create the Flask-Restless API manager.
manager = rest.APIManager(app, session=db.session)
manager.create_api(CM_CODER, methods=['GET', 'POST', 'DELETE'])
manager.create_api(CM_METHOD, methods=['GET', 'POST', 'DELETE'])
manager.create_api(CM_PARAMS, methods=['GET', 'POST', 'DELETE'])
manager.create_api(CM_TABLE, methods=['GET', 'POST', 'DELETE'])


