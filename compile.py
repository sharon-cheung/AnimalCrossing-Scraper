# -*- coding: utf-8 -*-
"""
Created on Thu Apr  2 16:13:25 2020

@author: scheu
"""

import pandas as pd
from scrape_moridb import scrape_moridb
from scrape_thonky import scrape_thonky

moridb_file = 'moridb_urls.txt'
thonky_file = 'thonky_urls.txt'
csv_suffix = "output.csv"

files = [moridb_file, thonky_file]

tables = []

for i in files:
    with open(i) as f:
        content = f.readlines()
    # you may also want to remove whitespace characters like `\n` at the end of each line
    tables.append([x.strip() for x in content])

# build file name
len_tables = len(tables)
# MoriDB Url's is first element, Thonky URL's in the second
for i in range(0, len_tables):
    count = 0
    if i == 0:
        for url in tables[i]:
            curr_table = scrape_moridb(url)
            name = "moridb" + "_" + str(count) + "_" + csv_suffix
            curr_table.to_csv(name, index = False)
            count = count + 1
    else:
        for url in tables[i]:
            curr_list = scrape_thonky(url)
            for table in curr_list:
                name = "thonky" + "_" + str(count) + "_" + csv_suffix
                table.to_csv(name, index = False)
                count = count + 1
        


    