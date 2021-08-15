"""
A python sraper to get companies data from stackoverflow.com
"""
import requests
from bs4 import BeautifulSoup
import csv
from itertools import zip_longest

from flask import Flask, request
from flask_sqlalchemy import SQLAlchemy


page_number = 1
company_titles = []
company_location = []
company_industry = []
company_description = []
company_website = []
company_size = []
company_founded_date = []
cip = 10 # Number of companies in one page

print("Getting data may take some secs...")
num = 0

while True:
    try:
        result = requests.get(f"https://stackoverflow.com/jobs/companies?pg={page_number}")
        src = result.content
        soup = BeautifulSoup(src,"lxml")

        pstr = soup.find("span",{"class":"description fc-light fs-body1"}).text
        page_limit = int(pstr[:1] + pstr[2:5])

        nop = page_limit // 10 # Total number of pages
        if page_number > nop:
            print("Data Collected Successfully!")
            break

        c_titles = soup.find_all("h2",{"class":"fs-body2 mb4"})
        c_location = soup.find_all("div",{"class":"d-flex gs12 gsx ff-row-wrap fs-body1"})
        # c_industry = soup.find_all("div",{"class":"d-flex gs12 gsx ff-row-wrap fs-body1"})
        c_description = soup.find_all("p",{"class":"mt8 mb0 fs-body1 fc-black-700 v-truncate2"})
        num += len(c_titles)

        # Get needed data
        # links = []
        leng = len(c_titles)
        for i in range(leng):
            company_titles.append(c_titles[i].find("a").text)
            # links.append(c_titles[i].find("a").attrs['href'])
            company_location.append(c_location[i].find("div",{"class":"flex--item fc-black-500 fs-body1"}).text)
            # company_industry.append(c_industry[i].find("div",{"class":"flex--item fc-black-500 fs-body1"}).text)
            if not leng > len(c_description):
                company_description.append(c_description[i].text)

        print(f"Number of companies till now {num}")
        print(f"Page #{page_number} Done.")
        page_number += 1

    except:
        print("Error in page data.")


# To save in DB
app = Flask(__name__)
# DB Configuration
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///companiesdb.db'
db = SQLAlchemy(app)
class CompanyModel(db.Model):
    id = db.Column(db.Integer,primary_key=True)
    name = db.Column(db.String(100),nullable=False)
    location = db.Column(db.String(100),nullable=False)
    # industry = db.Column(db.String(100),nullable=False)
    description = db.Column(db.String(250),nullable=False)
    def __repr__(self) -> str:
        return f"Company Data: {self.id} - {self.name} - {self.location}  - {self.description}"
db.create_all()


for cid in range(len(company_titles)):
    if not (cid+1) > len(company_description):
        co = CompanyModel(id=cid+1,name=company_titles[cid],location=company_location[cid],description=company_description[cid])
    else:
        co = CompanyModel(id=cid+1,name=company_titles[cid],location=company_location[cid],description="Not Provided")        
    db.session.add(co)
    print(f"Company #{cid} added.")
    
db.session.commit()
print("Data Commited.")
print("="*150)
result = CompanyModel.query.filter_by(id=12).first()
print(f"Company Data: {result.id} - {result.name} - {result.location} - {result.description}")


#To save in CSV
# try:
#     file_list = [company_titles,company_location,company_description]
#     exported = zip_longest(*file_list)
#     with open("T:\Code\Python\Python_Project\company-bs-data.csv","w",newline='',encoding="utf-8") as dataFile:
#         wr = csv.writer(dataFile)
#         wr.writerow(["Company Title","Company Location","Company Description"])
#         wr.writerows(exported)
#     print("File Saved.")
# except:
#     print("Error in file")
