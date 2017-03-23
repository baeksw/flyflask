
from fucor.application import *

from sqlalchemy import create_engine,Table

def query_col_comments(session, table_name):
    query_text = '''
SELECT 
    COLUMN_NAME, comments
FROM USER_COL_COMMENTS
WHERE comments IS NOT NULL
AND TABLE_NAME = :table_name    
    '''
    buf = []
    conn = session.connection()
    trans = conn.begin()
    try:
        rs = conn.execute(query_text, table_name=table_name)
        for x in rs:
            print(x[0])
            buf.append((x[0], x[1].split('\n')[0]))
        trans.commit()
        return dict(buf)
    except Exception as e:
        print("query_comment------------->>",e)
        trans.rollback()
#         trans.flush()
        return {}


class ERP_TABLE_META(object):
    
    engineType = ERP_ORACLE
    meta = MetaData()

    def __init__(self):
        self.erpEngine = create_engine(ERP_ORACLE, echo=False)        
        from sqlalchemy.orm import sessionmaker
        Session = sessionmaker(bind=self.erpEngine)
        self.ses = Session()

    def __enter__(self):
        table_names = ERP_TABLE_META.inspect_table_name(self.erpEngine)
        self.gg = self.__generate(table_names)
        return self.gg
    
    def __generate(self,table_names):
        for table_name in table_names:
            cmts = query_col_comments(self.ses,table_name)
            table = Table(table_name, self.meta, autoload=True, autoload_with=self.erpEngine)
            buf = []
            table_desc = {}
            table_desc['name'] = table_name
            table_desc['columns'] = []
            for i, x in enumerate(table.columns):
                d = {}
                key = str(x.key).upper()
                d['pname'] = key
                d['ptype'] = str(x.type)
                d['pdesc'] = cmts.get(key) if key in cmts else key
                buf.append(d)
            table_desc['columns'] = buf
            yield table_desc
                    
    def __exit__(self,*exc_info):
        self.erpEngine.dispose()
    
    @staticmethod
    def inspect_table_name(engine): 
        from sqlalchemy import inspect 
        inspector = inspect(engine) 
        for table_name in inspector.get_table_names(): 
            yield table_name.upper()

