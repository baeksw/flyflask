# -*- coding:utf-8 -*-
from fucor.single.single_base import *
from sqlalchemy.dialects.oracle.base import VARCHAR, NVARCHAR, NVARCHAR2,NUMBER
from flask_bootstrap import Bootstrap
from Cython.Compiler.Naming import self_cname

DEV_ORACLE = "oracle+cx_oracle://ktrdb:dev4kotric@210.97.19.50:1521/orcl"
DEV_OWNER = 'KTRDB'

ERP_ORACLE = "oracle+cx_oracle://KTR_DEV:KTR12#@192.168.1.13:1521/orcl"
ERP_OWNER = 'KTR_DEV'

DB_URL = DEV_ORACLE
DB_OWNER = DEV_OWNER

# SQLITE3 = "sqlite:///D:/fucor_db.db"
SQLITE3 = "sqlite:///D:/single_db.db"

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
# ------------------------------------------------------------------------------
MODELS
# ------------------------------------------------------------------------------
'''
class Base(db.Model):
    __abstract__  = True    
    @staticmethod
    def timestamp():
        return db.func.current_timestamp()
    

class TM_CODEXH(db.Model):
    __tablename__ = "TM_CODEXH"
    __table_args__ = {
        'autoload': True,
        'schema': DB_OWNER, 
        'autoload_with': db.engine
    }
    create_dt = db.Column(db.DateTime,  default=db.func.current_timestamp())
    update_dt = db.Column(db.DateTime,  default=db.func.current_timestamp(), onupdate=db.func.current_timestamp())

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
    Column('COMM_CODE', NVARCHAR(30), primary_key=True)
    Column('COMM_CDNM', NVARCHAR(100),nullable=False)
    Column('SYST_CODE', NVARCHAR(6))
    Column('CDGB_CODE', NVARCHAR(6))
    Column('COCD_LNTH', NUMBER(precision=5, scale=0, asdecimal=False))
    Column('RE1F_DESC', NVARCHAR(100))
    Column('RE1T_CODE', NVARCHAR(6))
    Column('RE2F_DESC', NVARCHAR(100))
    Column('RE2T_CODE', NVARCHAR(6))
    Column('RE3F_DESC', NVARCHAR(100))
    Column('RE3T_CODE', NVARCHAR(6))
    Column('RE4F_DESC', NVARCHAR(100))
    Column('RE4T_CODE', NVARCHAR(6))
    Column('INST_USID', NVARCHAR(30),default="ADMIN")
    Column('INST_DATE', default=db.func.current_timestamp())
    Column('UPDT_USID', NVARCHAR(30),default="ADMIN")
    Column('UPDT_DATE', default=db.func.current_timestamp(), onupdate=db.func.current_timestamp())

class TMP_TM_CODEXD(db.Model):
    __tablename__ = "TMP_TM_CODEXD"
    __table_args__ = {
        'schema': DB_OWNER 
    }        
    Column('COMM_CODE', NVARCHAR(30), primary_key=True)
    Column('COMD_CODE', NVARCHAR(30), primary_key=True)
    Column('COMD_CDNM', NVARCHAR(200),nullable=False) 
    Column('COMD_ENNM', NVARCHAR(100)) 
    Column('CRTE_DATE', NVARCHAR(8),default="20170113") 
    Column('REF1_FILD', NVARCHAR(100)) 
    Column('REF2_FILD', NVARCHAR(100)) 
    Column('REF3_FILD', NVARCHAR(100)) 
    Column('REF4_FILD', NVARCHAR(100)) 
    Column('SORT_ORDR', NUMBER(precision=5, scale=0, asdecimal=False)) 
    Column('INST_USID', NVARCHAR(30),default="ADMIN")
    Column('INST_DATE', default=db.func.current_timestamp())
    Column('UPDT_USID', NVARCHAR(30),default="ADMIN")
    Column('UPDT_DATE', default=db.func.current_timestamp(), onupdate=db.func.current_timestamp())

    
if __name__ == '__main__':

    F = '''
       COMM_CODE , COMM_CDNM , SYST_CODE , CDGB_CODE
     , RE1F_DESC , RE1T_CODE , RE2F_DESC , RE2T_CODE
     , RE3F_DESC , RE3T_CODE , RE4F_DESC , RE4T_CODE
     , ISET_YSNO , INST_DATE , UPDT_USID , UPDT_DATE
     '''
    stmt = '''
SELECT 
       COMM_CODE , COMM_CDNM , SYST_CODE , CDGB_CODE
     , RE1F_DESC , RE1T_CODE , RE2F_DESC , RE2T_CODE
     , RE3F_DESC , RE3T_CODE , RE4F_DESC , RE4T_CODE
     , ISET_YSNO , INST_DATE , UPDT_USID , UPDT_DATE
FROM TM_CODEXH
    '''
    rs = db.session.query(TM_CODEXH).from_statement(stmt).all()
    for x in rs:
        print(x)
    

   
    
    
'''
desc SF_GET_REFXFILD;
select comm_code, comd_code, comd_cdnm, crte_date , ref1_fild, ref2_fild, ref3_fild, ref4_fild, inst_usid, inst_date, updt_usid, updt_date , sort_ordr from tm_codexd;


        SELECT  /* TMMA0020.SEARCH00 공통코드 마스터 조회 */
                COMM_CODE   /*공통코드*/
               ,COMM_CDNM   /*공통코드명*/
               ,SYST_CODE   /*시스템코드*/
               ,CDGB_CODE   /*코드구분코드*/
               ,COCD_LNTH   /*세부코드길이*/
               ,RE1F_DESC   /*보조1필드설명*/
               ,SF_GET_REFXFILD('REXT_CODE', RE1T_CODE, '1') AS RE1T_CODE   /*보조1필드입력형태코드*/
               ,SF_GET_REFXFILD('REXT_CODE', RE1T_CODE, '2') AS RE1O_CODE   /*보조1필드출력형태코드*/
               ,RE1F_CMCD   /*보조1필드공통코드*/
               ,RE2F_DESC   /*보조2필드설명*/
               ,SF_GET_REFXFILD('REXT_CODE', RE2T_CODE, '1') AS RE2T_CODE   /*보조2필드입력형태코드*/
               ,SF_GET_REFXFILD('REXT_CODE', RE2T_CODE, '2') AS RE2O_CODE   /*보조2필드출력형태코드*/
               ,RE2F_CMCD   /*보조2필드공통코드*/
               ,RE3F_DESC   /*보조3필드설명*/
               ,SF_GET_REFXFILD('REXT_CODE', RE3T_CODE, '1') AS RE3T_CODE   /*보조3필드입력형태코드*/
               ,SF_GET_REFXFILD('REXT_CODE', RE3T_CODE, '2') AS RE3O_CODE   /*보조3필드출력형태코드*/
               ,RE3F_CMCD   /*보조3필드공통코드*/
               ,RE4F_DESC   /*보조4필드설명*/
               ,SF_GET_REFXFILD('REXT_CODE', RE4T_CODE, '1') AS RE4T_CODE   /*보조4필드입력형태코드*/
               ,SF_GET_REFXFILD('REXT_CODE', RE4T_CODE, '2') AS RE4O_CODE   /*보조4필드출력형태코드*/
               ,RE4F_CMCD   /*보조4필드공통코드*/
               ,RE5F_DESC   /*보조5필드설명*/
               ,SF_GET_REFXFILD('REXT_CODE', RE5T_CODE, '1') AS RE5T_CODE   /*보조5필드입력형태코드*/
               ,SF_GET_REFXFILD('REXT_CODE', RE5T_CODE, '2') AS RE5O_CODE   /*보조5필드출력형태코드*/
               ,RE5F_CMCD   /*보조5필드공통코드*/
               ,RE6F_DESC   /*보조6필드설명*/
               ,SF_GET_REFXFILD('REXT_CODE', RE6T_CODE, '1') AS RE6T_CODE   /*보조6필드입력형태코드*/
               ,SF_GET_REFXFILD('REXT_CODE', RE6T_CODE, '2') AS RE6O_CODE   /*보조6필드출력형태코드*/
               ,RE6F_CMCD   /*보조6필드공통코드*/
               ,RE7F_DESC   /*보조7필드설명*/
               ,SF_GET_REFXFILD('REXT_CODE', RE7T_CODE, '1') AS RE7T_CODE   /*보조7필드입력형태코드*/
               ,SF_GET_REFXFILD('REXT_CODE', RE7T_CODE, '2') AS RE7O_CODE   /*보조7필드출력형태코드*/
               ,RE7F_CMCD   /*보조7필드공통코드*/
               ,RE8F_DESC   /*보조8필드설명*/
               ,SF_GET_REFXFILD('REXT_CODE', RE8T_CODE, '1') AS RE8T_CODE   /*보조8필드입력형태코드*/
               ,SF_GET_REFXFILD('REXT_CODE', RE8T_CODE, '2') AS RE8O_CODE   /*보조8필드출력형태코드*/
               ,RE8F_CMCD   /*보조8필드공통코드*/
               ,RE9F_DESC   /*보조9필드설명*/
               ,SF_GET_REFXFILD('REXT_CODE', RE9T_CODE, '1') AS RE9T_CODE   /*보조9필드입력형태코드*/
               ,SF_GET_REFXFILD('REXT_CODE', RE9T_CODE, '2') AS RE9O_CODE   /*보조9필드출력형태코드*/
               ,RE9F_CMCD   /*보조9필드공통코드*/
               ,R10F_DESC   /*보조10필드설명*/
               ,SF_GET_REFXFILD('REXT_CODE', R10T_CODE, '1') AS R10T_CODE   /*보조10필드입력형태코드*/
               ,SF_GET_REFXFILD('REXT_CODE', R10T_CODE, '2') AS R10O_CODE   /*보조10필드출력형태코드*/
               ,R10F_CMCD   /*보조10필드공통코드*/
               ,REMK_100X   /*비고100*/
               ,ISET_YSNO   /*초기세팅여부*/
          FROM TM_CODEXH where comm_code = 'MLSFC_PRDLST_CD'
          
          
          ;


update TM_CODEXH
set
RE1F_DESC = '보조1'
, RE1T_CODE = '03'
where comm_code = 'MLSFC_PRDLST_CD';

commit;


select * from TM_CODEXH where comm_code = 'MLSFC_PRDLST_CD';

select * from TM_CODEXD where comm_code = 'MLSFC_PRDLST_CD';
          
select * from TM_CODEXD where comm_code in (select comm_code from tm_codexh where syst_code is null);

select * from TM_CODEXH where comm_code = 'ENF2_CODE' and RE1T_CODE = '03';


select * from TM_CODEXD where comm_code = 'ENF2_CODE';


select comm_code, comm_cdnm, syst_code, cdgb_code , re1f_desc , re1t_code, iset_ysno , inst_date, updt_usid, updt_date from tm_codexh;


-- cdgb_code = 1 : 업무 / 0:시스템
-- iset_ysno = 1 : 초기셋팅여부 or NULL
SELECT COMM_CODE, COMM_CDNM, SYST_CODE, CDGB_CODE , RE1F_DESC , RE1T_CODE, RE2F_DESC , RE2T_CODE, RE3F_DESC , RE3T_CODE, RE4F_DESC , RE4T_CODE, ISET_YSNO , INST_DATE, UPDT_USID, UPDT_DATE FROM TM_CODEXH; 


'''    
    
    
    
    
    
    
