# -*- coding: utf-8 -*-
"""
Created on Fri May 25 12:47:44 2018

@author: jackh
"""

"""
dublin city

short details

"""


# -*- coding: utf-8 -*-
"""
Created on Fri May 25 09:24:50 2018

@author: jackh
"""

"""
DCC - has description in short text so can treat as normal. No dates in short though.
Short details should slot in ok with main functions

TODO: long details function from url
"""



def get_short_details_all_terms_DCC(terms):
    
    
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
        term_details = initialize_search_DCC(term)
        df_out = df_out.append(term_details)
    
    
    return df_out



def initialize_search_DCC(term):
    """
    given a search term, specific county and link to search page returns info for all applications
    associated with term
    """
    search_page_link = 'http://www.dublincity.ie/swiftlg/apas/run/wphappcriteria.display'
    
    

    
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
    

    
    
    df = get_all_pages_DCC(br)  
    
    
    return df




def get_all_pages_DCC(br):
    """
    given browser on first page of search responses, returns df of all details
    on all pages
    TODO: exception handling, sleeps, prints on each server request
    
    """
    
    response = br.response()
    parser = BeautifulSoup(response, 'html.parser')
    page_links = ['http://www.dublincity.ie/swiftlg/apas/run/'+i['href'] for i in parser.find('div',{'id':'bodyContent'}).form.find_all('a', recursive=False)]


    
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
        df_out = parse_page_details_short_DCC(parser)
    except:
        print 'No info on page'
  
  
    for link in page_links:
        
        try:
            response = requests.get(link)
            parser = BeautifulSoup(response.content, 'html.parser')
            df_out = df_out.append(parse_page_details_short_DCC(parser))
            
        except :
            print link
            print 'Failed'
        
      
        sleep(np.random.uniform(2,5,1)[0])

    
    # parse details on each link
    # starting from current response!
    
    
    return df_out


def parse_page_details_short_DCC(parser):
    
    info_table = parser.find('table')
    


    urls = ['http://www.dublincity.ie/swiftlg/apas/run/'+i.find_all('td')[0].a['href'] for i in info_table.find_all('tr')[1:]]
    app_no = [i.find_all('td')[0].a.text for i in info_table.find_all('tr')[1:]]
    description = [i.find_all('td')[1].text.strip() for i in info_table.find_all('tr')[1:]]
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
                    'Council':'DCC'})

        
    
    
    return df_out

    

    
    
    
    





