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

class CP_BNCR023(AutoLoadBase): __tablename__ = 'CP_BNCR023'
class CP_BNCR002(AutoLoadBase): __tablename__ = 'CP_BNCR002'


'''
## -------------------------------------------------------------------------------------
## STATEMENTS
## -------------------------------------------------------------------------------------
'''
# how do i get table skeltone information 
def test_get_table_info():
    tbl = CP_BNCR023.__table__
    for x in tbl.c:
        print (x.key)
        print (str(x.type))
        print(x.info)

def get_user_tables():
    buf = []
    with db.engine.connect() as f:
        r = f.execute("SELECT TABLE_NAME FROM USER_TABLES where Regexp_Like(Table_Name,'^EX_|^IF_|^PR_|^CP_|^TT_|^CF_|^MK_|^CT_|^AV_|^IC_|^CU_') ORDER BY TABLE_NAME")
        for x in r:
            buf.append(x[0])
    return buf


def test_alter_table():
    table_name = "CP_BNCR023"
    TPL = "ALTER TABLE {} MODIFY({} {});"
    tbl = Table(table_name,MetaData(db.engine),autoload=True)
    for x in tbl.c:
        if 'VARCHAR' in str(x.type):
            a = TPL.format(table_name, x.key.upper(), 'N{}'.format(str(x.type)) )
            print(a)
 
 
def alter_table_varchar2_nvarchar2(table_name):
    buf = []
    TPL = "ALTER TABLE {} MODIFY({} {});"
    tbl = Table(table_name,MetaData(db.engine),autoload=True)
    for x in tbl.c:
        if 'VARCHAR' in str(x.type):
#             a = TPL.format(table_name, x.key.upper(), 'N{}'.format(str(x.type)) )
            if 'NVARCHAR' not in str(x.type):
                buf.append("\n-- TABLE : " + table_name)
                a = TPL.format(table_name, x.key.upper(), str(x.type).replace('VARCHAR(','NVARCHAR2(') )
                buf.append(a)
    return "\n".join(buf)



def autoload_table(table_name=None,engine=None):
    table = Table(table_name,MetaData(engine),autoload=True)
    def decorator(function):
        def wrapper( *args, **kwargs):
            print("decorated..")
            kwargs.update({'table': table ,'table_name' : table_name})
            return function(*args,**kwargs)
        return wrapper
    try:
        return decorator
    finally:
        engine.dispose()


@autoload_table('CP_BNCR023',db.engine)
def test(table_name, table):
    TPL = "ALTER TABLE {} MODIFY({} {});"
    for x in table.c:
        if 'NVARCHAR' not in str(x.type):
            if 'VARCHAR' in str(x.type):
                a = TPL.format(table_name, x.key.upper(), 'N{}'.format(str(x.type)) )  # @UndefinedVariable
                print(a)


@autoload_table('TM_CODEXD',db.engine)
def table_columns(table_name, table):
    buf = []
    for x in table.c:
        buf.append(x)
    return buf


if __name__ == '__main__23222':
    buf = table_columns()
    print("\n".join([str(x.__repr__()) for x in buf]))

















if __name__ == '__main__':
    with open('./alter_table.txt','w') as f:
        for x in get_user_tables():
            body = alter_table_varchar2_nvarchar2(x)
            f.write(body)
            




if __name__ == '__main__2':
    rs = db.session.query(CP_BNCR002).all()
    for x in rs:
        print(x.rcept_id)


# http://www.haruair.com/blog/1695   
    
'''
한글이 들어간 컬럼 검사 
select table_name,column_name, REGEXP_REPLACE(column_name, '[a-zA-Z0-9_]+', '') from USER_TAB_COLUMNS where REGEXP_REPLACE(column_name, '[a-zA-Z0-9_]+', '') is not null;


SELECT TABLE_NAME
,COLUMN_NAME
, REGEXP_REPLACE(COLUMN_NAME, '[A-ZA-Z0-9_]+', '') 
FROM USER_TAB_COLUMNS WHERE 
REGEXP_REPLACE(COLUMN_NAME, '[A-ZA-Z0-9_]+', '') IS NOT NULL;

'''    
    
    
    
    
    
    
    
