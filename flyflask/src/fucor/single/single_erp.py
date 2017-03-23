# -*- coding:utf-8 -*-
from fucor.single.single_base import *

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
class TM_ISSUE01(db.Model):
    __tablename__ = 'TM_ISSUE01'
    __table_args__ = {
        'autoload': True,
        'schema': DB_OWNER, 
        'autoload_with': db.engine
    }
    create_dt = db.Column(db.DateTime,  default=db.func.current_timestamp())
    update_dt = db.Column(db.DateTime,  default=db.func.current_timestamp(),
                                           onupdate=db.func.current_timestamp())


class TM_ISSUE04(db.Model):
    __tablename__ = 'TM_ISSUE04'
    __table_args__ = {
        'autoload': True,
        'schema': DB_OWNER, 
        'autoload_with': db.engine
    }

'''
## -------------------------------------------------------------------------------------
## STATEMENTS
## -------------------------------------------------------------------------------------
'''


def test_query_from_statment():
    stmt = '''
    SELECT A.ID
         , A.CATE_CODE
         , (SELECT CODE_VALUE FROM TM_ISSUE02 WHERE CODE = A.REQ ) REQ
         , A.REQ_MSG
         , (SELECT CODE_VALUE FROM TM_ISSUE02 WHERE CODE = A.RES ) RES
         , A.RES_MSG
         , (SELECT CODE_VALUE FROM TM_ISSUE02 WHERE CODE = A.JOB_STAT ) JOB_STAT
         , A.EXTRA_MSG
         , to_char(A.UPDATE_DT,'YYYY-MM-DD HH24:MI:SS') UPDATE_DT
         , to_char(A.CREATE_DT,'YYYY-MM-DD HH24:MI:SS') CREATE_DT
    FROM TM_ISSUE01 A
    WHERE 1 = 1 AND visible_yn = 'Y' AND 1 = :P1
    '''
    rs = db.session.query(TM_ISSUE01).from_statement(stmt).params(P1 = 1).all()
    for x in rs:
        print(x.cate_code, x.req, x.res)


def test_query_from_statment_with_view():
    stmt = '''
    SELECT A.ID
         , A.CATE_CODE
         , (SELECT CODE_VALUE FROM TM_ISSUE02 WHERE CODE = A.REQ ) REQ
         , A.REQ_MSG
         , (SELECT CODE_VALUE FROM TM_ISSUE02 WHERE CODE = A.RES ) RES
         , A.RES_MSG
         , (SELECT CODE_VALUE FROM TM_ISSUE02 WHERE CODE = A.JOB_STAT ) JOB_STAT
         , A.EXTRA_MSG
         , to_char(A.UPDATE_DT,'YYYY-MM-DD HH24:MI:SS') UPDATE_DT
         , to_char(A.CREATE_DT,'YYYY-MM-DD HH24:MI:SS') CREATE_DT
    FROM TM_ISSUE01 A
    WHERE 1 = 1 AND visible_yn = 'Y' AND 1 = :P1
    '''
    rs = db.session.query(TM_ISSUE01).from_statement(stmt).params(P1 = 1).all()
    for x in rs:
        print(x.cate_code, x.req, x.res)

from sqlalchemy.orm.exc import MultipleResultsFound
from sqlalchemy.orm.exc import NoResultFound

def test_query_multipleResultsFound_error_handle():
    try:
        rs = db.session.query().from_statement('select * from tm_issue04').one()
    except MultipleResultsFound as e:
        print("MultipleResultsFound")
        print(e)
    except Exception as e:
        print("EXTRA_ERROR")

def test_query_NoResultsFound_error_handle():
    try:
        rs = db.session.query().from_statement('select * from tm_issue04 where 1=2 ').one()
    except NoResultFound as e:
        print("NoResultFound")
        print(e)
    except Exception as e:
        print("EXTRA_ERROR")

def test_query_using_raw():
    r = db.session.query(TM_ISSUE04).filter("prog > :prog and prog > :prog").params(prog=75).order_by("TM_ISSUE04.devel").all()
    for x in r:
        print(x.prog)
        
test_query_using_raw()








if __name__ == '__main__':
    pass


   
    
    
    
    
    
    
    
    
    
