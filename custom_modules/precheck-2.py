# list all recursive files in directory and their size in pandas dataframe
# in megabytes(self,dirpath):
# %%

import os
import pandas as pd

def list_all_files(path):
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
    df = df.reset_index(drop=True)
    
    # #create pivot table with MB > 100 MB
    def large_files(df):
        return df[df['MB'] > 100]
    df = large_files(df)
    return df

# %%
root_dir = '/home/gyasis/Public/GD/Google Drive/Collection/Kaggle_competitions-'
data = list_all_files(root_dir)
data.head(20)


# %%
filenames = data['File']
# %%
git_path = (root_dir + '/' + '.gitignore')
print(git_path)
def read_text(filename):
    with open(filename, 'a+') as myfile:
        return myfile.read()
    
new_git = read_text(git_path)
# new_git.writelines(filenames)
new_git
# %%

        
