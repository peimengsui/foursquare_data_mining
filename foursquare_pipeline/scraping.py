_author_ = "Peimeng Sui"
'''
sample usage python scraping.py "shopping"
'''
import selenium
import time,re,json,numpy as np
import pandas as pd
from collections import defaultdict, Counter
import matplotlib.pyplot as plt
from selenium import webdriver
from bs4 import BeautifulSoup
import urllib
import pdb
import foursquare
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import sys
import csv

client = foursquare.Foursquare(client_id='AIJCQYDOQ1E5LLFG0ZWZWXZXASLJDIJQ1P33CX04YWEA5EDO', 
                               client_secret='SFT2TK2ZNUXGY3HYZGNV1HY1OH0KF2QQD5MRELNQC5BFB4TB', 
                               redirect_uri='http://fondu.com/oauth/authorize')
auth_uri = client.oauth.auth_url()
client = foursquare.Foursquare(client_id='AIJCQYDOQ1E5LLFG0ZWZWXZXASLJDIJQ1P33CX04YWEA5EDO', 
                               client_secret='SFT2TK2ZNUXGY3HYZGNV1HY1OH0KF2QQD5MRELNQC5BFB4TB')


def search(query = 'Restaurant',location='New York'):
    #this function do the search on foursquare automatically returning a final url
    browser = webdriver.Firefox()
    browser.maximize_window()
    url="http://foursquare.com"
    browser.get(url)
    browser.find_element_by_id('headerBarSearch').clear()
    browser.find_element_by_id('headerBarSearch').send_keys(query)
    browser.find_element_by_id('headerLocationInput').clear()
    browser.find_element_by_id('headerLocationInput').send_keys(location)
    browser.find_element_by_xpath("/html/body/div[1]/div[2]/div[1]/div[1]/div[3]/div/div/form/button").click()
    Wait = WebDriverWait(browser, 10)       
    Wait.until(EC.presence_of_element_located((By.XPATH, "/html/body/div[1]/div[2]/div/div[3]/div[1]/div[1]/div/div[1]/img")))
    page = browser.page_source
    return page


def get_tips(page,query,location):
    soup = BeautifulSoup(page)
    names = []
    ids = []
    #venues = []
    for ana in soup.findAll('a'):
        if ana.parent.name == 'h2':
            #venues.append(ana["href"])
            names.append(ana["href"].split('/')[2])
            ids.append(ana["href"].split('/')[3][0:24])
    #pdb.set_trace()
    #ids = [x[-24:] for x in venues]
    tips = query_tips(ids)
    tips["zone"] = location
    tips["category"] = query
    tips["venue"] = names
    return tips


def query_tips(ids,limit=500):     
    tips_text=[]
    for i in ids:
        text=[]
        items = client.venues.tips(i,params={'limit': limit})["tips"]["items"]
        for k in items:
                k["text"]= re.sub(r'^https?:\/\/.*[\r\n]*', '', k["text"], flags=re.MULTILINE)
                text.append(k["text"].lower())
        tips_text.append(text)

    d = {'tips_text' : pd.Series(tips_text, index=ids)}
    df = pd.DataFrame(d)
    return df

def get_stats(ids,query):
    #get number of checkins
    checkins=[]
    for i in ids:
        checkins.append(client.venues(i)["venue"]["stats"]["checkinsCount"])
    
    #get number of users
    users=[]
    for i in ids:
        users.append(client.venues(i)["venue"]["stats"]["usersCount"])
    
    #get number of tips
    tips=[]
    for i in ids:
        tips.append(client.venues(i)["venue"]["stats"]["tipCount"])
        
    #get number of visits
    visits=[]
    for i in ids:
        visits.append(client.venues(i)["venue"]["stats"]["visitsCount"])
                      
    #get number of likes
    likes=[]
    for i in ids:
        likes.append(client.venues(i)["venue"]["likes"]["count"])
    
    photos=[]
    for i in ids:
        photos.append(client.venues(i)["venue"]["photos"]["count"])
    
    sub_cat=[]
    for i in ids:
        sub=[]
        for cat in client.venues(i)["venue"]["categories"]:
            sub.append(cat["name"])
        sub_cat.append(sub)

    d = {'checkins' : pd.Series(checkins, index=ids),
         'users' : pd.Series(users, index=ids),
         'tips' : pd.Series(tips,index=ids),
         'visits' : pd.Series(visits,index=ids),
         'likes' : pd.Series(likes,index=ids),
         'photos' : pd.Series(photos,index=ids),
         'sub_cat':pd.Series(sub_cat,index=ids)
        }
    df = pd.DataFrame(d)
    df['Category'] = query
    return df

def build_stat_df(page,query,location):
    soup = BeautifulSoup(page)
    names = []
    ids = []
    for ana in soup.findAll('a'):
        if ana.parent.name == 'h2':
            #venues.append(ana["href"])
            names.append(ana["href"].split('/')[2])
            ids.append(ana["href"].split('/')[3][0:24])
    stat = get_stats(ids,query)
    stat["zone"] = location
    stat["venue"] = names
    return stat

l=[]
with open('nytownnames.csv') as csvfile:
    readCSV = csv.reader(csvfile, delimiter=',')
    for row in readCSV:
        l.append(row[0])
names = [x.strip(' ') for x in l]

for query in names:
    page = search(sys.argv[1],query)
    tips = get_tips(page,sys.argv[1],query)
    stat = build_stat_df(page,sys.argv[1],query)

    data3 = tips[["tips_text","category"]]
    data = stat.merge(data3,how="inner",left_index=True,right_index=True)
    data.to_pickle(query+'_'+sys.argv[1]+'.pkl')
