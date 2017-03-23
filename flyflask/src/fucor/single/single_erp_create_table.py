# -*- coding:utf-8 -*-
import functools
from fucor.single.single_base import *
from sqlalchemy import MetaData
from sqlalchemy.dialects.oracle.base import VARCHAR, NVARCHAR, NVARCHAR2

DEV_ORACLE = "oracle+cx_oracle://ktrdb:dev4kotric@210.97.19.50:1521/orcl"
DEV_OWNER = 'KTRDB'

ERP_ORACLE = "oracle+cx_oracle://KTR_DEV:KTR12#@192.168.1.13:1521/orcl"
ERP_OWNER = 'KTR_DEV'

DB_URL = ERP_ORACLE
DB_OWNER = ERP_OWNER

# SQLITE3 = "sqlite:///D:/fucor_db.db"
SQLITE3 = "sqlite:///D:/single_db.db"

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = DB_URL
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
app.config['SQLALCHEMY_ECHO'] = True
app.config['DEBUG'] = True
app.config['SQLALCHEMY_COMMIT_ON_TEARDOWN '] = True # 2017.01.04 추가

metadata = MetaData()
db = SQLAlchemy(app,metadata=metadata,session_options={'autocommit': False })

'''
## -------------------------------------------------------------------------------------
## MODELS
## -------------------------------------------------------------------------------------
'''

class AutoLoadBase(db.Model):
    __abstract__  = True
    __table_args__ = { 'autoload': True, 'schema': DB_OWNER, 'autoload_with': db.engine }

# class CP_BNCR023(AutoLoadBase): __tablename__ = 'CP_BNCR023'
# class CP_BNCR002(AutoLoadBase): __tablename__ = 'CP_BNCR002'

class CF_BCRV006(db.Model):
    __tablename__ ="CF_BCRV006"
    FCTRY_JDGMN_CO_ID = Column(NVARCHAR2(10),primary_key=True) 
    FCTRY_FDRM_PRSEC_ID = Column(NVARCHAR2(10),nullable=False) 
    RCEPT_NO = Column(NVARCHAR2(10)) 
    FDRM_PRSEC_YEAR = Column(NVARCHAR2(4),nullable=False) 
    CSTMR_NO = Column(NVARCHAR2(10)) 
    JDGMN_DE = Column(NVARCHAR2(8)) 
    RCPMNY_DE = Column(NVARCHAR2(8)) 
    CT_PYMNTDE = Column(NVARCHAR2(8)) 
    EVL_RESULT = Column(NVARCHAR2(1)) 
    IMPROPT_CN = Column(NVARCHAR2(50)) 
    AUDOFIR = Column(NVARCHAR2(10),) 
    REGISTER_ID = Column(NVARCHAR2(10)) 
    REGIST_DT = Column(db.DateTime) 
    CHANGER_ID = Column(NVARCHAR2(10)) 
    CHANGE_DT = Column(db.DateTime) 

    
    
    
    
db.create_all()
    
    
