#NewsFeed that houses search results
import requests
from bs4 import BeautifulSoup
from fake_useragent import UserAgent
import re
import urllib.parse
from urllib.parse import urlparse
from VIAA_Database import *
from homepagescript import *
from tld import get_tld
import sqlite3
from sqlite3 import Error

#Search keywords
def googleSearch(query):
    g_clean = [] #this is the list we store the search results
    header_clean = []
    url = 'https://www.google.com/search?client=ubuntu&channel=fs&q={}&ie=utf-8&oe=utf-8&as_qdr=w'.format(query) #this is the actual query we are going to scrape    
    try:
        html = requests.get(url)
        if html.status_code==200:
            soup = BeautifulSoup(html.text, 'lxml')
            a = soup.find_all('a') # a is a list
            h3 = soup.find_all('h3') # h3 is also a list
            header_i = 0
        for i2 in range(len(a)):
            i = a[i2];
            header = h3[header_i]
            k = i.get('href')
            if len(i.findChildren()) >= 2:
                j = i.findChildren()[1]
            try:
                m = re.search("(?P<url>https?://[^\s]+)", k)
                n = m.group(0)
                rul = n.split('&')[0]
                domain = urlparse(rul)
                if(re.search('google.com', domain.netloc)):
                    continue
                else:
                    childTag = i.find('h3')
                    if childTag:
                        g_clean.append(rul)
                        header_clean.append(header.contents[0].string)
                        header_i += 1
                        print(rul)
                        print(header.contents[0].string)

            except:
                continue
    #prints the errors            
    except Exception as ex:
        print(str(ex))
    finally:
        return g_clean, header_clean

def googleScholarSearch(query):
    g_clean = [] #this is the list we store the search results
    header_clean = []
    url = 'https://scholar.google.com/scholar?hl=en&q={}&ie=utf-8&oe=utf-8&as_qdr=w'.format(query) #this is the actual query we are going to scrape    
    try:
        html = requests.get(url)
        if html.status_code==200:
            soup = BeautifulSoup(html.text, 'lxml')
            a = soup.find_all('a') # a is a list
            h3 = soup.find_all('h3') # h3 is also a list
            header_i = 0
        else:
            print(html.status_code)    
        for i2 in range(len(a)):
            i = a[i2];
            header = h3[header_i]
            k = i.get('href')
            if len(i.findChildren()) >= 2:
                j = i.findChildren()[1]
            try:
                m = re.search("(?P<url>https?://[^\s]+)", k)
                n = m.group(0)
                rul = n.split('&')[0]
                domain = urlparse(rul)
                if(re.search('scholar.google.com', domain.netloc)):
                    continue
                else:
                    parentTag = i.parent.name
                    if parentTag == 'h3':
                        g_clean.append(rul)
                        temp_header = ''
                        for content in i.contents:
                            temp_header += content.string
                        header_clean.append(temp_header)
                        #header_clean.append(i.contents[0].string)
                        header_i += 1
                        print(rul)
                        #print(i.contents[0].string)
                        print(temp_header)

            except:
                continue
    #prints the errors            
    except Exception as ex:
        print(str(ex))
    finally:
        return g_clean, header_clean

'''

def JamiaSearch(query):
    g_clean = [] #this is the list we store the search results
    header_clean = []
    url = 'https://academic.oup.com/jamia/search-results?q={}&sort=Date+%e2%80%93+Newest+First&fl_SiteID=5396&page=1&qb={{%22q%22:%22{}%22}}'.format(query, query) #this is the actual query we are going to scrape 
   #https://academic.oup.com/jamia/search-results?q=puppies&sort=Date+%e2%80%93+Newest+First&fl_SiteID=5396&page=1&qb={%22q%22:%22puppies%22}
   
    print(url)

    try:
        headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36'}

        html = requests.get(url, headers)
        if html.status_code==200:
            soup = BeautifulSoup(html.text, 'lxml')
            a = soup.find_all('a') # a is a list
            h3 = soup.find_all('h4') # h4 is also a list
            header_i = 0
        else:
            print(html.status_code)    
        for i2 in range(len(a)):
            i = a[i2];
            header = h4[header_i]
            k = i.get('href')
            if len(i.findChildren()) >= 2:
                j = i.findChildren()[1]
            try:
                m = re.search("(?P<url>https?://[^\s]+)", k)
                n = m.group(0)
                rul = n.split('&')[0]
                domain = urlparse(rul)
                if(re.search('scholar.google.com', domain.netloc)):
                    continue
                else:
                    parentTag = i.parent.name
                    if parentTag == 'h4':
                        g_clean.append(rul)
                        temp_header = ''
                        for content in i.contents:
                            temp_header += content.string
                        header_clean.append(temp_header)
                        #header_clean.append(i.contents[0].string)
                        header_i += 1
                        print(rul)
                        #print(i.contents[0].string)
                        print(temp_header)    
            except:
                continue
    #prints the errors            
    except Exception as ex:
        print(str(ex))
    finally:
        return g_clean, header_clean

query = 'puppies'
j_results, jh_results = JamiaSearch(query)
print(j_results)
print(jh_results)
#JamiaSearch('puppies')
'''

def do_searches(inputnew_word):
    g_results, h_results = googleSearch(inputnew_word)
    gs_results, hs_results = googleScholarSearch(inputnew_word)
    #j_results, js_results = JamiaSearch(inputnew_word)
    
    database = r"dbVIAA.db"
    conn = create_connection(database)

    for result in range(len(g_results)):
        url = g_results[result]
        title = h_results[result]
        #Get Domain name
        info = get_tld(url, as_object=True)
        create_url(conn, title, info.domain, url, inputnew_word )

    for result in range(len(gs_results)):
        url = gs_results[result]
        title = hs_results[result]
        #Get Domain name
        info = get_tld(url, as_object=True)
        create_url(conn, title, info.domain, url, inputnew_word )

database = r"dbVIAA.db"
conn = create_connection(database)


#Insert into database
def create_url(conn,title,website_name,url,inputnew_word):
    
    #Create a new url into the url table
    #:param conn:
    #:param url:
    #:return: url id
    
    sql =  '''INSERT INTO url(title,website_name,url,keyword)
              VALUES(?,?,?,?) '''

    cur = conn.cursor()
    cur.execute(sql, (title,website_name.title(),url,inputnew_word ))
    conn.commit()
    return cur.lastrowid
'''
for result in range(len(g_results)):
    url = g_results[result]
    title = h_results[result]
    #Get Domain name
    info = get_tld(url, as_object=True)
    create_url(conn, title, info.domain, url, inputnew_word )

for result in range(len(gs_results)):
    url = gs_results[result]
    title = hs_results[result]
    #Get Domain name
    info = get_tld(url, as_object=True)
    create_url(conn, title, info.domain, url, inputnew_word )

for result in range(len(j_results)):
    url = j_results[result]
    title = jh_results[result]
    #Get Domain name
    info = get_tld(url, as_object=True)
    create_url(conn, title, info.domain, url,inputnew_word )    
''' 
# Getting urls per userid to populate table
def url_table(userID): 
    conn = create_connection(r"dbVIAA.db")
    cur = conn.cursor()
    cur.execute("SELECT url.title,website_name,url,url.keyword FROM url INNER JOIN keyword ON url.keyword = keyword.keyword where user_id = '" + userID + "';")

    results = cur.fetchall()
    
    return results
  