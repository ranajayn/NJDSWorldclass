##Web crawling for all the 10 pages
import requests
from bs4 import BeautifulSoup
import pandas

a=[]
base_url="https://www.lamps.com/outdoor-lights/outdoor-ceiling-lights?p="
for page in range(10):
    print(base_url+str(page))
    r=requests.get(base_url+str(page))
    c=r.content
    soup=BeautifulSoup(c,"html.parser")
    all=soup.find_all("li",{"class":"item"})
    for items in all:
            d={}
            try:
                d["Product_Description"]=items.find("h2",{"class":"product-name product-name-simple"}).text
            except:
                d["Product_Description"]="NO DESCRIPTION FOUND"

            d["Product_Price"]=items.find("span",{"class":"price"}).text
            try:
                d["Product_Image"]=items.find("img",{"class":"product-image"}).get('src')
            except:
                d["Product_Image"] = "NO IMAGE FOUND"
            a.append(d)
    df=pandas.DataFrame(a)
    df.to_csv("Final_Output.csv")