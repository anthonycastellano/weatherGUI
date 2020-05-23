#RPi weather gui 1.0
from tkinter import *
import tkinter as tk
from urllib.request import urlopen, Request
from bs4 import BeautifulSoup as soup
from PIL import Image, ImageTk

#hourly weather stats
def generate_stats():
	my_url = "https://weather.com/weather/hourbyhour/l/Leesburg+VA?canonicalCityId=7957afaa7b463a5dd6ed79c1391cd3222b40688674af35bf9fb9df27b3b44b41"
	headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2228.0 Safari/537.3'}
	req = Request(url =  my_url, headers=headers)
	page_html = urlopen(req).read()
	page_soup = soup(page_html, "html.parser")
	box = page_soup.find("div",{"id":"main-HourlyForecast-d2067ef5-92a1-4934-944c-b13028e80af9"})

	rows = box.findAll("td",{"classname":"twc-sticky-col  "})
	time_day = []
	for row in rows:
		time = row.find("div",{"class":"hourly-time"}).text.rstrip()
		day = row.find("div",{"class":"hourly-date"}).text.rstrip()
		time_day.append([time, day])

	rows = box.findAll("tr",{"classname":"clickable closed"}) + box.findAll("tr",{"classname":" closed"})
	temp_precip = []
	for row in rows:
		temp = row.find("td",{"class":"temp"}).text
		precip = row.find("td",{"class":"precip"}).text
		temp_precip.append([temp, precip])

	hourly_stats = []
	for item in range(len(time_day)):
		hourly_stats.append([time_day[item][0], time_day[item][1], temp_precip[item][0], temp_precip[item][1]])

	#current weather stats
	my_url = "https://weather.com/weather/today/l/7fd3e8cb2920f5ad9969ea4cefc03229d0f1b2606e54ed7d904e9061f5e7351c"
	headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2228.0 Safari/537.3'}
	req = Request(url =  my_url, headers=headers)
	page_html = urlopen(req).read()
	page_soup = soup(page_html, "html.parser")

	try:
		temp = page_soup.find("div",{"class":"today_nowcard-temp"}).text
		phrase = page_soup.find("div",{"class":"today_nowcard-phrase"}).text
	except:
		print("ERROR: couldn't fetch current data")
		temp = "loading..."
		phrase = "loading..."
		pass
	current_stats = [temp, phrase]

	return hourly_stats, current_stats


#GUI
hourly_stats, current_stats = generate_stats()
fullScreenState = True
REFRESH_TIME = 300000
HEIGHT = 600
WIDTH = 1024

def quitFullScreen(event):
	fullScreenState = False
	root.attributes('-fullscreen', fullScreenState)
	quit(0)

def current_refresh():
	hourly_stats, current_stats = generate_stats()
	temp_text.set("Current Temp: " + current_stats[0])
	phrase_text.set(current_stats[1])

	for i in range(10):
		date_string_vars[i].set(hourly_stats[i][0] + " " + hourly_stats[i][1])
		temp_string_vars[i].set("Temp: " + hourly_stats[i][2])
		precip_string_vars[i].set("Precip: " + hourly_stats[i][3])

	current_temp.after(REFRESH_TIME, current_refresh)

root = tk.Tk()
root.attributes('-fullscreen', True)
root.bind("<Escape>", quitFullScreen)

C = Canvas(root, height=HEIGHT, width=WIDTH)
filename = PhotoImage(file = "bg.png")
bg_label = Label(root, image=filename)
bg_label.place(x=0, y=0, relwidth = 1, relheight = 1)
C.pack()

temp_text = StringVar()
temp_text.set("Current Temp: " + current_stats[0])
current_temp = Label(root, textvariable=temp_text, bd=0, fg='white', bg='#B2B2B2', font=('Arial', '60','normal'))
current_temp.place(x=100,y=100)
current_temp.after(REFRESH_TIME, current_refresh)

phrase_text = StringVar()
phrase_text.set(current_stats[1])
current_phrase = Label(root, textvariable=phrase_text, bd=0, fg='white', bg='#B2B2B2', font=('Arial', '40', 'normal'))
current_phrase.place(x=100,y=190)

xPos = 85
yPos = 340
date_string_vars = []
temp_string_vars = []
precip_string_vars = []
for i in range(10):
	date_string_vars.append(StringVar())
	date_string_vars[i].set(hourly_stats[i][0] + " " + hourly_stats[i][1])

	temp_string_vars.append(StringVar())
	temp_string_vars[i].set("Temp: " + hourly_stats[i][2])

	precip_string_vars.append(StringVar())
	precip_string_vars[i].set("Precip: " + hourly_stats[i][3])

	date = Label(root, textvariable=date_string_vars[i], fg='white', bg='#B2B2B2', font=('Arial', '16', 'bold'))
	date.place(x=xPos, y=yPos)

	temp = Label(root, textvariable=temp_string_vars[i], fg='white', bg='#B2B2B2', font=('Arial', '12', 'normal'))
	temp.place(x=xPos+20, y=yPos+30)

	precip = Label(root, textvariable=precip_string_vars[i], fg='white', bg='#B2B2B2', font=('Arial', '12', 'normal'))
	precip.place(x=xPos+13, y=yPos+52)

	xPos += 180
	if i == 4:
		yPos += 110
		xPos = 85

root.mainloop()
