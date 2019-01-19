# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from bs4 import BeautifulSoup as bs
import json, codecs

def atomToJson():
    data = {}
    raw_html = codecs.open('jobs.txt','r','utf-8')
    soup = bs(raw_html, 'html.parser')
    jobs = [a for a in soup.find_all("div", {"class":"entry"})]
    for count, job in enumerate(jobs):
        amount = job.find("b", text="Salary:").next_sibling.strip()
        address = job.find("b", text="Location:").next_sibling.strip().split(",")
        try:
            street, city = (address[0:-1],address[-1])
        except ValueError as ve:
            print(ve, address)
        title_company = " ".join([a.text for a in job.find_all("span")if 'https://justjoin.it/feed.atom' in str(a)])
        if title_company:
            job_title, company_name = [a.strip() for a in title_company.split("@")]
            if company_name in jobs:
                data[company_name].append({'title':job_title,'salary':amount,'address':street,'city':city,'company_name':company_name})
            else:
                data[company_name] = [{'title':job_title,'salary':amount,'address':street,'city':city,'company_name':company_name}]
        else:
            print(f'error with company: {count}')
    with codecs.open('jobs.json', 'w', 'utf-8') as fp:
        json.dump(data, fp)
    return data
        

result = atomToJson()



