# %%
def precheck():

    import glob
    import os

    files = glob.glob('**', recursive=True)
    files = reversed(sorted(files, key=os.path.getsize))

    for item in files:
        size = os.path.getsize(item)
        if os.path.isfile(item):
            if (size >= 1048576):
                print(item + "->\t\t\t\t\t", (os.path.getsize(item) / 1048576),
                      "MB")
            elif (size >= 1024):
                print(item + "->\t\t\t\t\t", (os.path.getsize(item) / 1024),
                      "KB")
            else:
                print(item + "->\t\t\t\t\t", (os.path.getsize(item)), "bytes")

precheck()
# %%

# %%
