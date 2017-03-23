# -*- coding:utf-8 -*-
from fucor.single.single_base import *
from sqlalchemy.dialects.oracle.base import VARCHAR, NVARCHAR, NVARCHAR2,NUMBER
from flask_bootstrap import Bootstrap
from Cython.Compiler.Naming import self_cname

from fucor.single.load_excel import master, detail

DEV_ORACLE = "oracle+cx_oracle://ktrdb:dev4kotric@210.97.19.50:1521/orcl"
DEV_OWNER = 'KTRDB'

ERP_ORACLE = "oracle+cx_oracle://KTR_DEV:KTR12#@192.168.1.13:1521/orcl"
ERP_OWNER = 'KTR_DEV'

DB_URL = DEV_ORACLE
DB_OWNER = DEV_OWNER

app = Flask(__name__)
app.root_path = os.path.dirname(os.path.abspath(__file__))
app.config['SQLALCHEMY_DATABASE_URI'] = DB_URL
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
app.config['SQLALCHEMY_ECHO'] = True
app.config['DEBUG'] = True
app.config['SQLALCHEMY_COMMIT_ON_TEARDOWN '] = True # 2017.01.04 추가
Bootstrap(app)

metadata = MetaData()
db = SQLAlchemy(app,metadata=metadata,session_options={'autocommit': False })




'''
RE{X}T_CODE = 03 텍스트
- 01 : 공통코드
- 02 : 체크박스
- 03 : 텍스트
- 04 : 숫자
- 05 : 달력
'''
class TMP_TM_CODEXH(db.Model):
    __tablename__ = "TMP_TM_CODEXH"
    __table_args__ = {
        'schema': DB_OWNER 
    }    
    COMM_CODE = db.Column('COMM_CODE', db.String(30), primary_key=True, nullable=False)
    COMM_CDNM = db.Column('COMM_CDNM', db.String(100),nullable=False)
    SYST_CODE = db.Column('SYST_CODE', NVARCHAR(6))
    CDGB_CODE = db.Column('CDGB_CODE', NVARCHAR(6),nullable=False,default="1")
#     COCD_LNTH = db.Column('COCD_LNTH', NUMBER(precision=5, scale=0, asdecimal=False))
    RE1F_DESC = db.Column('RE1F_DESC', NVARCHAR(100))
    RE1T_CODE = db.Column('RE1T_CODE', NVARCHAR(6))
    RE2F_DESC = db.Column('RE2F_DESC', NVARCHAR(100))
    RE2T_CODE = db.Column('RE2T_CODE', NVARCHAR(6))
    RE3F_DESC = db.Column('RE3F_DESC', NVARCHAR(100))
    RE3T_CODE = db.Column('RE3T_CODE', NVARCHAR(6))
    RE4F_DESC = db.Column('RE4F_DESC', NVARCHAR(100))
    RE4T_CODE = db.Column('RE4T_CODE', NVARCHAR(6))
    INST_USID = db.Column('INST_USID', NVARCHAR(30),default="ADMIN",nullable=False) 
    INST_DATE = db.Column('INST_DATE', DATE,nullable=False,default=db.func.current_timestamp())
    UPDT_USID = db.Column('UPDT_USID', NVARCHAR(30),default="ADMIN",nullable=False) 
    UPDT_DATE = db.Column('UPDT_DATE', DATE,nullable=False,default=db.func.current_timestamp(), onupdate=db.func.current_timestamp())


class TMP_TM_CODEXD(db.Model):
    __tablename__ = "TMP_TM_CODEXD"
    __table_args__ = ( { 'schema': DB_OWNER } )    
    COMM_CODE = db.Column('COMM_CODE', db.String(30), primary_key=True, nullable=False)
    COMD_CODE = db.Column('COMD_CODE', db.String(30), primary_key=True, nullable=False)
    COMD_CDNM = db.Column('COMD_CDNM', NVARCHAR(200),nullable=False) 
    COMD_ENNM = db.Column('COMD_ENNM', NVARCHAR(100)) 
    CRTE_DATE = db.Column('CRTE_DATE', NVARCHAR(8),nullable=False,default="20170113") 
    REF1_FILD = db.Column('REF1_FILD', NVARCHAR(100)) 
    REF2_FILD = db.Column('REF2_FILD', NVARCHAR(100)) 
    REF3_FILD = db.Column('REF3_FILD', NVARCHAR(100)) 
    REF4_FILD = db.Column('REF4_FILD', NVARCHAR(100)) 
    SORT_ORDR = db.Column('SORT_ORDR', NUMBER(precision=5, scale=0, asdecimal=False)) 
    INST_USID = db.Column('INST_USID', NVARCHAR(30),default="ADMIN",nullable=False) 
    INST_DATE = db.Column('INST_DATE', DATE,nullable=False,default=db.func.current_timestamp())
    UPDT_USID = db.Column('UPDT_USID', NVARCHAR(30),default="ADMIN",nullable=False) 
    UPDT_DATE = db.Column('UPDT_DATE', DATE,nullable=False,default=db.func.current_timestamp(), onupdate=db.func.current_timestamp())

'''
SELECT * FROM TM_CODEXH WHERE COMM_CODE IN (SELECT COMM_CODE FROM TMP_TM_CODEXH);

DELETE FROM TM_CODEXH WHERE COMM_CODE IN (SELECT COMM_CODE FROM TMP_TM_CODEXH);
COMMIT;

INSERT INTO TM_CODEXH(COMM_CODE, COMM_CDNM, SYST_CODE, 
   CDGB_CODE, RE1F_DESC, RE1T_CODE, 
   RE2F_DESC, RE2T_CODE, RE3F_DESC, 
   RE3T_CODE, RE4F_DESC, RE4T_CODE, 
   INST_USID, INST_DATE, UPDT_USID, 
   UPDT_DATE) SELECT COMM_CODE, COMM_CDNM, SYST_CODE, 
   CDGB_CODE, RE1F_DESC, RE1T_CODE, 
   RE2F_DESC, RE2T_CODE, RE3F_DESC, 
   RE3T_CODE, RE4F_DESC, RE4T_CODE, 
   INST_USID, INST_DATE, UPDT_USID, 
   UPDT_DATE FROM TMP_TM_CODEXH;
   
   
COMMIT;   


SELECT * FROM TM_CODEXD WHERE COMM_CODE IN (SELECT COMM_CODE FROM TMP_TM_CODEXD);

DELETE FROM TM_CODEXD WHERE COMM_CODE IN (SELECT COMM_CODE FROM TMP_TM_CODEXD);
COMMIT;


DELETE FROM TM_CODEXD WHERE COMM_CODE IN (SELECT COMM_CODE FROM TMP_TM_CODEXD);
COMMIT;


INSERT INTO TM_CODEXD (
COMM_CODE, COMD_CODE, COMD_CDNM, 
   COMD_ENNM, CRTE_DATE, REF1_FILD, 
   REF2_FILD, REF3_FILD, REF4_FILD, 
   SORT_ORDR, INST_USID, INST_DATE, 
   UPDT_USID, UPDT_DATE
) SELECT 
COMM_CODE, COMD_CODE, COMD_CDNM, 
   COMD_ENNM, CRTE_DATE, REF1_FILD, 
   REF2_FILD, REF3_FILD, REF4_FILD, 
   SORT_ORDR, INST_USID, INST_DATE, 
   UPDT_USID, UPDT_DATE
FROM TMP_TM_CODEXD;

COMMIT;
'''


def clear_tmp_tm_codexh():
    db.session.query(TMP_TM_CODEXH).delete()
    try:
        db.session.commit()
    except Exception as e:
        db.session.rollback()

def clear_tmp_tm_codexd():
    db.session.query(TMP_TM_CODEXD).delete()
    try:
        db.session.commit()
    except Exception as e:
        db.session.rollback()

def apply_master_code():
    delete_script = '''
DELETE FROM TM_CODEXH WHERE COMM_CODE IN (SELECT COMM_CODE FROM TMP_TM_CODEXH)
'''
    move_script = '''
INSERT INTO TM_CODEXH(COMM_CODE, COMM_CDNM, SYST_CODE, 
   CDGB_CODE, RE1F_DESC, RE1T_CODE, 
   RE2F_DESC, RE2T_CODE, RE3F_DESC, 
   RE3T_CODE, RE4F_DESC, RE4T_CODE, 
   INST_USID, INST_DATE, UPDT_USID, 
   UPDT_DATE) SELECT COMM_CODE, COMM_CDNM, SYST_CODE, 
   CDGB_CODE, RE1F_DESC, RE1T_CODE, 
   RE2F_DESC, RE2T_CODE, RE3F_DESC, 
   RE3T_CODE, RE4F_DESC, RE4T_CODE, 
   INST_USID, INST_DATE, UPDT_USID, 
   UPDT_DATE FROM TMP_TM_CODEXH
    '''    
    with db.engine.connect() as c:
        tr = c.begin()
        try:
            c.execute(delete_script)
            c.execute(move_script)
            tr.commit()
        except Exception as e:
            eprint("TR_ERROR - ",e)
            tr.rollback()

def apply_detail_code():
    delete_script = '''
DELETE FROM TM_CODEXD WHERE COMM_CODE IN (SELECT COMM_CODE FROM TMP_TM_CODEXD)
'''
    move_script = '''
INSERT INTO TM_CODEXD (
COMM_CODE, COMD_CODE, COMD_CDNM, 
   COMD_ENNM, CRTE_DATE, REF1_FILD, 
   REF2_FILD, REF3_FILD, REF4_FILD, 
   SORT_ORDR, INST_USID, INST_DATE, 
   UPDT_USID, UPDT_DATE
) SELECT 
COMM_CODE, COMD_CODE, COMD_CDNM, 
   COMD_ENNM, CRTE_DATE, REF1_FILD, 
   REF2_FILD, REF3_FILD, REF4_FILD, 
   SORT_ORDR, INST_USID, INST_DATE, 
   UPDT_USID, UPDT_DATE
FROM TMP_TM_CODEXD
    '''    
    with db.engine.connect() as c:
        tr = c.begin()
        try:
            c.execute(delete_script)
            c.execute(move_script)
            tr.commit()
        except Exception as e:
            eprint("TR_ERROR - ",e)
            tr.rollback()
             

def mig_master_code(code=None):
    eprint("DB_URL ->"+DB_URL)
    clear_tmp_tm_codexh()
    df = master(code)
    df = df.fillna('')
    buf = []
    for i, x in enumerate(df.to_dict(orient="records")):
        t = TMP_TM_CODEXH()
        t.COMM_CDNM = x.get('COMM_CDNM')
        t.COMM_CODE = x.get('COMM_CODE')
        t.RE1F_DESC = x.get('RE1F_DESC')
        t.RE2F_DESC = x.get('RE2F_DESC')
        t.RE3F_DESC = x.get('RE3F_DESC')
        t.RE4F_DESC = x.get('RE4F_DESC')
        buf.append(t)
        
    db.session.add_all(buf)
    try:
        db.session.commit()
        apply_master_code();
    except Exception as e:
        eprint(e)
        db.session.rollback()

def mig_detail_code(code=None):
    clear_tmp_tm_codexd()
    eprint("DB_URL ->"+DB_URL)
    df = detail(code)
    df = df.fillna('')
    buf = []
    for i, x in enumerate(df.to_dict(orient="records")):
        t = TMP_TM_CODEXD()
        t.COMM_CODE = x.get('COMM_CODE')
        t.COMD_CODE = x.get('COMD_CODE')
        t.COMD_CDNM = x.get('COMD_CDNM')
        t.REF1_FILD = x.get('REF1_FILD')
        t.REF2_FILD = x.get('REF2_FILD')
        t.REF3_FILD = x.get('REF3_FILD')
        t.REF4_FILD = x.get('REF4_FILD')
        t.COMD_ENNM = ''
        t.SORT_ORDR = i
        buf.append(t)
        
    db.session.add_all(buf)
    try:
        db.session.commit()
        apply_detail_code()
    except Exception as e:
        eprint(e)
        db.session.rollback()


if __name__ == '__main__':
    code = [ 'SNDNG_MTH_CD'
    , 'TEST_PROGRS_MTH_CD'
    , 'CNTC_ENTRPS_CD'
    , 'ELCTRN_DOC_SNDNG_MTH_CD'
    , 'SCCD_CL_CD'
    , 'SUBPLC_NM'
    , 'SCCD_PRPOS_CD'
    , 'JOB_CL_CD'
    , 'SPLORE_SNDNG_MTH_CD'
    , 'MBER_SE_CD' ]
    code = []
    mig_master_code(code);
    mig_detail_code(code);


if __name__ == '__main__x':
   mig_master_code();
   mig_detail_code();



def re_create_all():
    db.metadata.drop_all(db.engine,tables=[
        TMP_TM_CODEXH.__table__
        , TMP_TM_CODEXD.__table__
    ])        
    db.create_all()
    
if __name__ == '__main__xxx':
   re_create_all()
    

    
