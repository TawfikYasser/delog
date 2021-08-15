"""
Python Scraper
"""
import requests
from bs4 import BeautifulSoup
import csv
from itertools import zip_longest

page_number = 0
jts = []
cs = []
ls = []
sls = []
reqs = []
requirements = []
pos = []

csv_file_path = "T:\Code\Python\wuzzuf-python-scraper.csv"

while True:

    try:
        result = requests.get(f"https://wuzzuf.net/search/jobs/?a=hpb&q=python&start={page_number}") # Page itself

        src = result.content # Page content

        soup = BeautifulSoup(src,"lxml") # BS Object - lxml Parser to do operations

        # Find elements we need (job title ...)

        #Page limit
        p_limit = int(soup.find("strong").text)
        if page_number > p_limit // 15:
            print("Data Collected")
            break
        
        job_title = soup.find_all("h2",{"class":"css-m604qf"}) # find_all : return list

        company = soup.find_all("a",{"class":"css-17s97q8"})

        locations = soup.find_all("span",{"class":"css-5wys0k"})

        skills = soup.find_all("div",{"class":"css-y4udm8"})

        date_new = soup.find_all("div",{"class":"css-4c4ojb"})
        date_old = soup.find_all("div",{"class":"css-do6t5g"})

        posted = [*date_new , *date_old]

        # loop tp extract needed data from lists

        jobs_length =len(job_title)
        job_links = []
        for i in range(jobs_length):
            jts.append(job_title[i].text)
            job_links.append(job_title[i].find("a").attrs['href'])
            cs.append(company[i].text)
            ls.append(locations[i].text)
            sls.append(skills[i].text)
            pos.append(posted[i].text)

        page_number +=1
        print(f"Page #{page_number} Switched")
    except:
        print("ERROR IN THE WEBPAGE")
print(len(job_links))
try:
    for link in job_links:
        print(link)
        l_result = requests.get(link)
        l_src = l_result.content
        l_soup = BeautifulSoup(l_src,"lxml")
        reqs = l_soup.find("div",{"class":"css-1t5f0fr"}).ul
        reqs_text = ""
        for li in reqs.find_all("li"):
            reqs_text += li.text + " | "
        reqs_text = reqs_text[:-2]
        requirements.append(reqs_text)
except:
    print("ERROR IN PAGES")


# CSV
try:
    file_list = [jts,cs,ls,pos,requirements]
    exported_data = zip_longest(*file_list) # Unpacking : Combination between all
    with open(csv_file_path,"w") as jfile:
        wr = csv.writer(jfile)
        wr.writerow(["Job Title","Company Name","Company Location","Date Posted","Requirements"])
        wr.writerows(exported_data)
    print("Done")
except:
    print("ERROR IN FILES")
