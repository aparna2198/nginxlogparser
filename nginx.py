# -*- coding: utf-8 -*-
"""
Created on Wed Aug 11 10:21:57 2021

@author: APARNA
"""

import csv
import re
import json
import pandas as pd

class Clean_csv:
    def __init__(self):
        self.headers = ['Date','Time','Id','Response Time(ms)','Route','Method','Status Code','Response Size']
        self.content = []
        self.dictparams = []
        self.filename = "authorlyextracteddata.csv"
        print("initiated")
        
    def set_regular_expressions(self):
        
        self.response_time_p = '\d+\.\d+ ms'
        self.dictparams_p  = '\{.*?\} '
        self.date_p = '\d+-\d+-\d+'
        self.time_p = ' \d+:\d+:\d+'
        self.id_p = ' \"\d+\"'
        self.method_p = 'GET|POST'
        self.route_p = " \/.*? "
        self.status_codes_p = '"Status code :"\d+ '
        self.response_size_p = '"Response Size :"\d+ '
        
    def write_to_csv(self):
        with open (self.filename,'w',newline = "") as efile:
            writer = csv.writer(efile)
            writer.writerow(self.headers)
            for c in self.content:
                writer.writerow(c)
    
    
    def dynamic_headers(self):
        file = pd.read_csv(self.filename)
        index = 0
        for i in range(len(self.dictparams)):
            d = self.dictparams[i]
            for j in d.keys():
                file.loc[index,j] = str(d[j])  
            index+=1
        file.to_csv(self.filename,index = False)
    
    
    def extract_data(self):
        with open('nginx_log.txt') as logfile:
            logs = logfile.readlines()
            self.set_regular_expressions()
            for log in logs:
                date = re.findall(self.date_p,log)[0] if re.findall(self.date_p,log)!=[] else ''
                time = re.findall(self.time_p,log)[0] if re.findall(self.time_p,log)!=[] else ''
                id_ = re.findall(self.id_p,log)[0] if re.findall(self.id_p,log)!=[] else ''
                response_time = re.findall(self.response_time_p,log)[0] if re.findall(self.response_time_p,log)!=[] else ''
                method  = re.findall(self.method_p, log)[0] if re.findall(self.method_p,log)!=[] else ''
                route = re.findall(self.route_p,log)[0] if re.findall(self.route_p,log)!=[] else ''
                status_code = int(re.findall(self.status_codes_p,log)[0].split('"Status code :"')[1]) if re.findall(self.status_codes_p,log)!=[] else ''
                response_size = int(re.findall(self.response_size_p,log)[0].split('"Response Size :"')[1]) if re.findall(self.response_size_p,log)!=[] else ''
                l1 = [date,time,id_,response_time,route,method,status_code,response_size]
                self.content.append(tuple(l1))
                self.dictparams.append(json.loads(re.findall(self.dictparams_p,log)[0] if re.findall(self.dictparams_p,log)!=[] else '{}'))
            self.write_to_csv()
        self.dynamic_headers()
        
            
            
def main():
    obj = Clean_csv()
    obj.extract_data()
    
if __name__ == '__main__':
    main()
        

    
        
        
        
        
    
    
    
    
    
    
    
    
    