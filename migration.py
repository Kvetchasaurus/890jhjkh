import pandas as pd
import json
from pprint import pprint
from pandas.io import sql
import pandas.io.gbq
from pandas import *
import csv
import random




def ff(symp):
    
    symp = str(symp)
    if isinstance(symp,str):
        return symp.lower()
    
    
def splitting(symptoms_string):
    list_of_symptoms = symptoms_string.split('|')
    return list_of_symptoms    



def replaceP(s):
    n = s.replace('%','')
    n=n.replace(',','.')
    
    return n
    
 
def repl(st):
    st = st.replace('{','|').replace('}','|').split('|')
    return st   
    

def junction_from_dict(d_dict,d_dict2):
    fn = 'bla'+str(random.randint(1,1000))
    f = open(fn,'w')
    f.write('1000$jkljkl$random\n')
    for i in d_dict2:
        c = 0        
        for j in range(len(d_dict2[i])):
            c  += 1
            ss = ("%s$%s$%d\n") %(i,d_dict[i][j].strip(),c)
            f.write(ss)
               
    f.close()
    
    return fn



        
def create_01_matrix(full_merged_table):
    
    r = full_merged_table.Symptoms.unique()
    c = full_merged_table.Disease.unique()
    df = DataFrame(np.zeros((len(r),len(c))),index = r, columns = c)
    
    for ii in c:
        df.loc[full_merged_table[full_merged_table.Disease==ii]['Symptoms'].tolist(),ii] = 1
        
        
    return df


    

    
def main():
    
    wd = 'C:/DataNew/'
    main_data = 'data.csv'
    diseaselist = 'DiseaseList.xlsx'
    symptomsplit = 'symptomSplit.xlsx'   
    
    
    dl = pd.read_excel(wd + diseaselist, columns =['Disease','Propability','URL'])
    sl = pd.read_excel(wd + symptomsplit)
    main = pd.read_csv(wd + main_data)
    
    dl['Propability'] = dl['Propability'].apply(replaceP).astype(float)
    sl['originSymptoms'] = sl['originSymptoms'].apply(ff)
    
    d = pd.merge(dl, main, on ='URL', how = 'inner')
    
    d_dict = d['Symptoms'].apply(repl)
    d_dict2 = d_dict.to_dict()
    
    fn = junction_from_dict(d_dict,d_dict2)
    
    junction = pd.read_csv(fn, sep = '$')
    junction.columns = ['group','Symptoms','sort']
    junction['Symptoms'] = junction['Symptoms'].apply(ff)
    
    new_dl = DataFrame(columns=['Disease','Propability','URL'])
    new_dl['Disease'] = d['Disease_x']
    new_dl['Propability'] = d['Propability']
    new_dl['URL'] = d['URL']
    new_dl['group'] = new_dl.index
    
    
    merged = pd.merge(junction,sl, left_on = 'Symptoms', right_on = 'originSymptoms', how = 'inner')
    
    
    dis_merge = merge(merged,new_dl, on='group')
    
    
    
    tt=merge(dis_merge,sl,on='symptomsID')
    
    A = tt[['Symptoms','Disease','sort','Propability']]
    
  
    
    ok = create_01_matrix(A)
    
    return A,ok


def main_for_db():
    
    wd = 'C:/DataNew/'
    main_data = 'data.csv'
    diseaselist = 'DiseaseList.xlsx'
    symptomsplit = 'symptomSplit.xlsx'   
    
    
    dl = pd.read_excel(wd + diseaselist, columns =['Disease','Propability','URL'])
    sl = pd.read_excel(wd + symptomsplit)
    main = pd.read_csv(wd + main_data)
    
    dl['Propability'] = dl['Propability'].apply(replaceP).astype(float)
    sl['originSymptoms'] = sl['originSymptoms'].apply(ff)
    
    d = pd.merge(dl, main, on ='URL', how = 'inner')
    
    
    d_dict = d['Symptoms'].apply(repl)
    d_dict2 = d_dict.to_dict()
    
    fn = junction_from_dict(d_dict,d_dict2)
    
    junction = pd.read_csv(fn, sep = '$')
    junction.columns = ['group','Symptoms','sort']
    junction['Symptoms'] = junction['Symptoms'].apply(ff)
    
    new_dl = DataFrame(columns=['Disease','Propability','URL'])
    new_dl['Disease'] = d['Disease_x']
    new_dl['Propability'] = d['Propability']
    new_dl['URL'] = d['URL']
    new_dl['group'] = new_dl.index
    
    
    merged = pd.merge(junction,sl, left_on = 'Symptoms', right_on = 'originSymptoms', how = 'inner')
    
    
    dis_merge = merge(merged,new_dl, on='group')
    
    
    
    tt=merge(dis_merge,sl,on='symptomsID')
    
    A = tt[['Symptoms','Disease','sort','Propability']]
    
  
    
    ok = create_01_matrix(A)
    
    return new_dl, sl, junction, ok





#symp_wek= create_symptoms_vector(['skin redness','tallness'], ok.index.values)
#
#A[A.index.isin(A[A.Symptoms.isin(L)].drop_duplicates(subset='Disease').index.values)]['Disease'].values
#    
#A.drop_duplicates(subset=['Disease']).drop_duplicates(subset='Symptoms')
#    
#d.loc[A[A.Disease=='Diarrhea']['Symptoms'].tolist(),'Diarrhea']






