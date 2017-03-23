# -*- coding:utf-8 -*-
from fucor.single.single_base import *
from sqlalchemy.dialects.oracle import *

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
'''
class CF_BCBS005(AutoLoadBase): 
    __tablename__ = 'CF_BCBS005'
'''

class TMP_CF_BCBS005(db.Model):
    __tablename__ = 'TMP_CF_BCBS005'
    MAK_CRTFC_STNDRD_REGIST_ID = db.Column(db.String(10),nullable=False,primary_key=True)
    MAK_PRDLST_CD = db.Column(db.String(10))
    MAK_PRDLST_NM = db.Column(db.String(100))
    MAK_REPRSNT_PRDLST = db.Column(db.String(100))
    APPN_DE = db.Column(db.String(8))
    CNFIRM_DE = db.Column(db.String(8))
    ESTBSH_REFORM_SE = db.Column(db.String(1))
    CN_DC = db.Column(db.String(100))
    MAK_MODEL_CN = db.Column(db.String(100))
    MAK_CRTFC_REALM_NM = db.Column(db.String(100))
    MAK_CRTFC_SCOPE_NM = db.Column(db.String(100))
    ATCH_ID = db.Column(db.String(6))
    WRTER_ID = db.Column(db.String(10))
    ESTMAN_ID = db.Column(db.String(10))
    REGISTER_ID = db.Column(db.String(10),nullable=False)
    REGIST_DT = db.Column(db.DATE,nullable=False)
    CHANGER_ID = db.Column(db.String(10),nullable=False)
    CHANGE_DT = db.Column(db.DATE,nullable=False)
    LAST_YN = db.Column(db.String(1))
    BEFORE_MAK_CRTFC_STN = db.Column(db.String(10))
    PROC_DE_CO = db.Column(NUMBER(4, 0))
    USESE = db.Column(db.String(1))
    MAKSE = db.Column(db.String(1))

'''
## -------------------------------------------------------------------------------------
## STATEMENTS
## -------------------------------------------------------------------------------------

COL_TPL = "{} = db.Column(db.{},nullable={},default={},primary_key={})"

def test_get_table_info():
    tbl = CF_BCBS005.__table__
    for x in tbl.c:
        _name = x.key.upper()
        _type = "db.{}".format(str(x.type).replace("VARCHAR","String"))
        _nullable = ",nullable={}".format(x.nullable) if x.nullable is False else ""
        _default = ",default={}".format(x.default) if x.default is not None else ""
        _primary_key = ",primary_key={}".format(x.primary_key) if x.primary_key is True else ""

        print("{} = db.Column({}{}{}{})".format(_name,_type,_nullable,_default,_primary_key))
#         print (x.key.upper())
#         print (str(x.type))
#         print(x.info)

test_get_table_info()
'''

class CP_BNCR002(AutoLoadBase): 
    __tablename__ = 'CP_BNCR002'

def test_get_table_info():
    tbl = CP_BNCR002.__table__
    for x in tbl.c:
        _name = x.key.upper()
        _type = "db.{}".format(str(x.type).replace("VARCHAR","String"))
        _nullable = ",nullable={}".format(x.nullable) if x.nullable is False else ""
        _default = ",default={}".format(x.default) if x.default is not None else ""
        _primary_key = ",primary_key={}".format(x.primary_key) if x.primary_key is True else ""

        print("{} = db.Column({}{}{}{})".format(_name,_type,_nullable,_default,_primary_key))


if __name__ == '__main__':
    test_get_table_info()

if __name__ == '__main__2':
    db.metadata.drop_all(db.engine,tables=[
        TMP_CF_BCBS005.__table__
    ])
    db.create_all()


   
    
    
    
    
    
    
    
    
    
