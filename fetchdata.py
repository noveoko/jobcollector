# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from bs4 import BeautifulSoup as bs
import json, codecs, requests

url = "https://justjoin.it/feed.atom"

def fetchData(url=url): #specify xml or html
    response = requests.get(url, timeout=100)
    head = response.headers
    ftype=""
    if response.status_code == 200:
        if 'application/xml' in head['Content-Type']: #xml file  
            ftype = 'xml'
        elif 'text/html' in head['Content-Type']: #html file
            ftype = 'html'
    filename = f'jobs.{ftype}'
    with open(filename, 'w') as outfile:
        outfile.write(str(response.content))
    return (filename, ftype)

def fileToJson():
    filename, ftype = fetchData() #fetches fresh XML file, returns filename
    data = {}
    raw_html = codecs.open(filename,'r','utf-8')
    if ftype == 'html': #parse HTML file
        soup = bs(raw_html, 'xml')
        jobs = [a for a in soup.find_all("div", {"class":"entry"})]
        for count, job in enumerate(jobs):
            amount = job.find("b", text="Salary:").next_sibling.strip()
            address = job.find("b", text="Location:").next_sibling.strip().split(",")
            try:
                street, city = (address[0:-1],address[-1])
            except ValueError as ve:
                print(ve, address)
            title_company = " ".join([a.text for a in job.find_all("span")if a.has_attr('xml:base')])
            if title_company:
                job_title, company_name = [a.strip() for a in title_company.split("@")]
                if company_name in jobs:
                    data[company_name].append({'title':job_title,'salary':amount,'address':street,'city':city,'company_name':company_name})
                else:
                    data[company_name] = [{'title':job_title,'salary':amount,'address':street,'city':city,'company_name':company_name}]
            else:
                print(f'error with company: {count}')
    elif ftype == 'xml': #parse xml
        print('this function not yet built')
    else:
        print('error')

    with codecs.open('jobs.json', 'w', 'utf-8') as fp:
        json.dump(data, fp)
    return data
        

fileToJson()




