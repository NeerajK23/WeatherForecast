from flask import Flask,render_template, request,url_for
import pywapi
import requests
from bs4 import BeautifulSoup

app=Flask(__name__)


def get_city_name_list(city_name):
    #this will give you a dictionary of all cities in the world with this city's name Be specific (city, country)!
    lookup = pywapi.get_location_ids(city_name)
    return lookup

def fetch_data(city_id,forecaste_type):
    url="https://weather.com/en-IN/weather/{}/l/{}:1:IN".format(forecaste_type,city_id)
    page=requests.get(url)

    soup=BeautifulSoup(page.content,"html.parser")

    if forecaste_type=="tenday":
        div_class_name="locations-title ten-day-page-title"
    elif forecaste_type=="5day":
        div_class_name="locations-title five-day-page-title"

    all=soup.find("div",{"class":div_class_name}).find("h1").text
    table=soup.find_all("table",{"class":"twc-table"})
    list_of_data=[]
    for items in table:
        for i in range(len(items.find_all("tr"))-1):
            d = {}
            d["day"]=items.find_all("span",{"class":"date-time"})[i].text
            d["date"]=items.find_all("span",{"class":"day-detail"})[i].text
            d["desc"]=items.find_all("td",{"class":"description"})[i].text
            d["temp"]=items.find_all("td",{"class":"temp"})[i].text
            d["precip"]=items.find_all("td",{"class":"precip"})[i].text
            d["wind"]=items.find_all("td",{"class":"wind"})[i].text
            d["humidity"]=items.find_all("td",{"class":"humidity"})[i].text
            list_of_data.append(d)

    return list_of_data

@app.route('/')
def name():
   return render_template('enterplace.html')

@app.route('/place',methods = ['POST', 'GET'])
def place():
   if request.method == 'POST':
      city_name = request.form['Name']
      list_of_cities=get_city_name_list(city_name)
      return render_template("list_of_cities.html",list_of_cities = list_of_cities)

@app.route('/finalcode',methods = ['POST', 'GET'])
def citykey():
    forecaste_type=request.form['forecaste_type']
    final_city_code = request.form['final_city']
    forecasted_data=fetch_data(final_city_code,forecaste_type)
    return render_template("show_data.html",forecasted_data = forecasted_data)

if __name__== '__main__':
    app.run(debug=True,host='0.0.0.0',port=5002, threaded=True)


