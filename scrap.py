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
            if '°' in str(j.find_all('td')[2].find('span', {'class': 'geo-dec'}).text.strip()):
                #print("Coordinates : "+j.find_all('td')[2].find('span', {'class': 'geo-dec'}).text.strip())  # lat lng N/S W/E
                s = str(j.find_all('td')[2].find('span', {'class': 'geo-dec'}).text.strip()).split()
                L1 = float(str(s[0][:-2]))
                L2 = float(str(s[1][:-2]))
                L1 = L1 if str(s[0][-2:]) == "°N" else -1*L1
                L2 = L2 if str(s[1][-2:]) == "°E" else -1*L2
            print("Current Status :",str(j.find_all('td')[3].text.strip())[-1] == '–')
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

############ create CSV

dict = {'Continent': csv_conti, 'Country': csv_contr, 'Launch_Site_name': csv_site,'Launch_site_link':csv_siteLink,'Latitude':csv_lat,'Longitude':csv_lng,'Opearating_years':csv_opDate,'Operating_status':csv_opStatus}

df = pd.DataFrame(dict)
 
print(df)

df.to_csv('Global_Launch_sites_022023.csv')
