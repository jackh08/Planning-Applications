# -*- coding: utf-8 -*-
"""
Created on Fri May 25 09:44:22 2018

@author: jackh
"""

"""
SDCC

TODO: amend so for a list of terms this first searches, then removes duplicates
then goes to each link.


"""

import requests
from bs4 import BeautifulSoup
import re
import pandas as pd
import mechanize
import numpy as np
from ipywidgets import widgets
from IPython.display import display
from time import sleep
import simplekml
"""
Site updated this is now broken!
"""




def get_short_details_SDCC(terms):
    """
    use very specific search terms
    """
    raw_input('\n\nUse very specific search terms, press enter to continue\n\n:')
    
    url = 'http://www.sdublincoco.ie/Planning/Applications'
    
    br = mechanize.Browser()
    br.set_handle_robots(False)
    
    links = []
    
    for term in terms:
        if term != '':
            print('Searching for "{0}"'.format(term))
            
            sleep(np.random.uniform(2,5,1)[0])
            br.open(url)

            # search for term
            br.form = list(br.forms())[0]  # use when form is unnamed
            br.form['ctl00$ContentPlaceHolder1$ctl00$Proposal'] = term
            br.submit(id  = "ctl00_ContentPlaceHolder1_ctl00_SearchApplications")

            last_page=False

            page=1
            while last_page==False:
                for link in br.links():
                    if link.text=='View More Details':
                        temp = 'http://www.sdublincoco.ie/' + link.url
                        links.append(temp)

                    if link.text=='Next':
                        next_url = 'http://www.sdublincoco.ie/'+link.url


                    if link.text=='Last':
                        last_url = 'http://www.sdublincoco.ie/'+link.url

                if last_url==next_url:
                    last_page = True
                

                sleep(np.random.uniform(2,5,1)[0])
                br.open(next_url)
                page += 1
                
    details = parse_details_SDCC(links)
    

    
    df_out = details[['Application Number',
                        'url',
                        'Applicant Name',
                        'Development Address',
                        'Planning Status',
                        
                        'Decision Type',
                        'Decision Due',
                        'Received Date',
                        'Decision Date'
                        ]]
    
    df_out['Short Description']=details['Description']
    df_out['Council'] = 'SDCC'
    
    return df_out
    



def get_long_details_SDCC(terms):
    """
    use very specific search terms
    """
    raw_input('\n\nUse very specific search terms, press enter to continue\n\n:')
    
    url = 'http://www.sdublincoco.ie/index.aspx?pageid=144'
    
    br = mechanize.Browser()
    br.set_handle_robots(False)
    
    links = []
    
    for term in terms:
        if term != '':
            print('Searching for "{0}"'.format(term))
            
            sleep(np.random.uniform(2,5,1)[0])
            br.open(url)

            # search for term
            br.form = list(br.forms())[0]  # use when form is unnamed
            br.form['ctl00$ContentPlaceHolder1$ctl00$Proposal'] = term
            br.submit(id  = "ctl00_ContentPlaceHolder1_ctl00_SearchApplications")

            last_page=False

            page=1
            while last_page==False:
                for link in br.links():
                    if link.text=='View More Details':
                        temp = 'http://www.sdublincoco.ie/' + link.url
                        links.append(temp)

                    if link.text=='Next':
                        next_url = 'http://www.sdublincoco.ie/'+link.url


                    if link.text=='Last':
                        last_url = 'http://www.sdublincoco.ie/'+link.url

                if last_url==next_url:
                    last_page = True
                

                sleep(np.random.uniform(2,5,1)[0])
                br.open(next_url)
                page += 1
                
    details = parse_details_SDCC(links)
    
    
    return details
    


def parse_details_SDCC(links):
    
    df_out  = pd.DataFrame({'Application Number':[],
                             'Appeal Notification':[],
                             'Appeal type':[],
                             'Appeal Submission Due date':[],
                             'Appeal Submission Sent Date':[],
                             'Appeal Decision':[],
                             'Appeal Decision Date':[],
                             'Appeal withdrawn':[],
                             'Appeal Dismissed':[],
                             'Appeal Reason':[],
                             
                             
                             
                             'Applicant Name':[],
                             'Applicant Address':[],
                             'Applicant Phone':[],
                             'Applicant Fax':[],
                             'Correspondance Address':[],
                             'Description':[],
                             'Development Address':[],
                             'Location Key':[],
                             'Development Name':[],
                             'Significant Case':[],
                             'Comments':[],
                             'Number of Conditions':[],
                             'Grant Date':[],
                             'Expiry Date':[],
        
                             'Application Type':[] ,
                             'Planning Status':[],
                             'Received Date':[],
                             'Decision Due':[],
                             'Validated':[],
                             'Invalidated':[],
                             'FI Requested Date':[],
                             'FI REceived Date':[],
                             'Withdrawn Date':[],
                             'Extend Date':[],
                             'Decision Type':[],
                             'Decision Date':[],
                             'Leave to Appeal':[],
                             'Appeal Date':[],
                             'Commenced Date':[],
                             'Submissions by':[],
                             'url':[]
                            
                             }      
        )
    
    for link in links:
        print link
        sleep(np.random.uniform(2,5,1)[0])
        
        try:
            response = requests.get(link)
        except Exception as e:
            print (e)
            print('Failed for '+link)
    
                
        content = response.content
        
        parser = BeautifulSoup(content, 'html.parser')
        
        row = pd.DataFrame(columns = df_out.columns,index=[0])
        
        row['url']=link
        
        row['Application Number']=parser.find_all('h2',{'class':'details-header'})[0].text.split()[3]
        
        
        
        details_list = parser.find('dl',{'class':'details-list'})
       
    
        
        for i in np.arange(0,len(details_list.find_all('dd'))):
            if bool(re.search('Date Received',parser.find_all('dt')[i].text)):
                row['Received Date'] = details_list.find_all('dd')[i].text.strip()
            
            if bool(re.search('Application Type',details_list.find_all('dt')[i].text)):
                row['Application Type'] = details_list.find_all('dd')[i].text.strip()
            
            if bool(re.search('Closing Date for Submissions',details_list.find_all('dt')[i].text)):
                 row['Submissions by'] = details_list.find_all('dd')[i].text.strip()
            
            if bool(re.search('Decision Due',details_list.find_all('dt')[i].text)):
                row['Decision Due'] = details_list.find_all('dd')[i].text.strip()
            
            if bool(re.search('Applicant',details_list.find_all('dt')[i].text)):
                row['Applicant Name'] = details_list.find_all('dd')[i].text.strip()
            if bool(re.search('Location',details_list.find_all('dt')[i].text)):
                row['Development Address'] = details_list.find_all('dd')[i].text.strip()
            if bool(re.search('Proposed Development',details_list.find_all('dt')[i].text.strip())):
                row['Description'] = details_list.find_all('dd')[i].text.strip()
        
        
        dec_list = parser.find_all('dl',{'class':'details-list'}) [1]
            
        for i in np.arange(0,len(dec_list.find_all('dd'))):
            
            if bool(re.search('Decision Date',dec_list.find_all('dt')[i].text)):
                row['Decision Date'] = dec_list.find_all('dd')[i].text.strip()
    
            if bool(re.search('Decision:',dec_list.find_all('dt')[i].text.strip())):
                row['Decision Type'] = dec_list.find_all('dd')[i].text
                
            if bool(re.search('Grant Date:',dec_list.find_all('dt')[i].text.strip())):
                row['Grant Date'] = dec_list.find_all('dd')[i].text
        
        
  
        
        
        
        
        
        df_out=df_out.append(row)
    
    return df_out
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    