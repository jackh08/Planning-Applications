# -*- coding: utf-8 -*-
"""
Created on Tue Jun 12 14:50:50 2018

@author: jackh
"""

"""
This applications simply searches the main pages and reports links where there
are new applications or applications have changed.

"""
mydir = 'C:\\Users\\jackh\\OneDrive\\Documents\\Projects\\Python scraping\\Application 2\\'
previous = pd.read_csv(mydir + 'Last check Solar.csv')

counties = ['Carlow']

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


terms = ['solar']

short_details_app2 = get_short_details_all_counties(terms,counties)
short_details_fingal_app2 =  get_short_details_all_terms_Fingal(terms)
short_details_app2 = short_details_app2.append(short_details_fingal_app2)
short_details_dcc_app2 =  get_short_details_all_terms_DCC(terms)
short_details_app2 = short_details_app2.append(short_details_dcc_app2)

# terms_sdcc = ['solar farm','energy storage']
# short_details_sdcc=get_short_details_SDCC(terms_sdcc) this function is broken 

# Cork county...
# Kerry
# Wexford
# Donegal

new_items = pd.DataFrame(columns = short_details_app2.columns)
changed_items = pd.DataFrame(columns = short_details_app2.columns)

new_items = []

for i in short_details_app2['Application Number']:
    print(i)
    if str(i).lstrip('0') in [str(j) for j in previous['Application Number']]:
        print('Found')
    else:
        print('Not Found')
        new_items.append(i)

new_rows = pd.DataFrame(columns = short_details_app2.columns)

for i in new_items:
    i = str(i).lstrip('0')
    row = short_details_app2.loc[short_details_app2['Application Number']==i]
    new_rows = new_rows.append(row)        

for i in new_rows['url']:
    print(i)


# Now look for changed items

previous_accepted.columns

previous_accepted = previous.loc[previous['Keep application'] != 'N']

previous_accepted

row = previous_accepted.iloc[292]

for index, row in previous_accepted.iterrows():
    if row['Application Number'] in [str(j) for j in short_details_app2['Application Number']]:
        #print(row['Application Number']+' found')
        
        temp = short_details_app2.loc[short_details_app2['Application Number']==row['Application Number']]
        try:
            if row['Planning Status'] != temp['Planning Status'][0]:
                pass
                #print(row['Application Number'])
                #print(row['Planning Status'])
                #print(temp['Planning Status'])
        except Exception as e:
            #print(e)
            print('error on: ')
            print(index)
            
            
        













