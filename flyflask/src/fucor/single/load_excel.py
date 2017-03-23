import os
import xlrd
import pandas as pd

filename = "공통코드_입력샘플.xlsx"
base_dir = os.path.dirname(os.path.abspath(__file__))
target_file = (os.path.join(base_dir,filename))


converters = {
'COMM_CODE' : str
,'COMD_CODE' : str
,'COMD_CDNM' : str
,'REF1_FILD' : str
,'REF2_FILD' : str
,'REF3_FILD' : str
,'REF4_FILD' : str
,'COMM_CDNM' : str
,'RE1F_DESC' : str
,'RE2F_DESC' : str
,'RE3F_DESC' : str
,'RE4F_DESC' : str
}

class ParseCodeExcel:
    def __init__(self,filename):
        self.xl = pd.ExcelFile(filename,converters=converters)
        self.names = self.xl.sheet_names
    def master(self,code=[]):
        print("code",code)
        tmp = None
        df = self.xl.parse(self.names[0],converters=converters)
        df = df.drop(df.index[[0]])
        if len(code) > 0:
            for x, g in df.groupby(['COMM_CODE']):
                if x in code:
                    if tmp is None:
                        tmp = g
                        print(1)
                    else:
                        print(x)
                        tmp = pd.concat([tmp,g],ignore_index=True)
                        print(tmp)
                        print("-------------------------")
                        tmp = tmp
                        
        if tmp is not None:
            return tmp
        return df
    
    def detail(self,code=None):
        tmp = None
        df = self.xl.parse(self.names[1],converters=converters)
        df = df.drop(df.index[[0]])
        if len(code) > 0:
            for x, g in df.groupby(['COMM_CODE']):
                if x.strip() in code:
                    if tmp is None:
                        tmp = g
                    else:
                        tmp = pd.concat([tmp,g],ignore_index=True)
        if tmp is not None:
            return tmp
        
        return df

pcExcel = ParseCodeExcel(target_file)       
        
def master(code):
    return pcExcel.master(code)
def detail(code):
    return pcExcel.detail(code)

