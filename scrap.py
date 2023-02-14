from bs4 import BeautifulSoup
import requests
import pandas as pd

continents = ["Africa","Asia","Europe","North America","South America","Oceania","In water"]
csv_conti = []
csv_contr = []
csv_site = []
csv_siteLink = []
csv_lat = []
csv_lng = []
csv_opDate = []
csv_opStatus = []

response = requests.get(
    'https://en.wikipedia.org/wiki/List_of_rocket_launch_sites')

soup = BeautifulSoup(response.content, 'html.parser')

each_table = soup.find_all('table', attrs={'class': 'wikitable sortable'})

count = 0

conti = 0

for i in each_table:
    for j in i.find_all('tr'):
        try:
            # print("Continent : "+continents[conti])
            
            # print("Country : ",j.find_all('td')[0].find('a').text.strip())  # country Name
            
            # print("link : ","https://en.wikipedia.org"+str(j.find_all('td')[1].find('a', href=True)[
            #       'href']))  # wiki link for launch site
            # launch site name
            # print("Launch Site Name : ",j.find_all('td')[1].find('a').text.strip())
            if '°' in str(j.find_all('td')[2].find('span', {'class': 'geo-dec'}).text.strip()):
                #print("Coordinates : "+j.find_all('td')[2].find('span', {'class': 'geo-dec'}).text.strip())  # lat lng N/S W/E
                s = str(j.find_all('td')[2].find('span', {'class': 'geo-dec'}).text.strip()).split()
                L1 = float(str(s[0][:-2]))
                L2 = float(str(s[1][:-2]))
                L1 = L1 if str(s[0][-2:]) == "°N" else -1*L1
                L2 = L2 if str(s[1][-2:]) == "°E" else -1*L2
                # print("Coordinates (Lat/Long) :",L1,L2)
            #print("operating date : "+j.find_all('td')[3].text.strip())  # opreational date
            #print(str(j.find_all('td')[3].text.strip())[-1])
            print("Current Status :",str(j.find_all('td')[3].text.strip())[-1] == '–')

            # print("No. Launches : "+j.find_all('td')[4].text.strip())  # number of launches
            # print("Max Payload (KG): "+str(j.find_all('td')[5].text.strip()).replace(" ","").replace("kg",""))  # heaviest
            # print("Max Altitude : "+j.find_all('td')[6].text.strip())  # highest
            count += 1
            csv_conti.append(str(continents[conti]))
            csv_contr.append(str(j.find_all('td')[0].find('a').text.strip()))
            csv_site.append(str(j.find_all('td')[1].find('a').text.strip()))
            csv_siteLink.append("https://en.wikipedia.org"+str(j.find_all('td')[1].find('a', href=True)['href']))
            csv_lat.append(L1)
            csv_lng.append(L2)
            csv_opDate.append(str(j.find_all('td')[3].text.strip()))
            csv_opStatus.append(str(j.find_all('td')[3].text.strip())[-1] == '–')
        except:
            print("Yo Error")
            pass
    conti+=1

print("# # ##### # #")
print(count)
print(len(csv_conti))
print(len(csv_contr))
print(len(csv_site))
print(len(csv_siteLink))
print(len(csv_lat))
print(len(csv_lng))
print(len(csv_opDate))
print(len(csv_opStatus))

############ create CSV

dict = {'Continent': csv_conti, 'Country': csv_contr, 'Launch_Site_name': csv_site,'Launch_site_link':csv_siteLink,'Latitude':csv_lat,'Longitude':csv_lng,'Opearating_years':csv_opDate,'Operating_status':csv_opStatus}

df = pd.DataFrame(dict)
 
print(df)

df.to_csv('Global_Launch_sites_022023.csv')