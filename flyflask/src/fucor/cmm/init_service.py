# -*- coding: utf-8 -*-
from fucor.application import *
from fucor.cod.models import CM_CODER,CM_METHOD

'''
http://flask-sqlalchemy.pocoo.org/2.1/models/
'''
def init_coder():
    coder = CM_CODER("백승우","공통모듈 개발","ktr.cmm") 
    print(coder)
    db.session.add(coder)
    db.session.commit()
    
if __name__ == '__main__':
    init_db()
#     init_coder()
