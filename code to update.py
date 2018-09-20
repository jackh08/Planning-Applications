# -*- coding: utf-8 -*-
"""
Created on Wed Aug 01 19:02:19 2018

@author: jackh
"""

"""
Checks csv of last update. Gets details of those and finds new items.
"""

import pandas as pd

mydir = 'C:\\Users\\jackh\\OneDrive\\Documents\\Projects\\Python scraping\\Storage Update\\Update August\\Previous update\\'
previous = pd.read_excel(mydir + 'Storage June ll.xlsx')

previous['url'].head() 
 

# First get updated details of list above.

# add code to first filter out non standard counties!!!

previous_standard = previous.loc[[i not in ['SDCC','Fingal','DCC','Cork County','Wexford','Donegal','Kerry'] for i in previous['Council']]]

updated_details_standard = get_details_all(previous_standard)


# Readd latitude and longitude
updated_details_ll = updated_details_standard.astype(str).merge(previous_standard[['Application Number','Latitude','Longitude','Council']].astype(str),how = 'left',left_on = 'Application Number',right_on = 'Application Number')
updated_details_ll.head()


short_details_app2

"""
Remember to update non-standard details
"""
previous.loc[[i in ['SDCC','Fingal','DCC','Cork County','Wexford','Donegal','Kerry'] for i in previous['Council']]]['url']





counties = ['Carlow',
             'Cavan',
             'Cork City',
             'Clare',
             'Galway',
             'Kildare',
             'Kilkenny',
             'Laois',
             'Leitrim',
             'Limerick',
             'Louth',
             'Longford',
             'Mayo',
             'Meath',
             'Monaghan',
             'Offaly',
             'Roscommon',
             'Sligo',
             'Tipperary',
             'Waterford',
             'Westmeath',
             'Wicklow']



short_details_app2.shape

terms = ['energy storage', 'battery storage']

mydir = 'C:\\Users\\jackh\\OneDrive\\Documents\\Projects\\Python scraping\\Storage Update\\Update August\\'
previous_all = pd.read_csv(mydir + 'Last check Solar.csv')

short_details_app2 = get_short_details_all_counties(terms,counties)



short_details_fingal_app2 =  get_short_details_all_terms_Fingal(terms)
short_details_app2 = short_details_app2.append(short_details_fingal_app2)
short_details_dcc_app2 =  get_short_details_all_terms_DCC(terms)
short_details_app2 = short_details_app2.append(short_details_dcc_app2)

short_details_app2.shape

new_items = pd.DataFrame(columns = short_details_app2.columns)
changed_items = pd.DataFrame(columns = short_details_app2.columns)

new_items = []

for i in short_details_app2['Application Number'].values:
    print(i)
    if str(i).lstrip('0') in [str(j) for j in previous_all['Application Number']]:
        print('Found')
    else:
        print('Not Found')
        new_items.append(i)

len(new_items)

new_rows = pd.DataFrame(columns = short_details_app2.columns)

for i in new_items:
    i = str(i).lstrip('0')
    row = short_details_app2.loc[short_details_app2['Application Number']==i]
    new_rows = new_rows.append(row)        

for i in new_rows['url']:
    print(i)


# now filter new rows
# remember to paste into history document as well

new_rows.to_csv

# 65 items with search term solar not previously found.
mydir = 'C:\\Users\\jackh\\OneDrive\\Documents\\Projects\\Python scraping\\Storage Update\\Update August\\'
short_details_app2['Keep application'] = 'N'

# add y if already in db
yn = []
for i in short_details_app2['Application Number'].values:
    print(i)
    if str(i).lstrip('0') in [str(j) for j in updated_details_ll['Application Number']]:
        print('Found')
        yn.append('Found')
    else:
        print('Not Found')
        yn.append('Not Found')
        
short_details_app2['Keep application'] = 'N'


short_details_app2 = short_details_app2.loc[[i=='Not Found' for i in yn]].reset_index()



short_details_app2.to_csv(mydir + 'New items to filter.csv',index = None)


new_rows_filtered = pd.read_csv(mydir + 'New items to filter.csv')

new_items_short = new_rows_filtered[new_rows_filtered['Keep application']=='y']


# fix limerick url

limerick = new_items_short.loc[new_items_short['Council']=='Limerick Local Authorities'].reset_index(drop=True)
limerick['url'] = [i.replace('www.eplanning','eplan.limerick') for i in limerick['url']]
new_items_short = new_items_short.loc[new_items_short['Council']!='Limerick Local Authorities'].append(limerick).reset_index(drop=True)

# 6 new items found
# get long details

url = new_items_short['url'][0]

new_items_long = get_details_all(new_items_short)



test_long_coords = get_long_lat(new_items_long)


full_output = updated_details_ll.append(test_long_coords)
full_output.shape
full_output = full_output.drop_duplicates()
 """
 Remember to check errors from above urls and recheck for new items
 
 """
cols = pd.read_excel('C:\\Users\\jackh\\OneDrive\\Documents\\Projects\\Python scraping\\Outputs\\Columns.xlsx',index = None,encoding='utf-8').columns.tolist()

full_output=full_output.loc[:,cols]

full_output.to_excel(mydir+'storage updated aug before manual checks.xls',index = None)

#
# then check cork updates for cork, wexford, fingal, donagal
#check weekly lists for above also
