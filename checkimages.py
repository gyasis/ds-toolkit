import os
import sys
from PIL import Image

if len(sys.argv) < 2:
    print("Error : Too Few Arguments \nUsage : python del_unwanted.py $1 \nwhere $1 = \"dir_name\" ( where images are stored ) \nRequires absolute directory path")
    sys.exit()
dirname=sys.argv[1]
cnt=0
for filename in os.listdir(dirname):
    try:
        img=Image.open(dirname+"/"+filename)
    except OSError:
        print("FILE: ", filename, "is corrupt!")
        cnt+=1
        os.remove(dirname+"/"+filename)
print("Successfully Completed Operation! Files Corrupted are ", cnt)