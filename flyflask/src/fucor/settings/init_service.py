# -*- coding: utf-8 -*-
from fucor.application import *
from fucor.cod.models import *

from sqlalchemy import create_engine

'''
http://flask-sqlalchemy.pocoo.org/2.1/models/
'''
def inspect_table_name(engine): 
    from sqlalchemy import inspect 
    inspector = inspect(engine) 
    for table_name in inspector.get_table_names(): 
        yield table_name.upper()

erp = create_engine(ERP_ORACLE, echo=False)




def create_params(name, descr):
    
    params = CM_PARAMS()
    params.name = "{}.{}".format('PARAM',name)  # @UndefinedVariable
    params.descr = descr # @UndefinedVariable
    params.add_param("String","name","이름")
    params.add_param("int","age","나이")
    params.apply_param() 
    
    db.session.add(params)
    db.session.commit()
    
    return params


def init_coder():

    m = CM_METHOD()
    m.method_id = "CMMC002.SEARCH00"
    m.descr = "XXXX"
    m.name = "SEARCH01"
    m.package = 'ktr.cot'
    m.table_name = 'TM_CODEXD'
    m.params_name = "PARAM.{}".format(m.method_id)

    create_params(m.method_id,"parameter")
    create_params(m.method_id+"1","parameter")

    coder = CM_CODER("백승우","공통모듈 개발(신규) **#@#$@#% ","ktr.cot") 
    coder.cls_name = "CMMC002"
    coder.cm_method = [ m ]
    
    print(coder)
    db.session.add(coder)
#     db.session.add(m)
    db.session.commit()


def drop_tables():
#     CM_PARAMS.query.drop_all()
    db.metadata.drop_all(db.engine,tables=[
        CM_PARAMS.__table__
        , CM_PARAM.__table__
        , CM_CODER.__table__
        , CM_METHOD.__table__
    ])

if __name__ == '__main__':
#     drop_tables()
    #init_db()
    init_coder()
#     init_table()
