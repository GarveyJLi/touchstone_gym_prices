import bs4
import re
import os
import requests
import pandas as pd




def gym_member_table(gym='pacific-pipe', duration=12):
    """
    Takes in name of touchstone gym and df of prices.
    """
    url = os.path.join('https://touchstoneclimbing.com/' + gym + '/members/')
    gym_html = requests.get(url, headers={'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/113.0.0.0 Safari/537.36'}).text.encode("utf-8")
    soup = bs4.BeautifulSoup(gym_html, 'lxml')
    table = soup.find('tbody')

    ind_mem = {}

    for membership in table.find_all('tr'):
        table_contents = membership.find_all('td')
        mem_type = table_contents[0].text
        mem_trate = table_contents[-1].text
        
        regex_prices ='\$((\d|(\,|\.))+)'
        prog = re.compile(regex_prices)
        mem_rates = prog.findall(mem_trate)

        if (len(mem_rates) > 2) or (len(mem_rates) <= 0):
            continue
        elif len(mem_rates) == 1:
            mem_irate = 0.0
            mem_rate = float(mem_rates[0][0].replace(',', ''))
        else: 
            mem_irate = float(mem_rates[0][0].replace(',', ''))
            mem_rate = float(mem_rates[1][0].replace(',', ''))

            if mem_irate == 0:
                mem_rate /= duration
        
        ind_mem[mem_type] = [mem_irate, mem_rate]
    
    return pd.DataFrame.from_dict(ind_mem, orient='index').rename(columns={0: 'Initial Fee', 1: 'Monthly Rate'})




