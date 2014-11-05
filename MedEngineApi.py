from analyzing import  *


def MedEngine_API(list_of_symptoms, location):
    
    if (not list_of_symptoms) and (not location):
        return_list = []
    
    elif (not list_of_symptoms) and location:
        return_list = []
    
    else:
        a,b = Symptoms(list_of_symptoms)
        
        return_list = a['Symptoms'].tolist()
 
        
 
        
    return return_list


l = MedEngine_API(['headache'],['jkljlj'])
