# -*- coding: utf-8 -*-

import pandas as pd
from bs4 import BeautifulSoup
import urllib.request

""" Thonky Web Scrape """

def scrape_thonky(url):
    html_doc = urllib.request.urlopen(url)
    soup = BeautifulSoup(html_doc, 'html.parser')
    list_table = soup.findAll("table", {"class": 'table table-bordered'})
    table_container = []
    
    # scrape all tables in the given webpage
    for table in list_table:
        temp_table = []
        temp_headers = []
        count = 0
        table_rows = table.findAll('tr')
        
        for table_row in table_rows:
            if count == 0:
                headers = table_row.findAll('th')
                
                for names in headers:
                    temp_headers.append(names.text)
                    
                count = count + 1

            columns = table_row.findAll('td')
            output_row = []
            
            for column in columns:
                output_row.append(column.text)
            
            len_row = len(output_row)
            len_head = len(temp_headers)
            
            if len_row == len_head:
                temp_table.append(output_row)
            elif temp_headers == []:
                temp_table.append(output_row)
        
        # use DataFrame, or can leave it as a list of lists
        if temp_headers != []:
            temp_table = pd.DataFrame(temp_table, columns = temp_headers)
        else:
            temp_table = pd.DataFrame(temp_table)
        table_container.append(temp_table)
        
    # return a list of dataframes for all tables from the page
    return table_container

# Examples
furniture = 'https://www.thonky.com/animal-crossing-new-leaf/list-of-furniture'
feng_shui = 'https://www.thonky.com/animal-crossing-new-leaf/feng-shui-guide'
theme = 'https://www.thonky.com/animal-crossing-new-leaf/furniture-by-theme'
customizable = 'https://www.thonky.com/animal-crossing-new-leaf/list-of-custom-furniture'
clothes = 'https://www.thonky.com/animal-crossing-new-leaf/gracie-fashion-check'
wallpaper_carpets = 'https://www.thonky.com/animal-crossing-new-leaf/list-of-wallpapers-carpets'    
    
furniture_table = scrape_thonky(furniture)
feng_shui_table = scrape_thonky(feng_shui)
theme_table = scrape_thonky(theme)
customizable_table = scrape_thonky(customizable)
wall_floor = scrape_thonky(wallpaper_carpets)

