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
<<<<<<< Updated upstream
coco_path = r"C:\Users\CocoL\Universität St.Gallen\STUD-Capstoneproject Tell 6 - General\Coding"
jona_path = r"/Users/jhoff/Universität St.Gallen/STUD-Capstoneproject Tell 6 - Dokumente/General/Coding"
jonathan_path = r"/Users/jonathanebner/Universität St.Gallen/STUD-Capstoneproject Tell 6 - General/Coding"
leo_path = "some ugly mac book path"
=======

# Coco
# path = r"C:\Users\CocoL\Universität St.Gallen\STUD-Capstoneproject Tell 6 - General\Coding"
# Jona
# path = r"/Users/jhoff/Universität St.Gallen/STUD-Capstoneproject Tell 6 - Dokumente/General/Coding"
# Giovanni
# path = r"/Users/jonathanebner/Universität St.Gallen/STUD-Capstoneproject Tell 6 - General"
# Leo
path = r"/Users/Leonidas/Universität St.Gallen/Capstone Tell 6/Coding"
>>>>>>> Stashed changes

################################################################################################################
# Loading Data
################################################################################################################

test_file_path = os.path.join(coco_path,"1-Data", 'test_data.txt')

with open(test_file_path) as f:
    first_record = f.readline() 
    
print(first_record)
print("Hallo Jona, wie gehts? top")