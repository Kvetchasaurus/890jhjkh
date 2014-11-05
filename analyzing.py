from pandas import *
from numpy import *
from sklearn.metrics import *
import matplotlib.pyplot as plt
#from sklearn.ensemble import RandomForestClassifier
#from sklearn.tree import DecisionTreeClassifier
#from sklearn.cluster import AgglomerativeClustering
from scipy.spatial.distance import  pdist, squareform
from scipy.cluster.hierarchy import linkage, dendrogram, ward
import migration
import IO_Mysql

    # get data from local files
#A, numeric = migration.main()

    #get data from database
A, numeric = IO_Mysql.pandas_tables_from_db()


def create_symptoms_vector(symptoms_list, all_symptoms):
    '''creates a vector for individual symptom depending on its apearances in 
    all_symptoms'''

    SV = []
    for symptom in all_symptoms:
        if symptom in symptoms_list:
            SV.append(1)
        else:
            SV.append(0)
    return np.array(SV)
    
    


def calculate_similarities(symptoms_vector, numeric):
    '''calculates the number of symptoms from user generated list that relate 
    to individual diseases''' 
    
    matt_sim = []
    matched = []
    df = DataFrame(columns=['Disease','matched','matthews_sim'])

    for column in numeric.columns:
        val = numeric[column].values
        
        matched.append(sum(val * symptoms_vector))
        matt_sim.append(matthews_corrcoef(val,symptoms_vector))
        
    df['Disease'] = numeric.columns
    df['matched'] = matched
    df['matthews_sim'] = matt_sim
     
    return df


    
        
def get_all_diseases_with_symptoms(symptom_list,A):
    '''generates a list of diseases that relate to given symptoms'''
    
    disease_list = A[A.index.isin(A[A.Symptoms.isin(symptom_list)].drop_duplicates(subset='Disease') \
    .index.values)]['Disease'].values
    
    return disease_list
    
    

def get_all_symptoms_from_disease_list(disease_list,A):
    '''generates a symptom suggestion list from diseases that relate to given 
    set of symptoms'''
    symptom_list = A[A.Disease.isin(disease_list)]['Symptoms'].drop_duplicates().values
    
    return symptom_list
    
    


def merge_and_calculate(A,simi):
    ''' '''

    merged_A_simi = merge(A, simi, on = 'Disease')
    
    return merged_A_simi.drop_duplicates(subset = 'Symptoms')
    
    
    
def calculate_disease_distance(numeric):
    ''' '''
    ok = squareform(pdist(numeric.transpose(),metric=matthews_corrcoef))
    disease_distance = DataFrame(ok,index=numeric.columns,columns=numeric.columns)
    
    return disease_distance
    
    

def pair_wise(ab,cd):
    ''' '''
    return dist_disease.loc[ab,cd]


def calculate_rolling_distance(kk):
    ''' '''
    dl = kk.Disease.values
    dd = []
    for ii in range(len(dl) - 1):
        d1=dl[ii]
        d2=dl[ii+1]
        dist = pair_wise(d1,d2)
        dd.append(dist)
    dd.insert(0,0)
    kk['disease_distance'] = dd
    return kk 
    
def calculate_sum_distance(disease_list):
    ''' '''
    sum_dist = dist_disease.loc[disease_list,disease_list].sum()
    df = DataFrame(columns=['Disease','sum_distance'])
    df['Disease'] = sum_dist.index
    df['sum_distance'] = sum_dist.values
    
    return df



def random_rows(df, n):
    return df.ix[np.random.choice(df.index, n)]
    
    



   
    

def Symptoms(L):
    WagesI = (0.66,0.5,0.33)
    WagesII = (0.5,0.5,0.5)
    WagesIII = (0.33,0.5,0.66)

    symp_wek= create_symptoms_vector(L, numeric.index.values)
    
    simi = calculate_similarities(symp_wek,numeric)
    
    disease_list = get_all_diseases_with_symptoms(L,A)
    
    all_symptoms = get_all_symptoms_from_disease_list(disease_list,A)
    
    kk = merge_and_calculate(A,simi)
    
    kk = kk.sort(columns=['matthews_sim','Propability'], ascending = [0,0])
    
    #drop symptoms that are in L
    kk = kk[kk.Symptoms.isin(L) != 1]
    
    #ok = calculate_rolling_distance(kk)
    #
    #sum_dist = calculate_sum_distance(disease_list)
    #
    #abcd = merge(ok,sum_dist, on='Disease')
    
    if len(L)<3:
        WP,WMatt,WMatched = WagesI
        kk['master_score'] = ( (WP*kk['Propability'].values/100) +   (WMatt*kk['matthews_sim'])  + (WMatched*kk['matched']/len(L)) )
        kk = kk.sort(columns='master_score', ascending = False)[:25]
        rnd = random_rows(kk, 7)
        
    elif len(L)== 3:
        WP,WMatt,WMatched = WagesII
        kk['master_score'] = ( (WP*kk['Propability'].values/100) +   (WMatt*kk['matthews_sim'])  + (WMatched*kk['matched']/len(L)) )
        kk = kk.sort(columns='master_score', ascending = False)[:25]
        rnd = random_rows(kk, 7)
        
    else:
        WP,WMatt,WMatched = WagesIII
        kk['master_score'] = ( (WP*kk['Propability'].values/100) +   (WMatt*kk['matthews_sim'])  + (WMatched*kk['matched']/len(L)) )
        kk = kk.sort(columns='master_score', ascending = False)[:25]
        rnd = random_rows(kk, 7)
        
    return rnd,kk

   









