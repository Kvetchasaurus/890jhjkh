from sqlalchemy import *
from pandas import *
from migration import *



#send tables to db.
def pandas_tables_to_db():
    
    dl, sl, junction, numeric=main_for_db()
    
#    prepare table for sending
    sl = sl.astype(object).where(pd.notnull(sl), None)
    
    
    
    engine = create_engine('mysql://root:sorcery@173.194.254.76/testbazy', echo=False)
    conn = engine.raw_connection()
    
    
    
    dl.to_sql('disease_table',conn,flavor='mysql',if_exists = 'replace')
    sl.to_sql('symptoms_table',conn, flavor='mysql', if_exists = 'replace')
    junction.to_sql('junction_table', conn, flavor = 'mysql', if_exists = 'replace')
    numeric.to_sql('binary_table', conn, flavor='mysql', if_exists = 'replace')




def pandas_tables_from_db():
    
    ''' function downloads mysql data and converts to pandas frames merging hapens here'''
    

    engine = create_engine('mysql://root:sorcery@173.194.254.76/testbazy', echo=False)
#    meta = MetaData()
#    meta.reflect(bind = engine)
    
    table_names_in_db = inspect(engine).get_table_names()
#    disease_table = Table('disease_table', meta, autoload = True, autoload_with=engine)
#    symptoms_table = Table('symptoms_table', meta, autoload = True, autoload_with=engine)
#    binary_table = Table('binary_table', meta, autoload = True, autoload_with=engine)
#    junction_table = Table('junction_table', meta, autoload = True, autoload_with=engine)
#    Session = sessionmaker(bind=engine)
#     session = Session()
    
    disease_table = read_sql('disease_table', engine).drop('index', axis = 1)
    junction_table = read_sql('junction_table', engine).drop('index', axis = 1)
    binary_table = read_sql('binary_table', engine).drop('index', axis = 1)
    symptoms_table = read_sql('symptoms_table', engine).drop('index', axis = 1)
    
    merged = pd.merge(junction_table,symptoms_table, left_on = 'Symptoms', right_on = 'originSymptoms', how = 'inner')
    dis_merge = merge(merged,disease_table, on='group')
    tt=merge(dis_merge,symptoms_table,on='symptomsID')
    A = tt[['Symptoms','Disease','sort','Propability']]
    binary_table = create_01_matrix(A)
    full_merged_table = A
    
    return full_merged_table, binary_table
    
    
    
    
    
    
    
    






