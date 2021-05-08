import requests
import os
from urllib.request import urlopen
from lxml import etree
import csv

path = os.getcwd()

omistetutosakkeetlista = []
osinkoarvo = []
osinko = 0.0
numero = 0
rivinro = 0

url = 'https://www.is.fi/taloussanomat/osinkokalenteri/vuosi/2020/'

headers = {'Content-Type': 'text/html', }
response = requests.get(url, headers=headers)
html = response.text
f = open('star_wars_html', 'w', encoding='utf-8')
f.write(html)

# read local html file and set up lxml html parser
local = 'file:///C:/Users/Aarni-HY/Documents/star_wars_html'
response = urlopen(local)
htmlparser = etree.HTMLParser(encoding='utf-8')
tree = etree.parse(response, htmlparser)
table = tree.xpath("//table[@class='companydata__table sortable js-dividend-table']")[0]

for text in table.xpath(".//tbody[1]/tr"):
    rivinro += 1
    text2 = tree.xpath('/html/body/div[3]/main/div[3]/div/div/div/section/table/tbody/tr[' + str(rivinro) + ']/td[5]')
    text3 = tree.xpath('/html/body/div[3]/main/div[3]/div/div/div/section/table/tbody/tr[' + str(rivinro) + ']/td[1]/a')
    text2 = text2[0].text
    text3 = text3[0].text
    text2 = text2.replace(',', '.')
    text5 = text2[0:6]
    osinkoarvo.append((text3, text5))

with open('osakkeet.txt', newline='') as csvfile:
    omistetutosakkeet = csv.reader(csvfile, delimiter=',')
    for osakkeet in omistetutosakkeet:
        omistetutosakkeetlista.append(osakkeet)
    for omatosakkeet in omistetutosakkeetlista:
        for osakkeet3 in osinkoarvo:
            if osakkeet3[:][0].strip() == omatosakkeet[0]:
                print("Kokonaisosinko:",str(osinko)," €")
                osinko += ((float(osakkeet3[1])*float(omatosakkeet[1])))
                print("")
                print(osakkeet3[0],omatosakkeet[1],"kpl",osakkeet3[1],"€/kpl","Osinko yht.",str(float(osakkeet3[1])*float(omatosakkeet[1])),"€")

print("")
print("Kokonaisosinkotulot vuodessa:", osinko,"€")
print("Kokonaisosinkotulot kuukaudessa:", (osinko/12),"€")

input()