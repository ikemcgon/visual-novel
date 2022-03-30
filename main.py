from PyQt5 import QtWidgets
import csv
import cv2
import textwrap
import os.path
import numpy as np
from PIL import Image

def load_save():
	n = 0
	bif = "default.png"

	if not os.path.exists('save.csv'):
		file = open('save.csv','a+')
		file.close()
	else:		
		with open('save.csv', newline='') as csvfile:
			spamreader = csv.reader(csvfile, delimiter=' ', quotechar='|')
			for row in spamreader:
				n = row[0][:-1]
				bif = row[1]

	return int(n), bif

def load_script(fname):
	txt = open(os.path.join('scripts',fname), 'r')
	return txt.readlines()

def load_bg(bif):
	back = Image.open(os.path.join('bg',bif))
	return back.resize((1200,800))

def load_fg(fif):
	fore = Image.open(os.path.join('fg',fif))
	w, h = fore.size
	return fore.resize((int(w * 1.5), int(h * 1.5)))

def load_tb(tif):
	fore = Image.open(os.path.join('tb',tif))
	w, h = fore.size
	return fore.resize((1200, 800))

def combine_bgfg(bg, fg):
	# Place foreground image in center of background
	wb, hb = bg.size
	wf, hf = fg.size
	x = wb//2 - wf//2
	y = hb - hf
	bg.paste(fg, (x, y), fg)
	return bg

def combine_center(bg, fg):
	wb, hb = bg.size
	wf, hf = fg.size
	x = wb//2 - wf//2
	y = hb//2 - hf//2
	bg.paste(fg, (x, y), fg)
	return bg

def convert(pil_img):
	# Convert PIL image to OpenCV
	open_cv_image = np.array(pil_img)
	return open_cv_image[:, :, ::-1].copy()

def update_speaker(img, txt):
	w, h, l = img.shape

	# Font stylings
	font = cv2.FONT_HERSHEY_SIMPLEX
	org = (10, h // 2 - 50)
	fontScale = 1
	color = (0, 0, 255)
	thickness = 2

	return cv2.putText(img, txt, org, font, fontScale, color, thickness, cv2.LINE_AA)

def update_text(img, txt):
	w, h, l = img.shape

	# Font stylings
	font = cv2.FONT_HERSHEY_SIMPLEX
	x = 10
	y = h // 2
	font_size = 1
	font_thickness = 2
	fontScale = 1
	color = (255, 255, 255)
	thickness = 2

	wrapped_text = textwrap.wrap(txt, width=60)
	for i, ln in enumerate(wrapped_text):
		textsize = cv2.getTextSize(ln, font, font_size, font_thickness)[0]

		gap = textsize[1] + 10

		y = y + i * gap
		x = x

		cv2.putText(img, ln, (x, y), font, font_size, color, font_thickness, lineType = cv2.LINE_AA)
	


if __name__ == "__main__":
	# Load save and script files
	nbr, bgImgFile = load_save()
	script = load_script('danganronpa.txt')

	# Load in textbox
	tbImgFile = 'dthh.png'
	tbImg = load_tb(tbImgFile)

	# Read script line for line
	for line in script:
		# Catch up to save point
		if nbr != 0:
			nbr = nbr - 1
			continue

		# Check if line contains a scene definition
		if line.split(':')[0]=='SCENE':
			# Load scene first with no characters
			bgImgFile = line.split(':')[1][:-1]
			bgImg = load_bg(bgImgFile)
			cbImg = convert(bgImg)
		else:
			# Parse character image, name, and text from script
			fgImgFile = line.split(':')[0]
			charName = line.split(':')[1]
			text = line.split(':')[2][:-1]

			# Compile all info into a single image
			fgImg = load_fg(fgImgFile)
			bgImg = load_bg(bgImgFile)
			cbImg = combine_bgfg(bgImg, fgImg)
			cbImg = combine_center(cbImg, tbImg)
			cbImg = convert(cbImg)
			cbImg = update_speaker(cbImg, charName)
			update_text(cbImg, text)

		# Display image until player inputs
		cv2.imshow('Visual Novel - Main Screen', cbImg)
		cv2.waitKey(0)

	# End game
	cv2.destroyAllWindows()
	

