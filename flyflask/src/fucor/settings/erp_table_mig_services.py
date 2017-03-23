
from fucor.application import *
from fucor.cmm.erp_util import ERP_TABLE_META
from fucor.cod.models import *


def add_cm_table(session, table_info):
    table = CM_TABLE()
    cols = table_info.get('columns')
    table.name = table_info.get('name') 
    table.descr = table_info.get('name') 
#     table.add_all_column(cols)
    session.add(table)
    for c in cols:
        p = search_column(session, **c)
        p = session.query(CM_COLUMN) \
                .filter(and_(CM_COLUMN.name == c['pname'],CM_COLUMN.data_type == c['ptype'])) \
                .one()
        table.cm_column.append(p)

def search_column(session, pname, ptype,pdesc):
    try:
        p = session.query(CM_COLUMN) \
                .filter(and_(CM_COLUMN.name == pname,CM_COLUMN.data_type == ptype)) \
                .one()
    except Exception as e:
        print("SEARCH",e)
        p = create_column(session, pname, ptype, pdesc)
    return p

def create_column(session,pname,ptype,pdesc):
    try:
        p = CM_COLUMN()
        p.name, p.data_type, p.descr = pname, ptype, pdesc
        session.add(p)
        session.commit()
        return p
    except Exception as e:
        print("CRE",e)
        session.rollback()
        return None
    

if __name__ == '__main__':
    db = SQLAlchemy(app,metadata=metadata)
    print("##############################")
    #print(db.session.begin(subtransactions=True))
    print("##############################")
    try:
        db.session.query(CM_TABLE).delete()
        db.session.query(CM_COLUMN).delete()
        db.session.commit()
    except Exception as e:
        db.session.rollback()
        
    with ERP_TABLE_META() as t:
        for x in t:
            add_cm_table(db.session,x)
#             break
        try:
            db.session.commit()
        except Exception as e:
            print(e)
            db.session.rollback()
#             db.session.flush()
    db.session.close()
    
