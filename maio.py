import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt

import time 
import random
import requests

import signaturehelper

# Korean font for matplotlib graph 
from matplotlib import font_manager, rc
font_name = font_manager.FontProperties(fname="c:/Windows/Fonts/malgun.ttf").get_name()
rc('font', family=font_name)
# Get keys from keys.txt file
keydict = {}
with open('./keys.txt','r') as f:
    lines = f.readlines()
    for line in lines:
        keyname = line.split('=')[0]
        key = line.split('=',maxsplit=1)[1].strip()
        keydict[keyname] = key
    

API_KEY = keydict['API_KEY']
SECRET_KEY = keydict['SECRET_KEY']
CUSTOMER_ID = int(keydict['CUSTOMER_ID'])


def get_header(method, uri, api_key, secret_key, customer_id):
    timestamp = str(round(time.time() * 1000))
    signature = signaturehelper.Signature.generate(timestamp, method, uri, SECRET_KEY)
    return {
            'Content-Type': 'application/json; charset=UTF-8',
            'X-Timestamp': timestamp,
            'X-API-KEY': API_KEY,
            'X-Customer': str(CUSTOMER_ID), 
            'X-Signature': signature
           }
import os
def keywords_graph(kwd):

    if not os.path.exists('./data'):
        os.mkdir('data')
    ## naver ads keywords

    BASE_URL = 'https://api.naver.com'

    uri = '/keywordstool'
    method = 'GET'
    payload={
            'hintKeywords':kwd,
            'showDetail' :1
            }

    r = requests.get(BASE_URL + uri, params=payload, headers=get_header(method, uri, API_KEY, SECRET_KEY, CUSTOMER_ID))
    keywords = r.json()['keywordList'][:100]
    del r


    # preprocessing
    keywords = pd.DataFrame(keywords)
    keywords.columns = ['relkeyword','sch','mob_sch','click','mob_click','clk_r','mob_clk_r','num_ads','comp']

    comp_dic={'높음':2,'중간':1,'낮음':0}

    keywords.comp = keywords.comp.apply(lambda x : comp_dic[x])
    keywords.sch = keywords.sch.astype('str').str.replace('< ','').astype('int')
    keywords.mob_sch = keywords.mob_sch.astype('str').str.replace('< ','').astype('int')

    # preprocessing before entering DataLab API
    keywords10 = keywords[:10]

    from datetime import datetime
    from dateutil.relativedelta import relativedelta as delta
    end = datetime.now().strftime('%Y-%m-%d')
    start   = (datetime.now() - delta(years=1) ).strftime('%Y-%m-%d')

    kwds=keywords10.relkeyword.to_list()
    kwd01 = []
    kwd01.append(kwds[:5])
    kwd01.append(kwds[5:])

    ## naver data lab

    for i in range(2):
        client_id = keydict['nav_client_id']
        client_secret = keydict['nav_client_secret']
        url = "https://openapi.naver.com/v1/datalab/search"
        body = {
            'startDate': start,
            'endDate':  end,
            'timeUnit': 'month',
            'keywordGroups' :[]
        #     'keywordGroups': [{'groupName': '한글', 'keywords': ['한글', 'korean']},
        #                       {'groupName': '영어', 'keywords': ['영어', 'english']}],
        #     'device': 'pc',
        #     'ages': ['1', '2'],
        #     'gender': 'f'
        }
        for kw in kwd01[i]:
            group = { 'groupName': kw , 'keywords': [kw] }
            body['keywordGroups'].append(group)

        header = {}
        header["X-Naver-Client-Id"] = client_id
        header["X-Naver-Client-Secret"] = client_secret
        header["Content-Type"]="application/json"
        rq = requests.post(url ,json=body ,headers=header )

        results = rq.json()['results']

        fig, axs = plt.subplots(1, 1, constrained_layout=True, sharey=True,figsize=(15,8))
        for item in results:
            df = pd.DataFrame(item['data'])
            axs.plot(df.period,df.ratio,'--o',label=item['title'])

        axs.grid(True)  
        plt.xticks(rotation=45)
        plt.legend(loc='best')
        plt.xlabel('month')
        plt.ylabel('Trend')
        fig.savefig('data/graph_%s%d.png'%(kwd,i))

from datetime import datetime
from dateutil.relativedelta import relativedelta as delta

class keywordTrend :

    def __init__(self,kwd):
        self.kwd = kwd
        self.tkwds = self.preprcs_kwds(self.ads_kwds(kwd )  )
        self.kwds_coordis = None
        # self.keycoords

    ## naver ads keywords
    def ads_kwds(self,kwd):
        BASE_URL = 'https://api.naver.com'

        uri = '/keywordstool'
        method = 'GET'
        payload={
                'hintKeywords':kwd,
                'showDetail' :1
                }

        r = requests.get(BASE_URL + uri, params=payload, headers=get_header(method, uri, API_KEY, SECRET_KEY, CUSTOMER_ID))
        keywords = r.json()['keywordList'][:100]
        del r
        return keywords

    ## preprocessing of naver ads keywords
    def preprcs_kwds(self,keywords):
        keywords = pd.DataFrame(keywords)
        keywords.columns = ['relkeyword','sch','mob_sch','click','mob_click','clk_r','mob_clk_r','num_ads','comp']

        comp_dic={'높음':2,'중간':1,'낮음':0}

        keywords.comp = keywords.comp.apply(lambda x : comp_dic[x])
        keywords.sch = keywords.sch.astype('str').str.replace('< ','').astype('int')
        keywords.mob_sch = keywords.mob_sch.astype('str').str.replace('< ','').astype('int')

        return keywords

    def get_keywords(self,num=10):
        return self.tkwds[:num]
        

    def kwds_coordinates(self,num=10):
        
        keywords10 = self.get_keywords(num=num)

        end = datetime.now().strftime('%Y-%m-%d')
        start   = (datetime.now() - delta(years=1) ).strftime('%Y-%m-%d')
        
        kwds=keywords10.relkeyword.to_list()
        kwd01 = []

        for x in range(0 ,len(kwds) ,5 ):
            kwd01.append(kwds[x:x+5] )

        ## naver data lab
        results = []
        for i in range(len(kwd01)):
            client_id = keydict['nav_client_id']
            client_secret = keydict['nav_client_secret']
            url = "https://openapi.naver.com/v1/datalab/search"
            body = {
                'startDate': start,
                'endDate':  end,
                'timeUnit': 'month',
                'keywordGroups' :[]
            #     'keywordGroups': [{'groupName': '한글', 'keywords': ['한글', 'korean']},
            #                       {'groupName': '영어', 'keywords': ['영어', 'english']}],
            #     'device': 'pc',
            #     'ages': ['1', '2'],
            #     'gender': 'f'
            }
            for kw in kwd01[i]:
                group = { 'groupName': kw , 'keywords': [kw] }
                body['keywordGroups'].append(group)

            header = {}
            header["X-Naver-Client-Id"] = client_id
            header["X-Naver-Client-Secret"] = client_secret
            header["Content-Type"]="application/json"
            rq = requests.post(url ,json=body ,headers=header )

            results.extend(rq.json()['results'] )

        self.kwds_coordis = results 
        return results 

    def show(self):
        if self.kwds_coordis == None :
            kwds = self.kwds_coordinates()
        else :
            kwds = self.kwds_coordis

        for x in range(0,len(kwds),5):
            results = kwds[x:x+5]

            fig, axs = plt.subplots(1, 1, constrained_layout=True, sharey=True,figsize=(15,8))
            for item in results:
                df = pd.DataFrame(item['data'])
                axs.plot(df.period,df.ratio,'--o',label=item['title'])
            
            axs.grid(True)  
            plt.xticks(rotation=45)
            plt.legend(loc='best')
            plt.xlabel('month')
            plt.ylabel('Trend')
            plt.show()

import sys
if __name__ == '__main__' :

    test_kw = '홍삼'
    if len(sys.argv)>1:
        keywords_graph(sys.argv[1])
    else :
        keywords_graph(test_kw)
