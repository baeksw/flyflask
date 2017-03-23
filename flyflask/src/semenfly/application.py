# -*- coding: utf-8 -*-
import sys
    
from sqlalchemy import MetaData
from sqlalchemy import Column, Integer, String, DateTime, Text, and_, or_
from sqlalchemy import func
'''
from flask import Blueprint, request, render_template
from flask import flash, g, session, redirect, url_for
from flask import Flask, request, session, g, redirect, url_for,jsonify
from flask import abort, render_template, flash,make_response, request,send_file
'''
from werkzeug import check_password_hash, generate_password_hash
from flask import *

from werkzeug import secure_filename

from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bootstrap import Bootstrap
import numpy as np

# http://flask-sqlalchemy.pocoo.org/2.1/quickstart/#a-minimal-application

import numpy as np
import pandas as pd

import time
from datetime import datetime

def eprint(*args, **kwargs):
    print(*args, file=sys.stderr, **kwargs)

DEV_ORACLE = "oracle+cx_oracle://ktrdb:dev4kotric@210.97.19.50:1521/orcl"
DEV_OWNER = 'KTRDB'

ERP_ORACLE = "oracle+cx_oracle://KTR_DEV:KTR12#@192.168.1.13:1521/orcl"
ERP_OWNER = 'KTR_DEV'

DBMS = ERP_ORACLE
DB_OWNER = ERP_OWNER

DEBUG_MODE = True

SQLITE3 = "sqlite:///D:/semen_db.db"

def create_app():
    app = Flask(__name__)
    app.secret_key = 'super secret key'
    app.config['SESSION_TYPE'] = 'filesystem'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
    app.config['SQLALCHEMY_DATABASE_URI'] = SQLITE3
    app.config['SQLALCHEMY_ECHO'] = DEBUG_MODE
    app.config['DEBUG'] = DEBUG_MODE
    app.config['SQLALCHEMY_COMMIT_ON_TEARDOWN '] = True # 2017.01.04 추가
    Bootstrap(app)
    return app

metadata = MetaData()
app = create_app()
db = SQLAlchemy(app,metadata=metadata,session_options={'autocommit': False })

# ----------------------------------------------------------------------------
# IMPORT MODELS
# ----------------------------------------------------------------------------

#from fucor.cmm.models import *

# ----------------------------------------------------------------------------
 
def init_db():
    engine = db.get_engine(app)    
    metadata.create_all(bind=engine)

    
import os
from jinja2 import Environment, PackageLoader
env = Environment(loader=PackageLoader('semenfly','templates'),extensions=['jinja2.ext.do'])
#tpl_table = env.get_template('./create_table.tpl') 

def get_template(tpl):
    return env.get_template(tpl)
