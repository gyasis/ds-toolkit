# %%
# %%
def precheck(x):

    import glob
    import os
    import pandas as pd
    
    files = glob.glob((x+'/*'), recursive=True)
    # files = reversed(sorted(files, key=os.path.getsize))
   
    filename = []
    filesize = []
    totalsize = 0
    for item in files:
        try:
            size = os.path.getsize(item)
            totalsize += size
            if os.path.isfile(item):
                if (size >= 10485760):
                    # print(item + "->\t\t\t\t\t", (size / 1048576),
                        # "MB")
                    filename.append(item)
                    filesize.append(size / 1048576)
              
        except:
            # print('Warning!! Unrecognizable filetype', item)                   
            filename.append("WARNING!!! ---->"+item)
            filesize.append(0)
            
    totalsize = totalsize / 1048576
    filename.append('Total MB: ')
    filesize.append(totalsize)
    df = pd.DataFrame(list(zip(filename, filesize)),
               columns =['File', 'MB'])
    df = df.sort_values(by=['MB'], ascending=False)
    return df

# %%

# %%
