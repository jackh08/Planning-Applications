# -*- coding: utf-8 -*-
"""
Created on Thu May 24 14:05:31 2018

@author: jackh
"""

# test scripts

"""
Fingal and DCC can be treated as the normal sites as they both give
reduced descriptions on search pages. SDCC must be searched with more specific 
search terms as it accesses each application individually.

For now full details can be accessed from the normal sites. Fingal and DCC must be 
checked manually.
"""

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


terms = ['battery storage','energy storage']

# First get short details for each county
short_details=get_short_details_all_counties(terms,counties)
short_details.shape

short_details_fingal =  get_short_details_all_terms_Fingal(terms)
short_details = short_details.append(short_details_fingal)
short_details_dcc =  get_short_details_all_terms_DCC(terms)
short_details = short_details.append(short_details_dcc)

# terms_sdcc = ['solar farm','energy storage']
# short_details_sdcc=get_short_details_SDCC(terms_sdcc) this function is broken 





# filter out unnecessary ones
test_short_filtered = filter_all(short_details)



# Filter out fingal
without_fingal = test_short_filtered.loc[test_short_filtered['Council']!='Fingal']

# Get rest of details
test_long = get_details_all(without_fingal)


test_long = get_details_all(test_short_filtered)

# If response error on any fix here
url_missed = 'http://www.eplanning.ie/OffalyCC/AppFileRefDetails/17199/0'
missing = get_details_url(url_missed)
test_long=test_long.append(missing)

# Fix limerick URLs and get details
limerick = test_short_filtered.loc[test_short_filtered['Council']=='Limerick Local Authorities'].reset_index()
limerick['url'] = [i.replace('www.eplanning','eplan.limerick') for i in limerick['url']]
limerick_long = get_details_all(limerick)
test_long = test_long.append(limerick_long)

# Get Fingal short details, check these manually as function is not done
fingal_short = test_short_filtered.loc[test_short_filtered['Council']=='Fingal'].reset_index()

for i in fingal_short['url']:
    print i
    print '\n\n'

# fingal_long - for now do manually as new function needs to be done for this

test_long.to_csv('C:\\Users\\jackh\\OneDrive\\Documents\\Projects\\Python scraping\\Storage Update\\Storage June.csv',index = None,encoding='utf-8')

# Manually add Cork, Kerry and Fingal long details

long_details = pd.read_csv('C:\\Users\\jackh\\OneDrive\\Documents\\Projects\\Python scraping\\Storage Update\\Storage June.csv',encoding='latin1')

previous_details = pd.read_csv('C:\\Users\\jackh\\OneDrive\\Documents\\Projects\\Python scraping\\Storage\\Updated storage applications ll.csv')

# Check to see if any in previous version were missed
a=0
for i in previous_details['Planning_ref']:
    if str(i) not in [str(j) for j in long_details['Application Number']]:
        print i
        a+=1

# Add them as here if so
url_1 = 'http://www.eplanning.ie/MeathCC/AppFileRefDetails/AA160553/0'
url_2 = 'http://www.eplanning.ie/MeathCC/AppFileRefDetails/LB171475/0'



long_details = pd.read_csv('C:\\Users\\jackh\\OneDrive\\Documents\\Projects\\Python scraping\\Outputs\\full list 12 June.csv')

long_to_add = get_details_url(url_2)
long_details = long_details.append(long_to_add)

# reset index and save
long_details = long_details.reset_index()
long_details.to_csv('C:\\Users\\jackh\\OneDrive\\Documents\\Projects\\Python scraping\\Storage Update\\Storage June.csv',index = None,encoding='utf-8')



# Coordinates ...
test_long_coords = get_long_lat(long_details)





cols = pd.read_excel('C:\\Users\\jackh\\OneDrive\\Documents\\Projects\\Python scraping\\Outputs\\Columns.xlsx',index = None,encoding='utf-8').columns.tolist()

out=test_long_coords.loc[:,cols]

out.to_csv('C:\\Users\\jackh\\OneDrive\\Documents\\Projects\\Python scraping\\Storage Update\\Storage June ll.csv',index = None,encoding='utf-8')


test_long_coords_fixed = pd.read_csv('C:\\Users\\jackh\\OneDrive\\Documents\\Projects\\Python scraping\\Storage Update\\Storage June ll.csv',encoding='utf-8')





save_as_kml(test_long_coords_fixed)


