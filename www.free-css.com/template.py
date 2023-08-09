import time
import uuid
import youtube_dl
import requests
import mysql.connector
from bs4 import BeautifulSoup

url = "https://www.free-css.com"

mydb = mysql.connector.connect(
  host="localhost",
  user="root",
  password="",
  database="gethub"
)
mycursor = mydb.cursor()


id_str = ""
title = ""
alt_img = ""
url_from = ""
icon_img = ""
name = ""
more = ""
link = ""
rating = ""
url_template = ""

t_authorname = ""
t_doctype = ""
t_layout = ""
t_contrast = ""
t_colours = ""

def DownloadImg():
    with requests.Session() as session:
        # Save img
        r = session.get(icon_img, timeout=10)
        file = open("imgs/" + str(id_str) + ".jpg", "wb")
        file.write(r.content)
        file.close()
        print("Save Img")

def DownloadTemplate():
    ydl_opts_icon = {'outtmpl': "template/"+id_str+".zip"}
    with youtube_dl.YoutubeDL(ydl_opts_icon) as ydl:
        ydl.download([url_template])
    print("Save Template")
    pass

def SaveData():
    #Download Img
    while True:
        try:
            DownloadImg()
            break
        except:
            time.sleep(10)
    #Download Temolate
    while True:
        try:
            DownloadTemplate()
            break
        except:
            time.sleep(10)
    sql = "INSERT INTO templates (id,title,link,url_from,icon,tags,authorname,doctype,layout,contrast,colours) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"
    val = (id_str,title,id_str+".zip",url_from,id_str+".jpg",rating,t_authorname,t_doctype,t_layout,t_contrast,t_colours)
    mycursor.execute(sql, val)
    mydb.commit()
    #Save Data In mysql

    print("Save Data")

print("Yes Start Script")
# GET Item
item = 0
for page in range(8,1000):
    if(page == item):
        urlnew = url+"/free-css-templates"
        print(urlnew)
    else:
        urlnew = url+"/free-css-templates?start="+str(item)
        print(urlnew)
    item = item + 12
    print("Page This >>>>>>> "+str(page))
    while True:
        try:
            r = requests.get(urlnew, timeout=10)
            break
        except:
            time.sleep(10)
    soup = BeautifulSoup(r.text, 'html.parser')
    soup_templates = soup.find('div',id='showcase')
    templates = soup_templates.find_all('a')
    print(len(templates))
    for template in templates:
        id_str = str(uuid.uuid1())
        title = template.find('img')['title']
        alt_img = template.find('img')['alt']
        url_from = url+template['href']
        t_colours = ""
        rating = ""
        sql = "SELECT url_from FROM templates WHERE url_from= %s"
        adr = (url_from,)
        mycursor.execute(sql, adr)
        myresult = mycursor.fetchall()
        mydb.commit()
        if len(myresult) > 0:
            print("find -->>>>>>> this >>>>>>> " + url_from)
        else:
            while True:
                try:
                    r_page = requests.get(url_from, timeout=10)
                    soup_page = BeautifulSoup(r_page.text, 'html.parser')
                    break
                except:
                    pass
            url_template = url+soup_page.find('li',class_='dld').find('a')['href']
            icon_img = url+soup_page.find("div",class_="fl_left").find('img')['src']
            mores = soup_page.find("div",class_="fl_right")

            t_authorname = mores.find("li", class_="authorname").find('strong').text
            t_layout = mores.find("li", class_="layout").text
            t_contrast = mores.find("li", class_="contrast").text
            t_doctype = mores.find("li", class_="doctype").text
            colours = mores.find("li", class_="colours")
            for mo in colours.findAll('img'):
                t_colours = t_colours + "|" + mo['title']

            tags = soup_page.find("div",class_="tags").findAll('li')

            for tag in tags:
                rating = rating + "|" + tag.text.lower()
            SaveData()
