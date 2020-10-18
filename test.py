################################################################################################################
# Setup and Package Import
################################################################################################################

# --------------------------------------------------------------------------------------------------------------
# Importing
# --------------------------------------------------------------------------------------------------------------

import os
# import pandas as pd
# import numpy as np
# import pickle
# import csv
# import json
# import matplotlib.pyplot as plt
# import seaborn as sns
import spacy
# sns.set()
# pd.options.display.float_format = '{:.2f}'.format

# --------------------------------------------------------------------------------------------------------------
# Getting Paths and Working Correct
# --------------------------------------------------------------------------------------------------------------

# print(os.getcwd()) 
# os.chdir("Change to your path if necessary")
coco_path = r"C:\Users\CocoL\Universität St.Gallen\STUD-Capstoneproject Tell 6 - General\Coding"
jona_path = "some ugly mac book path"
jonathan_path = r"/Users/jonathanebner/Universität St.Gallen/STUD-Capstoneproject Tell 6 - General"
leo_path = "some ugly mac book path"

################################################################################################################
# Loading Data
################################################################################################################

test_file_path = os.path.join(coco_path,"1-Data", 'test_data.txt')

with open(test_file_path) as f:
    first_record = f.readline() 
    
print(first_record)