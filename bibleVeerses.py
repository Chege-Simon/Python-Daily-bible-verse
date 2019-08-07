#!/usr/bin/python3

import tkinter as tk
from PIL import Image, ImageTk
import requests, bs4, os ,base64

# *****************************backend***********************************

os.makedirs('pics', exist_ok = True )
os.remove("pics/DailyVerse.jpg")

url = 'https://www.bible.com'
# Download the page.
print('Downloading page %s...' % url)
res = requests.get(url)
try:
	res.raise_for_status()
except Exception as exc:
		print('There was a problem: %s' % (exc))

soup = bs4.BeautifulSoup(res.text, "html.parser")
# Find the URL of the verse image.
picElem = soup.select('div img')
if picElem == [] or picElem == 'None':
	print('Could not find verse image.')
else:
	picUrl = 'http:' + picElem[4].get('src')
	print('Downloading image %s...' % (picUrl))
	res = requests.get(picUrl)
	try:
		res.raise_for_status()
	except Exception as exc:
		print('There was a problem: %s' % (exc))

		# Save the image to ./pics.
	imageFile = open(os.path.join('pics', os.path.basename('DailyVerse.jpg')), 'wb')
	for chunk in res.iter_content(100000):
		imageFile.write(chunk)
	imageFile.close()
print('Done.')


#*****************************frontend***********************************

HEIGHT = 900
WIDTH = 1200

root = tk.Tk()

canvas = tk.Canvas(root, height=HEIGHT, width=WIDTH)
canvas.pack()

frame = tk.Frame(root, bg='#80c1ff')
frame.place(relx=0.1, rely=0.1, relwidth=0.8, relheight = 0.8)

label = tk.Label(frame, text="Bible Verses", bg='green', font=40)
label.place(relx=0.1, rely=0, relwidth=0.8, relheight=0.2)

verseImage = ImageTk.PhotoImage(file = 'pics/DailyVerse.jpg')
verse = tk.Label(frame, image=verseImage)
verse.place(relx=0.1, rely=0.25, relwidth=0.8, relheight = 0.8)

root.mainloop()




