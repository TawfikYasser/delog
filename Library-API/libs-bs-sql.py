import itertools
import requests
from bs4 import BeautifulSoup
import csv
from itertools import zip_longest
import json
import os
from flask import Flask, request, jsonify
from flask_restful import Api, Resource, reqparse, abort, fields, marshal_with
from flask_sqlalchemy import SQLAlchemy

print("Getting data started...")

app = Flask(__name__)
api = Api(app)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///libdb.db'
db = SQLAlchemy(app)
class LibraryModel(db.Model):
    id = db.Column(db.Integer,primary_key=True)
    name = db.Column(db.String(150),nullable=False)
    version = db.Column(db.String(100),nullable=False)
    link = db.Column(db.String(100),nullable=False)
    description = db.Column(db.String(250),nullable=False)

db.create_all()

page_number = 1
libs_names = []
libs_links = []
libs_desc = []
libs_version = []
cip = 20 # Number of libs in one page
total_libs = 0

while True:
    
    result = requests.get(f"https://pypi.org/search/?c=Programming+Language+%3A%3A+Python&page={page_number}")
    src = result.content
    soup = BeautifulSoup(src,"lxml")

    # # Checking more data
    # pstr = soup.find("div",{"class":"split-layout split-layout--table split-layout--wrap-on-tablet"}).find("div").find("p").find("strong").text
    # page_limit = int(pstr[:2] + pstr[3:6])

    nop = 10000 // 20 # Total number of pages
    if page_number > nop:
        print("Data Collected Successfully!")
        break

    libs = soup.find_all("span",{"class":"package-snippet__name"})
    links = soup.find_all("a",{"class":"package-snippet"})
    desc = soup.find_all("a",{"class":"package-snippet"})
    version = soup.find_all("span",{"class":"package-snippet__version"})

    for i in range(len(libs)):
        libs_names.append(libs[i].text.strip())
        libs_links.append(links[i].attrs['href'].strip())
        if desc[i].find("p",{"class":"package-snippet__description"}).text.strip():
            libs_desc.append(desc[i].find("p",{"class":"package-snippet__description"}).text.strip())
        else:
            libs_desc.append("Description not provided.")
        libs_version.append(version[i].text.strip())
    
    total_libs += 20
    print(f"Page #{page_number} Done - {total_libs} collected till now.")        
    page_number +=1 
        

# final_data = {name: {'Version': ver, 'link': link} for name, ver, link in zip(libs_names, libs_version, libs_links)}
final_data = [{'Library Name': name, 'Library Version': ver, 'Library Link': link, "Library Description": desc} for name, ver, link, desc in zip(libs_names, libs_version, libs_links, libs_desc)]

for lid in range(len(libs_names)):
    lib = LibraryModel(id=(lid+1),name=libs_names[lid],version=libs_version[lid],link=libs_links[lid],description=libs_desc[lid])
    db.session.add(lib)
    print(f"Library #{lid+1} added.")
    
db.session.commit()
print("Data Commited to DB successfully.")

with open("libs-data-serialize.json","w") as json_file:
    json.dump(final_data,json_file)
    print("Data saved to json file.")

# print("="*150)
# result = LibraryModel.query.order_by(LibraryModel.id).all()
# for i in list(result):    
#     print(f"Library Data: {i.id} - {i.name} - {i.version} - {i.link} - {i.description}")