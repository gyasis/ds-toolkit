# %%
from pyforest import *
lazy_imports()
from faker import Faker




# %%
nr_of_customer = 1000
fake = Faker()

name=[]
iban=[]
dob=[]

for customers_id in range(nr_of_customer):
    name.append(fake.name())
    iban.append(fake.iban())
    dob.append(fake.date())
   
   
#combine lists into data_frame
def list_to_data_frame(name,iban,dob):
    df = pd.DataFrame({'name':name,'iban':iban,'dob':dob})
    return df

df = list_to_data_frame(name,iban,dob)




# %%
# create fake dataframe with Faker
def create_fake_dataframe(x):
    df = pd.DataFrame()
    df["class_name"] = np.random.randint(0,10, size=x)
    df["class_name"] = df["class_name"].astype(str)
    df["class_name"] = df["class_name"].str.replace("0","0")
    df["class_name"] = df["class_name"].str.replace("1","1")
    return df
    
    
    
    
    
# %%
# convert dataframe columns to ndarray and randomsample to get a random sample of the dataframe
def randomselect