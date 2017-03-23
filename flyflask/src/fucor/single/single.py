# -*- coding:utf-8 -*-
import os
import sys
    
from sqlalchemy import Enum
from sqlalchemy import *
from flask import *

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

# SQLITE3 = "sqlite:///D:/fucor_db.db"
SQLITE3 = "sqlite:///D:/single_db.db"

def create_app():
    app = Flask(__name__)
    app.root_path = os.path.dirname(os.path.abspath(__file__))
    app.secret_key = 'super secret key'
    app.config['SESSION_TYPE'] = 'filesystem'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
    app.config['SQLALCHEMY_DATABASE_URI'] = DEV_ORACLE
    app.config['SQLALCHEMY_ECHO'] = True
    app.config['DEBUG'] = True
    app.config['SQLALCHEMY_COMMIT_ON_TEARDOWN '] = True # 2017.01.04 추가
    Bootstrap(app)
    return app

metadata = MetaData()
app = create_app()
db = SQLAlchemy(app,metadata=metadata,session_options={'autocommit': False })

'''

class CM_ISSUE01(db.Model):
    __tablename__ = "CM_ISSUE01"
    id        = db.Column(db.Integer,nullable=False, primary_key=True)
    scrn_id   = db.Column(db.String(50),nullable=False)
    dev_user  = db.Column(db.String(50),nullable=False)
    oper_user = db.Column(db.String(50),nullable=True)
    proc      = db.Column(Enum('중단','예정','진행중','완료','이슈'),nullable=False)
    pre_ref   = db.Column(db.String(50),nullable=True)
    issue     = db.Column(db.Text,nullable=False)
    create_dt = db.Column(db.DateTime,  default=db.func.current_timestamp())
    update_dt = db.Column(db.DateTime,  default=db.func.current_timestamp(),
                                           onupdate=db.func.current_timestamp())


'''

class CM_ISSUE01(db.Model):
    __tablename__ = 'CM_ISSUE01'
    __table_args__ = {
        'autoload': True,
        'schema': DEV_OWNER, 
        'autoload_with': db.engine
    }
    create_dt = db.Column(db.DateTime,  default=db.func.current_timestamp())
    update_dt = db.Column(db.DateTime,  default=db.func.current_timestamp(),
                                           onupdate=db.func.current_timestamp())
import flask_restless as rest

# Create the Flask-Restless API manager.
manager = rest.APIManager(app, session=db.session)
# manager.create_api(CM_CODER, methods=['GET', 'POST', 'DELETE'])

def rebuild_db():
    db.metadata.drop_all(db.engine,tables=[
        CM_ISSUE01.__table__
    ])
    db.create_all()
#     db.create_all(db.engine, tables=[
#         CM_ISSUE01.__table__
#     ])

def commit(session):
    try:
        session.commit()
    except Exception as e:
        eprint(e)
        session.rollback()
        session.flush()

def insert_data():
    issue = CM_ISSUE01()
    issue.id = 3
    issue.scrn_id = 'TM00001'
    issue.dev_user = '백승우'
    issue.proc = '중단'
    issue.issue = "ㄴㅇㄹㄹㅉㄹㅉㅇㄹㅉㄹㅉㄹㅉㄹ"
    db.session.add(issue)
    commit(db.session)

if __name__ == '__main__':
#     rebuild_db()
    insert_data()
#     df = pd.read_sql('select * from cm_issue01',con=db.engine)
#     print(df['issue'])
#     d = df.to_dict(orient='list')
#     eprint(d.get('issue')[0])
#     


    
    
    
    
    
    
    
    
    
    
