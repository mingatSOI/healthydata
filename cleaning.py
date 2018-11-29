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

##Not actually useful to coerce to a format - no easy way to distinguish between centuries 
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
path2 = '/mnt/c/Linux/healthydata/data'
file_list = os.listdir(path2)

#Set acceptable values to pass as string instead of null
#Default values are:
na_default = ['', '#N/A', '#N/A N/A', '#NA', '-1.#IND', '-1.#QNAN', '-NaN', '-nan', '1.#IND', '1.#QNAN', 'N/A', 'NA', 'NULL', 'NaN', 'n/a', 'nan', 'null']

na_names = ['', '#N/A', '#N/A N/A', '#NA', '-1.#IND', '-1.#QNAN', '-NaN', '-nan', '1.#IND', '1.#QNAN', 'N/A', 'n/a']

#Create rules for cleaning columns up front regarding null values
disciplines = ['HH', 'OE', 'FF', 'SS', 'HP', 'FUNF']

def create_dicts(dis, file_name):
    df = pd.read_csv('/mnt/c/Linux/healthydata/data/CSV files/' + file_name, encoding='latin1', nrows=1)
    cols = list(df.columns)
    dis = dict()
    for i in cols:
        if i == 'Athlete_Name' or i == 'Athlete_First_Name':
            dis[i] = na_names
        else:
            dis[i] = na_default
    return dis

hh = create_dicts('hh', 'HH_2007-2018.csv')
ss = create_dicts('ss', 'SS_2007-2018.csv')
oe = create_dicts('oe', 'OE_2007-2018.csv')
hp = create_dicts('hp', 'HP_2007-2018.csv')
funf = create_dicts('funf', 'FUNF_2007-2018.csv')
ff = create_dicts('ff', 'FF_2007-2018.csv')

#Clean it all!

def main_clean(dis, file_name, output):
    data = pd.read_excel('/mnt/c/Linux/healthydata/data/'+file_name, encoding = 'utf8', keep_na = False, na_values = dis)
    data['Athlete_Name_Clean'] = data['Athlete_Name'].apply(clean_names)
    data['Athlete_First_Name_Clean'] = data['Athlete_First_Name'].apply(clean_names)
    #data['Athlete_DOB_Clean'] = data['Athlete_Date_Of_Birth'].apply(clean_dob)
    data['Country_clean'] = data['Country'].apply(clean_country)
    data.to_csv('/mnt/c/Linux/healthydata/data/clean_csv/'+output, index=False)
    print(f"{file_name} is done")

main_clean(hh, 'HH_2007-2018.xlsx', 'HH_2007-2018.csv')
main_clean(ss, 'SS_2007-2018.xlsx', 'SS_2007-2018.csv')
main_clean(oe, 'OE_2007-2018.xlsx', 'OE_2007-2018.csv')
main_clean(hp, 'HP_2007-2018.xlsx', 'HP_2007-2018.csv')
main_clean(funf, 'FUNF_2007-2018.xlsx', 'FUNF_2007-2018.csv')
main_clean(ff, 'FF_2007-2018.xlsx', 'FF_2007-2018.csv')
