# list all recursive files in directory and their size in pandas dataframe
# in megabytes(self,dirpath):
# %%
%matplotlib inline
import os
import pandas as pd
import matplotlib.pyplot as plt

def list_all_files(path, target_size=100):
    filepath = []
    files =[]
    for (dirpath, dirnames, filenames) in os.walk(path):
        for file in filenames:
            filepath.append(os.path.join(dirpath, file))
            files.append(file)
    df = pd.DataFrame(files, columns=['File'])
    
    def convert_to_MB(x):
        try:
            return round(os.path.getsize(x)/1024/1024,2)
        except:
            x = 0
            return x
    df['path'] = filepath
    df['MB'] = df['path'].apply(lambda x: convert_to_MB(x))
    # df = df.sort_values(by=['MB'], ascending=False)
    print(len(df))
    #  create piechart of files and filesize
    def create_piechart():  
        df.MB.plt.pie(df.MB, labels=df.File, autopct='%1.1f%%', shadow=True, startangle=90)
        return plt.show()
    
    create_piechart()
  
    # df = df.reset_index(drop=True)
    
    # #create pivot table with MB > 100 MB
    def large_files(df):
        return df[df['MB'] > target_size]
    df = large_files(df)
    df = df.reset_index(drop=True)
    return df
# %%

# %%
root_dir = '/home/gyasis/Public/GD/Google Drive/Collection/Kaggle_competitions-'
data = list_all_files(root_dir)
data.head(20)
filenames = data['File']
print(filenames)
# %%
git_path = (root_dir + '/' + '.gitignore')
print(git_path)
myfile = open(git_path, 'w+') 

print(type(myfile))
myfile.read()
# %%

for i, line in enumerate(filenames):
    print(filenames[i])
    myfile.write(filenames[i] + '\n')

myfile.readlines()
# %%
myfile.close()

# %%
# check contents of file
def open_file(filename):
    with open(filename,'r') as f:
        print(f.read())
        return f.read()

open_file(git_path)
# %%
