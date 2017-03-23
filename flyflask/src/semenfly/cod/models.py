from fucor.application import *
from time import localtime, strftime
from pip.commands.show import search_packages_info
from alembic.ddl.base import add_column

# Define a base model for other database tables to inherit
class Base(db.Model):
    __abstract__  = True
    #id        = db.Column(db.Integer,nullable=False, primary_key=True)
    create_dt = db.Column(db.DateTime,  default=db.func.current_timestamp())
    update_dt = db.Column(db.DateTime,  default=db.func.current_timestamp(),
                                           onupdate=db.func.current_timestamp())

class CM_CODER(Base):
    __tablename__ = "CM_CODER"
    cls_name  = db.Column(db.String(100), nullable=True, primary_key=True) # 코드 설명
    package   = db.Column(db.String(100), nullable=False) # 코드 설명
    author    = db.Column(db.String(50), nullable=False, info={"description":'코드 작성자'}) # 코드 작성자
    descr     = db.Column(db.String(200), nullable=False) # 코드 설명
    since     = db.Column(db.String(10), nullable=False,default=strftime('%Y-%m-%d', localtime())) # 코드 설명
    version   = db.Column(db.String(10), nullable=False,default="1.0.0") # 코드 설명
    cm_method = db.relationship('CM_METHOD', backref="CM_CODER", lazy="dynamic")

    def __init__(self, author, descr, package):
        self.author, self.descr,self.package = author, descr, package

    def __repr__(self):
        return '<CM_CODER {} {} {} {}>'.format(self.author, self.package, self.version, self.since)    


class CM_METHOD(Base):
    __tablename__ = "CM_METHOD"
    method_id   = db.Column(db.String(50), primary_key=True) # classname + name
    descr       = db.Column(db.String(200), nullable=False) # 코드 설명
    name        = db.Column(db.String(100), nullable=False) # 코드 설명
    since       = db.Column(db.String(10), nullable=False,default=strftime('%Y-%m-%d', localtime())) # 코드 설명
    returning   = db.Column(db.String(100), nullable=False,default='NA') # 코드 설명
    exception   = db.Column(db.String(100), nullable=False,default='NA') # 코드 설명
    example     = db.Column(db.String(1000), nullable=False,default='example') # 코드 설명
    # Define Relationship
    cls_name = db.Column(db.String(100), db.ForeignKey('CM_CODER.cls_name'))
    table_name = db.Column(db.String(50), db.ForeignKey('CM_TABLE.name'))
    params_name = db.Column(db.String(50), db.ForeignKey('CM_PARAMS.name'))

    def __repr__(self):
        return '<CM_METHOD {} {} {} {}>'.format(self.name, self.since, self.returning, self.descr)
'''
    def __init__(self, name, descr, action_type, since, returning, exception, example):
        self.name, self.descr, self.action_type, self.since = name, descr, action_type, since
        self.returning, self.exception, self.example = returning, exception, example

class CM_PARAM_MAP(Base):
    __tablename__ = "CM_PARAM_MAP"
    param_id = db.Column(db.Integer,db.ForeignKey('CM_PARAM.id'))
    params_name = db.Column(db.String(100),db.ForeignKey('CM_PARAMS.name'))
'''

param_map = db.Table('CM_PARAM_MAP' \
    , db.Model.metadata
    , db.Column('param_id',db.Integer,db.ForeignKey('CM_PARAM.id'))  \
    , db.Column('params_name',db.String(100),db.ForeignKey('CM_PARAMS.name')) \
)  

class CM_PARAM(Base):
    __tablename__ = "CM_PARAM"
    id        = db.Column(db.Integer, nullable=False, primary_key=True)
    name        = db.Column(db.String(100), nullable=False)
    data_type   = db.Column(db.String(100), nullable=False)
    descr       = db.Column(db.String(100), nullable=False, default="NA") 

    def __repr__(self):
        return '<CM_PARAM {} {} {} method_id : {}>'.format(self.name, self.data_type, self.descr )



class CM_PARAMS(Base):
    __tablename__ = "CM_PARAMS"
    name        = db.Column(db.String(100),primary_key=True)
    descr       = db.Column(db.String(100), nullable=True) 
    cm_param   = db.relationship('CM_PARAM',secondary=param_map, backref="CM_PARAMS", lazy="dynamic")
    cm_method = db.relationship('CM_METHOD', backref="CM_PARAMS", lazy="dynamic")
                                
    buf = []
    
    def add_param(self,ptype, pname, pdesc):
        p = self.search_param(pname,ptype,pdesc) 
        if p:
            self.buf += [ p ]
    
    def apply_param(self):       
        self.cm_param = self.buf
        
    def search_param(self,pname, ptype,pdesc):
        try:
            p = db.session.query(CM_PARAM) \
                    .filter(and_(CM_PARAM.name == pname,CM_PARAM.data_type == ptype)) \
                    .one()
        except Exception as e:
            p = self.create_param(pname, ptype, pdesc)
        return p

    def create_param(self,pname,ptype,pdesc):
        try:
            p = CM_PARAM()
            p.name, p.data_type, p.descr = pname, ptype, pdesc
            db.session.add(p)
            db.session.commit()
            return p
        except Exception as e:
            return None

    def __repr__(self):
        return '<CM_PARAM {} {} {} desc : {}>'.format(self.name, self.data_type,self.descr )


table_map = db.Table('CM_TABLE_MAP' \
    , db.Model.metadata
    , db.Column('column_id',db.Integer,db.ForeignKey('CM_COLUMN.id'))  \
    , db.Column('table_name',db.String(100),db.ForeignKey('CM_TABLE.name')) \
) 
 
class CM_COLUMN(Base):
    __tablename__ = "CM_COLUMN"
    id         = db.Column(db.Integer, nullable=False, primary_key=True)
    name       = db.Column(db.String(50), nullable=False)
    descr      = db.Column(db.String(100), nullable=False) 
    data_type  = db.Column(db.String(50), nullable=False)

    def __repr__(self):
        return '<CM_METHOD {} {}>'.format(self.name, self.data_type )

class CM_TABLE(Base):
    __tablename__ = "CM_TABLE"
    name        = db.Column(db.String(50),primary_key=True)
    descr       = db.Column(db.String(100), nullable=True) 
    #method_id   = db.Column(db.String(50), db.ForeignKey('CM_METHOD.method_id'))
    cm_column   = db.relationship('CM_COLUMN',secondary=table_map, backref="CM_TABLE", lazy="dynamic")
    cm_method = db.relationship('CM_METHOD', backref="CM_TABLE", lazy="dynamic")
    buf = []
    
    def add_all_column(self,cols=[]):
        for x in cols:
            self.add_column(**x)
        self.apply_column()

    
    def add_column(self,pname, ptype, pdesc):
        p = self.search_column(pname,ptype,pdesc) 
        if p:
            self.buf += [ p ]
    
    def apply_column(self):       
        for x in self.buf:
#             self.cm_column = self.buf
            self.cm_column.append(x)
        
    def search_column(self,pname, ptype,pdesc):
        try:
            p = db.session.query(CM_COLUMN) \
                    .filter(and_(CM_COLUMN.name == pname,CM_COLUMN.data_type == ptype)) \
                    .one()
        except Exception as e:
            p = self.create_column(pname, ptype, pdesc)
        return p

    def create_column(self,pname,ptype,pdesc):
        try:
            p = CM_COLUMN()
            p.name, p.data_type, p.descr = pname, ptype, pdesc
            db.session.add(p)
            db.session.commit()
            return p
        except Exception as e:
            db.session.rollback()
            return None
    
    def __repr__(self):
        return '<CM_TABLE {} {}>'.format(self.name, self.method_id)







'''
# Define a User model
class User(Base):

    __tablename__ = 'auth_user'

    # User Name
    name    = db.Column(db.String(128),  nullable=False)

    # Identification Data: email & password
    email    = db.Column(db.String(128),  nullable=False,
                                            unique=True)
    password = db.Column(db.String(192),  nullable=False)

    # Authorisation Data: role & status
    role     = db.Column(db.SmallInteger, nullable=False)
    status   = db.Column(db.SmallInteger, nullable=False)

    # New instance instantiation procedure
    def __init__(self, name, email, password):

        self.name     = name
        self.email    = email
        self.password = password

def __repr__(self):
        return '<User %r>' % (self.name)    
'''