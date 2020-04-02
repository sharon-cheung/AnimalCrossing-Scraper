# -*- coding: utf-8 -*-

import pandas as pd
from bs4 import BeautifulSoup
import urllib.request
import time


""" MoriDB Web Scrape """

source = 'http://moridb.com/'

def scrape_moridb(url):
    temp_output = []
    
    # loop through search results
    while(1):
        html_doc = urllib.request.urlopen(url)
        soup = BeautifulSoup(html_doc, 'html.parser')
        list_table = soup.findAll("div", {"class": 'item-info span9'})
        num_items = 0
        results = []
        
        # list of items
        for item in list_table:
            data = []
            item_name = item.findAll("a", {"class": "item-name"})[0].contents[0]
            data.append(item_name)
            names = item.findAll("dt")
            info = item.findAll("dd")
            num_fields = len(names)
            num_items = num_items + 1
            columns = ["Name"]
            
            for i in range(num_fields):
                columns.append(names[i].text.strip())
                data.append(info[i].text.strip())
            
            data = pd.DataFrame(data).T
            data.columns=columns
            results.append(data)
        
        len_results = len(results)
        
        # compile list of items
        for i in range(0,len_results):
            if i == 0:
                output = results[0]
            else:
                output = pd.concat([output,results[i]],join='outer',
                                   sort=False)
            
        temp_output.append(output)
        
        # check if next page exists
        next_list = soup.findAll("li", {"class": "next"})
        len_next = len(next_list)
        
        if len_next==2:
            next_list = next_list[1]
            link = next_list.find("a")
            
            if link != None:
                suffix = link.get('href')
                url = source + suffix
            else:
                break
        
        # sleep timer
        time.sleep(5)
    
    # consolidate the final output across page results
    len_output = len(temp_output)
    
    for i in range(0,len_output):
        if i == 0:
            consolidated = temp_output[0]
        else:
            consolidated = pd.concat([consolidated, temp_output[i]], 
                                     join = 'outer',
                                     sort = False)
            
    consolidated.to_csv("moridb_output.csv", index=False)
    return consolidated

# Example
tops_db ='http://moridb.com/items/tops/?limit=50&offset=0'
tops = scrape_moridb(tops_db)

shoes = 'http://moridb.com/items/shoes/'
shoes = scrape_moridb(shoes)
