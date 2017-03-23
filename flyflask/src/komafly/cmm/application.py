import sys
    
from sqlalchemy import MetaData
from sqlalchemy import Column, Integer, String, DateTime, Text, and_, or_
from sqlalchemy import func

from flask import Flask, request, session, g, redirect, url_for,jsonify
from flask import abort, render_template, flash,make_response, request,send_file
from werkzeug import secure_filename

from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bootstrap import Bootstrap
import numpy as np

# http://flask-sqlalchemy.pocoo.org/2.1/quickstart/#a-minimal-application
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

def create_app():
    app = Flask(__name__)
    app.secret_key = 'super secret key'
    app.config['SESSION_TYPE'] = 'filesystem'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
    app.config['SQLALCHEMY_DATABASE_URI'] = DBMS
    app.config['SQLALCHEMY_ECHO'] = DEBUG_MODE
    app.config['DEBUG'] = DEBUG_MODE
    Bootstrap(app)
    return app

metadata = MetaData()
app = create_app()
db = SQLAlchemy(app,metadata=metadata,session_options={'autocommit': False })

from komafly.ktr.model import *
 
def init_db():
    engine = db.get_engine(app)    
    metadata.create_all(bind=engine)

