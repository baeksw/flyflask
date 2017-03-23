# -*- coding: utf-8 -*-
import os
import xlrd
import pandas as pd
import numpy as np

filename = "(20170112) 접수화면_기초코드.xlsx"
# base_dir = os.path.dirname(os.path.abspath(__file__))
base_dir ="C:/Users/USER/Documents/카카오톡 받은 파일/"
target_file = (os.path.join(base_dir,filename))
print("target_file = {}".format(target_file))


converters = {
'컬럼명' : str
,'컬럼코멘트' : str
,'코드' : str
,'코드설명' : str
,'보조1필드' : str
,'보조2필드' : str
,'보조3필드' : str
,'보조4필드' : str
,'REF3_FILD' : str
,'REF4_FILD' : str
,'COMM_CDNM' : str
,'RE1F_DESC' : str
,'RE2F_DESC' : str
,'RE3F_DESC' : str
,'RE4F_DESC' : str
}
xl = pd.ExcelFile(target_file,converters=converters)
names = xl.sheet_names

df = xl.parse(names[0],converters=converters)

df = df[['컬럼명','컬럼코멘트','코드','코드설명','보조1필드']]
renames = {
    '컬럼명' : 'COMM_CODE'
    ,'컬럼코멘트' : 'COMM_CDNM'
    , '코드' : 'COMD_CODE'
    , '코드설명' : 'COMD_CDNM'
    , '보조1필드' : 'REF1_FILD'
    , '보조2필드' : 'REF2_FILD'
    , '보조3필드' : 'REF3_FILD'
    , '보조4필드' : 'REF4_FILD'
}

df.rename(columns=renames, inplace=True)

tmp = np.NaN
tmp2 = np.NaN
for index, row in df.iterrows():
    if row['COMM_CODE'] is not np.NaN and tmp is np.NaN:
        tmp = row['COMM_CODE']
        tmp2 = row['COMM_CDNM']
    elif row['COMM_CODE'] is not np.NaN and tmp is not np.NaN:
        tmp = row['COMM_CODE']
        tmp2 = row['COMM_CDNM']
    elif row['COMM_CODE'] is np.NaN and tmp is not np.NaN:
        row['COMM_CODE'] = tmp
        row['COMM_CDNM'] = tmp2
        
    pass

print("---------------------")

def clip_master():
    df = df.drop_duplicates(['COMM_CODE'], keep='last')
    df[['COMM_CODE','COMM_CDNM']].to_clipboard(excel=True)

def clip_detail():
    df[['COMM_CODE','COMD_CODE','COMD_CDNM']].to_clipboard(excel=True)


























