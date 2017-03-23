
from flask import Blueprint, request, render_template
from flask import flash, g, session, redirect, url_for

from werkzeug import check_password_hash, generate_password_hash

from fucor.application import db
from fucor.cmm.models import *
from fucor.cmm.services import *

import numpy as np
import pandas as pd
from functools import partial
 
mod_cmm = Blueprint('cmm', __name__, url_prefix='/', template_folder='templates')

@mod_cmm.route('/', methods=['GET', 'POST'])
def index():
    return render_template("cmm/index.html")

@mod_cmm.route("/coder/add", methods=['GET','POST'])
def coder_add():
    if request.method == 'POST':
        pass
    return render_template("cmm/add.html")
