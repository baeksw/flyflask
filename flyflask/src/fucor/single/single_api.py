# -*- coding:utf-8 -*-
from fucor.single.single_base import *

from flask_bootstrap import Bootstrap
from Cython.Compiler.Naming import self_cname

DEV_ORACLE = "oracle+cx_oracle://ktrdb:dev4kotric@210.97.19.50:1521/orcl"
DEV_OWNER = 'KTRDB'

ERP_ORACLE = "oracle+cx_oracle://KTR_DEV:KTR12#@192.168.1.13:1521/orcl"
ERP_OWNER = 'KTR_DEV'

DB_URL = ERP_ORACLE
DB_OWNER = ERP_OWNER

# SQLITE3 = "sqlite:///D:/fucor_db.db"
SQLITE3 = "sqlite:///D:/single_db.db"

app = Flask(__name__)
app.root_path = os.path.dirname(os.path.abspath(__file__))
app.config['SQLALCHEMY_DATABASE_URI'] = SQLITE3
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

param_map = db.Table('CM_PARAM_MAP' \
    , db.Model.metadata
    , db.Column('param_id',db.Integer,db.ForeignKey('CM_PARAM.id'))  \
    , db.Column('params_name',db.String(100),db.ForeignKey('CM_PARAMS.name')) \
)  

class Base(db.Model):
    __abstract__  = True    
    @staticmethod
    def timestamp():
        return db.func.current_timestamp()
    
class CM_API(db.Model):
    __tablename__ = "CM_API"
    id           = db.Column(db.Integer, nullable=False, primary_key=True)
    api_descr    = db.Column(db.String(500),nullable=False)
    api_comment  = db.Column(db.String(500),nullable=False)
    api_sample   = db.Column(db.Text)
    methods      = db.Column(db.String(500)) # GET/POST/PUT/DELETE
    req_uri      = db.Column(db.String(1000)) # Call
    req_headers  = db.Column(db.String(1000))
    req_body     = db.Column(db.String(1000))
    res_headers  = db.Column(db.String(1000))
    res_body     = db.Column(db.Text)
    create_dt    = db.Column(db.DateTime,  default=Base.timestamp())
    update_dt    = db.Column(db.DateTime,  default=Base.timestamp(), onupdate=Base.timestamp()) 
    params_name  = db.Column(db.String(50), db.ForeignKey('CM_PARAMS.name'))

class CM_PARAMS(db.Model):
    __tablename__ = "CM_PARAMS"
    name        = db.Column(db.String(100),primary_key=True)
    descr       = db.Column(db.String(100), nullable=True) 
    create_dt   = db.Column(db.DateTime,  default=Base.timestamp())
    update_dt   = db.Column(db.DateTime,  default=Base.timestamp(), onupdate=Base.timestamp())                               
    cm_param    = db.relationship('CM_PARAM',secondary=param_map, backref="CM_PARAMS")
    cm_api      = db.relationship('CM_API', backref="CM_PARAMS")
    
    def __repr__(self):
        return '<CM_PARAM {} {} {} desc : {}>'.format(self.name, self.data_type,self.descr )


class CM_PARAM(db.Model):
    __tablename__ = "CM_PARAM"
    id           = db.Column(db.Integer, nullable=False, primary_key=True)
    param_name   = db.Column(db.String(100), nullable=False)
    param_desc   = db.Column(db.String(100), nullable=False,default="_NO_DESC_")
    param_value  = db.Column(db.String(100), nullable=False,default="_NO_VALUE_")
    data_type    = db.Column(db.String(100), nullable=False,default="_UNDEFINED_")
    location     = db.Column(db.String(100))
    extra_desc   = db.Column(db.String(100), nullable=False, default="NA") # etc
    description  = db.Column(db.String(100), nullable=False, default="NA") 
    create_dt = db.Column(db.DateTime,  default=Base.timestamp())
    update_dt = db.Column(db.DateTime,  default=Base.timestamp(), onupdate=Base.timestamp())    

    def set_parm(self, pname, pvalue):
        self.param_name = pname
        self.param_value = pvalue
        return self
    
    def __repr__(self):
        return '<CM_PARAM {} {} {}>'.format(self.param_name, self.data_type, self.param_desc )

'''
# ------------------------------------------------------------------------------
ROUTES
# ------------------------------------------------------------------------------
'''
@app.route("/")
def index():
    return render_template("api_page.html")

@app.route("/ora_dtypes")
def oracle_data_types(): 
    cm_params = db.session.query(CM_PARAMS).filter(CM_PARAMS.name == 'ORACLE_DATA_TYPES').one()
    buf = []
    for x in cm_params.cm_param:
        buf += [ dict([('param_name' , x.param_name),('param_value',x.param_value)]) ]
    return jsonify(buf)
        
def init_oracle_data_types():
    
    db.session.query(CM_PARAMS).filter(CM_PARAMS.name == 'ORACLE_DATA_TYPES').delete()
    params = CM_PARAMS()
    params.name = "ORACLE_DATA_TYPES"
    
    vParams = [
        CM_PARAM().set_parm("VARCHAR2", "VARCHAR2")
        , CM_PARAM().set_parm("NUMBER", "NUMBER")
        , CM_PARAM().set_parm("INTEGER", "INTEGER")
        , CM_PARAM().set_parm("DECIMAL", "DECIMAL")
        , CM_PARAM().set_parm("FLOAT", "FLOAT")
        , CM_PARAM().set_parm("CLOB", "CLOB")
        , CM_PARAM().set_parm("NVARCHAR", "NVARCHAR")
        , CM_PARAM().set_parm("CHAR", "CHAR")
    ]

    for param in vParams:
        params.cm_param.append(param)
    
    db.session.add(params)
    try:
        db.session.commit()
    except Exception as e:
        eprint(e)
        db.session.rollback()
        



if __name__ == '__main__xx':
#     init_oracle_data_types();
    cm_params = db.session.query(CM_PARAMS).filter(CM_PARAMS.name == 'ORACLE_DATA_TYPES').one()
    for x in cm_params.cm_param:
        print(x)

if __name__ == '__main__':
    app.run(debug=True)

if __name__ == '__main__1':
    db.metadata.drop_all(db.engine,tables=[
        CM_PARAMS.__table__
        , CM_PARAM.__table__
        , CM_API.__table__
    ])    
    db.create_all()

   
    
    
    
    
    
    
    
    
    
