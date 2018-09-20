# -*- coding: utf-8 -*-
"""
Created on Thu May 24 10:42:45 2018

@author: jackh
"""

# All functions
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

standard_counties = ['Carlow',
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

def filter_all(df):
    df = df.drop_duplicates()
    
    df['Keep application'] = 'N'
    
    df.to_csv('C:\\Users\\jackh\\OneDrive\\Documents\\Projects\\Python scraping\\Filter\\Manual Check.csv',index=None,encoding='utf-8')
    
    print(
"""
  \nCSV file has been saved in C:\\Users\\jackh\\OneDrive\\Documents
  \\Projects\\Python scraping\\Filter\\Manual Check.csv'.
  \n\nPlease open file, Change "N" to "y" for desired files,
  save AND EXIT the file and press return. If desired also check that address 
  format is suitable for google maps API at this stage
"""
          )
    
    raw_input("Press Enter when ready")

    df = pd.read_csv('C:\\Users\\jackh\\OneDrive\\Documents\\Projects\\Python scraping\\Filter\\Manual Check.csv')
    
    """
    try:
        past = pd.read_csv('C:\\Users\\jackh\\OneDrive\\Documents\\Projects\\Python scraping\\Filter\\Past responses\\Past responses.csv')
        past = past.append(df)
        past.to_csv('C:\\Users\\jackh\\OneDrive\\Documents\\Projects\\Python scraping\\Filter\\Past responses\\Past responses.csv',index=None)
    except exception as e:
        print('Issue saving past data\n\n'+e)
        """
        
    df = df.loc[df['Keep application']=='y']
    
    
    
    return df

def get_short_details_all_counties(terms,counties):
    
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
    
    links = {'Carlow':'http://www.eplanning.ie/CarlowCC/SearchExact/Description',
             'Cavan':'http://www.eplanning.ie/CavanCC/SearchExact/Description',
             'Clare':'http://www.eplanning.ie/ClareCC/SearchExact/Description',
             'Cork City':'http://planning.corkcity.ie/searchexact',
             'Galway':'http://www.eplanning.ie/GalwayCC/SearchExact/Description',
             'Kildare':'http://www.eplanning.ie/KildareCC/SearchExact/Description',
             'Kilkenny':'http://www.eplanning.ie/KilkennyCC/SearchExact/Description',
             'Laois':'http://www.eplanning.ie/LaoisCC/SearchExact/Description',
             'Leitrim':'http://www.eplanning.ie/LeitrimCC/SearchExact/Description',
             'Limerick':'http://eplan.limerick.ie/SearchExact/Description',
             'Louth':'http://www.eplanning.ie/LouthCC/SearchExact/Description',
             'Longford':'http://www.eplanning.ie/LongfordCC/SearchExact/Description',
             'Mayo':'http://www.eplanning.ie/MayoCC/SearchExact/Description',
             'Meath':'http://www.eplanning.ie/MeathCC/SearchExact/Description',
             'Monaghan':'http://www.eplanning.ie/MonaghanCC/SearchExact/Description',
             'Offaly':'http://www.eplanning.ie/OffalyCC/SearchExact/Description',
             'Roscommon':'http://www.eplanning.ie/RoscommonCC/SearchExact/Description',
             'Sligo':'http://www.eplanning.ie/SligoCC/SearchExact/Description',
             'Tipperary':'http://www.eplanning.ie/TipperaryCC/SearchExact/Description',
             'Waterford':'http://www.eplanning.ie/WaterfordCCC/SearchExact/Description',
             'Westmeath':'http://www.eplanning.ie/WestmeathCC/SearchExact/Description',
             'Wicklow':'http://www.eplanning.ie/WicklowCC/SearchExact/Description',
             'SDCC':'http://www.sdublincoco.ie/index.aspx?pageid=144'
                     }
    
    for county in counties:
        county_details = get_short_details_all_terms(terms,links[county],county)
        df_out = df_out.append(county_details)
        print(county + ' done')
        
    return df_out
    

def get_short_details_all_terms(terms,search_page_link,county):
    """
    given list of terms and a search page link returns info for all applications
    for all terms
    """
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
        try:
            term_details = initialize_search(term,search_page_link,county)
            df_out = df_out.append(term_details)
        except:
            print('error with : ' + term + ' in ' + county)
    
    
    
    return df_out


def initialize_search(term,search_page_link,county):
    """
    given a search term, specific county and link to search page returns info for all applications
    associated with term
    """
   
    
    if county in standard_counties:
    
        br = mechanize.Browser()
        br.set_handle_robots(False)
        
        try:
            br.open(search_page_link)  
            br.form = list(br.forms())[1]
            br.form['TxtDevdescription'] = term
            br.submit()
            #print('Search : '+term)
            #print('Open seach page : '+search_page_link)
        except:
            print(search_page_link+' Not working')
    

    

    
    df = get_all_pages(br,county)  
    
    
    return df



def get_all_pages(br,county):
    """
    given browser on first page of search responses, returns df of all details
    on all pages
    TODO: exception handling, sleeps, prints on each server request
    
    """
    
    
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
    last_page = False
    
    pages=0
    while not last_page:
        
        
        
        resp = br.response() 
        try:
            details = parse_page_details(resp)
            df_out = df_out.append(details)
        except:
            print('Error parsing page')
        
        
        
        last_page = True
        next_page_link = None
        
        
        #print(parser.find_all('li',{'class':'PagedList-skipToNext'}))
        for link in br.links():
            if link.text==u'\xbb':    
                next_page_link = link
        
        if next_page_link != None:
            br.follow_link( next_page_link )
            pages+=1
            #print('Next Page')
            last_page=False
        
        
        sleep(np.random.uniform(2,5,1)[0])
    #print(str(pages)+' Pages scraped')
    return df_out
            

    
def parse_page_details(response):
    """
    given response of search page details returns all details on 1 page
    TODO: exception handling!!!
    """
    parser = BeautifulSoup(response, 'html.parser')
    
    info_table = parser.find_all('table')[0]
    
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
    
    # for each tr...
    for i in info_table.find_all('tr')[1:]:
    
        try:
            File_number = i.find_all('td')[0].a.text
        except Exception as e:
            print('File Number not found')
            File_number = None
        try:
            
            #TODO: FIX link for limerick - www.ie.eplan or something.
            
            
            Link = 'http://www.eplanning.ie'+i.find_all('td')[0].a['href']
            Application_status = i.find_all('td')[1].text
            Decision_due_date =  i.find_all('td')[2].text
            Decision_date =  i.find_all('td')[3].text
            Decision = i.find_all('td')[4].text
            Received_date = i.find_all('td')[5].text
            Applicant_Name = i.find_all('td')[6].text
            Development_address = i.find_all('td')[7].text
            Short_desc = i.find_all('td')[8].text
            Local_Auth = i.find_all('td')[9].text
        except:
            print('Error getting info for '+File_number)
        
        try:
            row = pd.DataFrame({'Application Number' : File_number,
                                'url' : Link,
                                'Applicant Name':Applicant_Name,
                                'Development Address':Development_address,
                                'Planning Status':Application_status,
                                'Short Description':Short_desc,
                                'Decision Type':Decision,
                                'Decision Due':Decision_due_date,
                                'Received Date':Received_date,
                                'Decision Date':Decision_date,
                                'Council':Local_Auth},index = [0])
        except:
            print('Error appending dataframe')
        
        df_out = df_out.append(row)
    return df_out





def get_details_all(dataframe):
    
    #TODO: ensure naming consistency for links etc.
    urls = dataframe['url'] .tolist()
    url=urls[0]
    try:
        out = get_details_url(url)
        print('success on :'+url)
    except:
        print 'Error on : '+url
        
    for url in urls[1:]:
        
        try:
            out = out.append(get_details_url(url))
            print('success on :'+url)
        except:
            print 'Error on : '+url
        sleep(np.random.uniform(2,5,1)[0])
    return out



url2 = 'http://www.redcafe.net/threads/diego-godin.440693/'
def get_details_url(url):
    
    
    
    try:
        response = requests.get(url)
    except Exception as e:
        print (e)
        print('Failed for '+url)
    
    row = parse_details_response(response,url)

    return row


def parse_details_response(response,url):
       

    content = response.content

    parser = BeautifulSoup(content, 'html.parser')
       
    # Get info from details table
    Details_table = parser.find_all('div',id = 'Details')[0]
    
    App_no = Details_table.find_all('td')[0].text.strip()
    Application_type = Details_table.find_all('td')[2].text.strip()
    Planning_status = Details_table.find_all('td')[3].text.strip()
    Received_date = Details_table.find_all('td')[4].text.strip()
    Decision_Due_date = Details_table.find_all('td')[5].text.strip()
    Validated_date = Details_table.find_all('td')[6].text.strip()
    Invalidated_date = Details_table.find_all('td')[7].text.strip()
    FI_requested_date = Details_table.find_all('td')[8].text.strip()
    FI_Received_date = Details_table.find_all('td')[9].text.strip()
    Withdrawn_date = Details_table.find_all('td')[10].text.strip()
    Extend_date = Details_table.find_all('td')[11].text.strip()
    Decision_type = Details_table.find_all('td')[12].text.strip()
    Decision_date = Details_table.find_all('td')[13].text.strip()
    Leave_to_appeal = Details_table.find_all('td')[14].text.strip()
    Appeal_date = Details_table.find_all('td')[15].text.strip()
    Commenced_date = Details_table.find_all('td')[16].text.strip()
    Submissions_by = Details_table.find_all('td')[17].text.strip()
    
    # Get info from applicant table
    Applicant_table = parser.find_all('div',id = 'Applicant')[0]
    
    Applicant_Name = Applicant_table.find_all('td')[0].text.strip()
    Applicant_Address = Applicant_table.find_all('td')[1].text.strip()
    Phone_no = Applicant_table.find_all('td')[2].text.strip()
    Fax_no = Applicant_table.find_all('td')[3].text.strip()
    Corresp_address = Applicant_table.find_all('td')[4].text.strip()
    
    
    # Get info from development table
    Development_table = parser.find_all('div',id = 'Development')[0]
    
    Description = Development_table.find_all('td')[0].text.strip()
    Dev_address = Development_table.find_all('td')[1].text.strip()
    Loc_key = Development_table.find_all('td')[3].text.strip()
    Dev_Name = Development_table.find_all('td')[12].text.strip()
    
    # Get info from comments table
    Comments_table = parser.find_all('div',id = 'Comments')[0]
    Sig_case  = Comments_table.find_all('td')[0].text.strip()
    Comments  = Comments_table.find_all('td')[1].text.strip()
    
    # Get info from Decision table
    Decision_table = parser.find_all('div',id = 'Decision')[0]
    
    No_conds = Decision_table.find_all('td')[3].text.strip()
    Grant_date  = Decision_table.find_all('td')[4].text.strip()
    Exp_date = Decision_table.find_all('td')[8].text.strip()
    
    #Get info from appeal table
    Appeal_table = parser.find_all('div',id = 'Appeal')[0]
    
    Notification_date = Appeal_table.find_all('td')[0].text.strip()
    Appeal_type = Appeal_table.find_all('td')[2].text.strip()
    App_sub_due = Appeal_table.find_all('td')[4].text.strip()
    App_sub_date = Appeal_table.find_all('td')[5].text.strip()
    App_decision = Appeal_table.find_all('td')[6].text.strip()
    App_dec_date = Appeal_table.find_all('td')[7].text.strip()
    App_withdrawn_date = Appeal_table.find_all('td')[8].text.strip()
    App_dismissed_date = Appeal_table.find_all('td')[9].text.strip()
    App_reason = Appeal_table.find_all('td')[10].text.strip()
    
    row  = pd.DataFrame({'Application Number':App_no,
                         'Appeal Notification':Notification_date,
                         'Appeal type':Appeal_type,
                         'Appeal Submission Due date':App_sub_due,
                         'Appeal Submission Sent Date':App_sub_date,
                         'Appeal Decision':App_decision,
                         'Appeal Decision Date':App_dec_date,
                         'Appeal withdrawn':App_withdrawn_date,
                         'Appeal Dismissed':App_dismissed_date,
                         'Appeal Reason':App_reason,
                         
                         
                         
                         'Applicant Name':Applicant_Name,
                         'Applicant Address':Applicant_Address,
                         'Applicant Phone':Phone_no,
                         'Applicant Fax':Fax_no,
                         'Correspondance Address':Corresp_address,
                         'Description':Description,
                         'Development Address':Dev_address,
                         'Location Key':Loc_key,
                         'Development Name': Dev_Name,
                         'Significant Case':Sig_case,
                         'Comments':Comments,
                         'Number of Conditions':No_conds,
                         'Grant Date':Grant_date,
                         'Expiry Date':Exp_date,
    
                         'Application Type':Application_type ,
                         'Planning Status':Planning_status,
                         'Received Date':Received_date,
                         'Decision Due':Decision_Due_date,
                         'Validated':Validated_date,
                         'Invalidated':Invalidated_date,
                         'FI Requested Date':FI_requested_date,
                         'FI REceived Date':FI_Received_date,
                         'Withdrawn Date':Withdrawn_date,
                         'Extend Date':Extend_date,
                         'Decision Type':Decision_type,
                         'Decision Date':Decision_date,
                         'Leave to Appeal':Leave_to_appeal,
                         'Appeal Date':Appeal_date,
                         'Commenced Date':Commenced_date,
                         'Submissions by':Submissions_by,
                         'url':url
                        
                         },index = [0]
    
    )
    return row





def get_long_lat(df):
    """ Get coordinates for locations vector in Dublin.
    Args:
        API_Key: API Key available from google
        locations: vector of locations 
        
    returns:
        latitude: vector of latitude coordinates
        longitude: vector of longitude coordinates
    """
    
    locations = df['Development Address'].tolist()

    # Set up arrays to populate
    lat = np.zeros(np.shape(locations)[0])
    lng = np.zeros(np.shape(locations)[0])
    ite = 0
    url_google = 'https://maps.googleapis.com/maps/api/geocode/json'
  
    
    
    # get coordinate for each location and add to vectors
    for i in locations:
        complete = False
        address = i
        shortened = False
        while not complete:
            
            parameters_google = {'address':address,'key':'AIzaSyDfjTJ9_zaRMvxu2xJu9UpHwLYg4YK8d0Y'}
            response_google = requests.get(url_google,params=parameters_google)
            
            
            long_lat = response_google.json()
            
            incomplete = 0
                
            try:
                results = long_lat['results'][0]
                
                lat[ite] = results['geometry']['location']['lat']
                lng[ite] = results['geometry']['location']['lng']
                print('{0} \n {1} , {2}\n\n'.format(address,lng[ite], lat[ite]))
                complete=True
            except Exception as e:
                lat[ite] = None
                lng[ite] = None 
                complete = True
                incomplete +=1
                print('{0} not found, please check'.format(address))
                


            
        ite = ite+1
       
    print('\n\nComplete\n\n')  
    df['Latitude'] = lat
    df['Longitude'] = lng
    
    return df


def save_as_kml(df,path = "C:\\Users\\jackh\\OneDrive\\Documents\\Projects\\Python scraping\\Outputs\\kml_output.kml"):
    
    kml = simplekml.Kml()
    df.apply(lambda X: kml.newpoint(name=X['Applicant Name'], description = X['Description'],coords=[( X["Longitude"],X["Latitude"])]) ,axis=1)
    kml.save(path)