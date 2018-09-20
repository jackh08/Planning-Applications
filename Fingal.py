# -*- coding: utf-8 -*-
"""
Created on Fri May 25 09:24:50 2018

@author: jackh
"""

"""
Fingal - has description in short text so can treat as normal. No dates in short though.
Short details should slot in ok with main functions

TODO: long details function from url
"""





def get_short_details_all_terms_Fingal(terms):
    
    
    df_out = pd.DataFrame({'Application Number' : [],
                        'url' : [],
                        'Applicant Name':[],
                        'Development Address':[],
                        'Planning Status':[],
                        'Short Description':[],
                        'Decision Type':[],
                        'Decision Due':[],
                        'Received Date':[],
                        'Decision Date':[],
                        'Council':[]})
    
    for term in terms:
        term_details = initialize_search_Fingal(term)
        df_out = df_out.append(term_details)
    
    
    return df_out



def initialize_search_Fingal(term):
    """
    given a search term, specific county and link to search page returns info for all applications
    associated with term
    """
    search_page_link = 'http://planning.fingalcoco.ie/swiftlg/apas/run/wphappcriteria.display'
    
    

    
    br = mechanize.Browser()
    br.set_handle_robots(False)
    
    try:
        br.open(search_page_link)  
        br.form = list(br.forms())[0]
        br.form['JUSTDEVDESC.MAINBODY.WPACIS.1'] = term
        br.submit()
        print('Search : '+term)
        print('Open seach page : '+search_page_link)
    except:
        print(search_page_link+' Not working')
    

    
    
    df = get_all_pages_Fingal(br)  
    
    
    return df



def get_all_pages_Fingal(br):
    """
    given browser on first page of search responses, returns df of all details
    on all pages
    TODO: exception handling, sleeps, prints on each server request
    
    """
    
    response = br.response()
    parser = BeautifulSoup(response, 'html.parser')
    links = ['http://planning.fingalcoco.ie/swiftlg/apas/run/'+i['href'] for i in parser.find_all('div',{'id':'apas_form_text'})[0].find_all('a')]
    
    df_out = pd.DataFrame({'Application Number' : [],
                        'url' : [],
                        'Applicant Name':[],
                        'Development Address':[],
                        'Planning Status':[],
                        'Short Description':[],
                        'Decision Type':[],
                        'Decision Due':[],
                        'Received Date':[],
                        'Decision Date':[],
                        'Council':[]})
    
    # loop through pages in browser and return parsed info
    # do this for each page
    
    # get link of each page
    try:
        df_out = parse_page_details_short_Fingal(parser)
    except:
        print 'No info on page'
    page = 1
  
    for link in links:
        try:
            response = requests.get(link)
            parser = BeautifulSoup(response.content, 'html.parser')
            df_out = df_out.append(parse_page_details_short_Fingal(parser))
        except :
            print '' + link + ' Failed'
        print(page)
        page+=1
        sleep(np.random.uniform(2,5,1)[0])

    
    # parse details on each link
    # starting from current response!
    
    
    return df_out


def parse_page_details_short_Fingal(parser):
    
    info_table = parser.find('table',{'class':'apas_tbl'})
    
    

    urls = ['http://planning.fingalcoco.ie/swiftlg/apas/run/'+i.find_all('td')[0].a['href'] for i in info_table.find_all('tr')[1:]]
    app_no = [i.find_all('td')[0].a.text for i in info_table.find_all('tr')[1:]]
    description = [i.find_all('td')[1].text for i in info_table.find_all('tr')[1:]]
    address = [i.find_all('td')[2].text.strip() for i in info_table.find_all('tr')[1:]]
    df_out = pd.DataFrame({'Application Number' : app_no,
                    'url' : urls,
                    'Applicant Name':None,
                    'Development Address':address,
                    'Planning Status':None,
                    'Short Description':description,
                    'Decision Type':None,
                    'Decision Due':None,
                    'Received Date':None,
                    'Decision Date':None,
                    'Council':'Fingal'})

        
    
    
    return df_out

    



def parse_details_Fingal(links):
    
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
        
        details_list = parser.find_all('p',{'class':'fieldset_data'})
        
        parser.find_all('h2')
        
        row['Application Number']=details_list[0].text.strip()
        row['Received Date'] = details_list[1].text.strip()
        row['Applicant Name']
        row['Development Address'] 
        row['Decision Date']
        
        
        row['Description']
        
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
    
    

    
    
    





