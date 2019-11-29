from io import BytesIO

import requests
from PIL import Image
from bs4 import BeautifulSoup

response = requests.get('https://www.twitchmetrics.net/emotes').text
soup = BeautifulSoup(response, 'html.parser')

active_emotes = soup.find("div", class_="d-flex flex-wrap align-content-around")

emotes = active_emotes.find_all("div", class_="py-4 text-center")

f=open("guru99.txt", "a+")

for e in emotes:

	uri = e.img["src"] 
	name = e.samp.text
	file_name = e.samp.text.lower() + ".png" 
	if (name[0] == "[") or (name[0] =="\\"):
		continue
	
	response = requests.get(uri)
	img = Image.open(BytesIO(response.content))
	basewidth = 25
	wpercent = (basewidth/float(img.size[0]))
	hsize = int((float(img.size[1])*float(wpercent)))
	img = img.resize((basewidth,hsize), Image.ANTIALIAS)
	img.save(file_name) 
	f.write(file_name + "\t\t\t" + name + "\n")
	print(uri)
	print(file_name) 	


f.close() 



