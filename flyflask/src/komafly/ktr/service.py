
from komafly.cmm.application import *

from komafly.ktr.model import User,TM_ISSUE02

import numpy as np
import pandas as pd
from functools import partial
 
def select_issue02_all(group_code):
    try:
        rs = db.session \
            .query(TM_ISSUE02) \
            .filter(TM_ISSUE02.grp_code == group_code) \
            .all()
        return rs
    except Exception as e:
        return []

def load_cnames():
    query = '''
SELECT COLUMN_NAME
     , COMMENTS
FROM
  (SELECT LOWER(COLUMN_NAME) AS COLUMN_NAME
        , COMMENTS
   FROM ALL_COL_COMMENTS
   WHERE REGEXP_LIKE(TABLE_NAME,'^TM_|^EX_|^IF_|^PR_|^CP_|^TT_|^CF_|^MK_|^CT_|^AV_|^IC_|^CU_')  AND COMMENTS IS NOT NULL  )
GROUP BY COLUMN_NAME
       , COMMENTS
ORDER BY COLUMN_NAME    
    '''
    try:
        df = pd.read_sql(query,con=db.engine)
        dic = df.to_dict(orient='list')
        return dict(zip(dic['column_name'],dic['comments']))
    except Exception as e:
        print("ERROR - ",e)
        return {}

def get_cnames():
    cnames = getattr(g,'_cnames',None)
    if cnames is None:
        cnames = g._cnames = load_cnames()
    return cnames

def create_temptable():
    isExist = False
    try:
        print("===========================")
        rs = db.engine.execute("select * from all_tables where table_name = 'TMP_COLS'")
        for x in rs:
            print(x)
            isExist = True
        print("===========================")
    except Exception as e:
        print(e)
        pass
    
    head = " INSERT INTO TMP_COLS " if isExist else " CREATE GLOBAL TEMPORARY TABLE TMP_COLS ON COMMIT PRESERVE ROWS AS "
    try:
        q = '''
SELECT COLUMN_NAME
     , COMMENTS
FROM
  (SELECT LOWER(COLUMN_NAME) AS COLUMN_NAME
        , COMMENTS
   FROM ALL_COL_COMMENTS
   WHERE REGEXP_LIKE(TABLE_NAME,'^TM_|^EX_|^IF_|^PR_|^CP_|^TT_|^CF_|^MK_|^CT_|^AV_|^IC_|^CU_') AND COMMENTS IS NOT NULL )
GROUP BY COLUMN_NAME
       , COMMENTS
ORDER BY COLUMN_NAME
        '''
        q = head + q
        db.engine.execute(q)
        rs = db.engine.execute('select * from tmp_cols').fetchall()
        for x in rs:
            print(rs)
    except Exception as e:
        print(e)
        pass

if __name__ == '__main__':
    cnames = load_cnames()
    print(cnames)
    print("--------------")

if __name__ == '__main__2':
    engine = db.engine
    q = '''
    SELECT 
RCEPT_ID, ISGN_ORGINL_RCEPT_ID, RCEPT_TOTAMT, 
   DECSN_TOTAMT, RCPMNY_SE_CD, RCEPT_PROGRS_STTUS_CD, 
   AGREM_ID, REGISTER_ID, REGIST_DT, 
   CHANGER_ID, CHANGE_DT, INDUST_CL_CD
FROM CP_BNCR002
    '''
    df = pd.read_sql(q,con=db.engine)
    df = df.fillna('')
    df.rename(columns=get_cnames(),inplace=True)
    
    print(df.head(3))