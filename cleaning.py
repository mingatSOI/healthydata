import pandas as pd
from fuzzywuzzy import process
import os


#Apply to surname and firstname 
def clean_names(x):
    try:
        #lower case
        tmp = x.lower()
        #strip leading/trailing spaces
        tmp = tmp.strip()
        #Camel case if surname is more than 1 word, capitalize if just one word.
        clean = tmp.title()
        return clean
    except:
        pass

def clean_country(x):
    try:
        if 'USA' in x:
            if x == 'USA':
                return x
            elif x == 'USA_California':
                return 'California'
            else:
                y = x.split("USA_")[1]
                c = process.extractOne(y, cc_set)
                return c[0] #extractOne returns a tuple (result, score)
        elif x == 'Georgia':
            return 'Georgia Republic'            
        else: 
            c = process.extractOne(x, cc_set)
            if c[1] > 90:
                return c[0]
            else:
                return x
    except:
        pass

##Not actually useful to coerce to a format - no easy to distinguish between centuries 
##based on available HAS date input since it was a two-digit year format (dd-MonthAbrev-YY)
# def clean_dob(x):
#     """x is the DOB series"""
# 	cdob = pd.to_datetime(x, dayfirst=True, errors='raise')
# 	return cdob

# Official program and country names based on ALL available accreditation files at SOI
path1 = '/mnt/c/Linux/accreditation'
os.chdir(path1)

cc_filelist = os.listdir(path1)
cc_set = set() # list of correct country names

for file in cc_filelist:
    cc_year = pd.read_excel(file)
    cc_country = cc_year.Program.values
    cc_set.update(cc_country)

#Run cleaning functions 
path2 = '/mnt/c/Linux/healthydata/data/CSV files'
file_list = os.listdir(path2)

for file_name in file_list:
    data = pd.read_csv('/mnt/c/Linux/healthydata/data/CSV files/'+file_name, encoding = 'latin1')
    data['Athlete_Name_clean'] = data['Athlete_Name'].apply(clean_names)
    data['Athlete_First_Name_Clean'] = data['Athlete_First_Name'].apply(clean_names)
    #data['Athlete_DOB_Clean'] = data['Athlete_Date_Of_Birth'].apply(clean_dob)
    data['Country_clean'] = data['Country'].apply(clean_country)
    data.to_csv('/mnt/c/Linux/healthydata/data/clean_csv/'+file_name)
    print(f"{file_name} is done")