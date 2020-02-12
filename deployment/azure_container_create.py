import os
import sys
from azure_storage import *

"""
Deployment script to create a storage container on azure,
for the storage of default datasets & user uploaded files
"""

DATASETS_PATH = './datasets/'

if __name__ == '__main__':
    try:
        create_container("gdat")
    except Exception as e:
        print(e)
        sys.exit(-1)
    # upload all default datasets
    for filename in os.listdir(DATASETS_PATH):
        with open(os.path.join(DATASETS_PATH, filename), "rb") as data:
            try:
                create_blob("gdat", filename, data)
            except Exception as e:
                print(e)
                sys.exit(-1)
    print("Container creation completed.")
    sys.exit(0)
