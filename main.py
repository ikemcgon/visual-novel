import csv
import cv2
import textwrap
import sys
import os
import multiprocessing
import numpy as np
import playsound as ps
from PIL import Image

class VisualRunner:
	def __init__(self):
		# Load menu assets
		bgImgFile, bgmFile, title, ngText, cgText, exText = self.load_menu()
		bgm = self.load_bgm(bgmFile)
		bgm.start()
		menuStatus = 0

		# Initialize menu window
		while True:
			# Menu background and text
			bgImg = self.load_bg(bgImgFile)
			cbImg = self.convert(bgImg)
			self.update_menu(cbImg, title, ngText, cgText, exText, menuStatus)
			cv2.imshow('Visual Novel - Main Screen', cbImg)

			# Accept user input
			key = cv2.waitKeyEx(0)
			if key == 27:
				# Quit on ESC
				bgm.terminate()
				quit()
			if key == 2490368:
				# Go up in menu
				menuStatus = (menuStatus - 1) % 3
			if key == 2621440:
				# Go down in menu
				menuStatus = (menuStatus + 1) % 3
			if key == 13:
				# Select menu item
				bgm.terminate()
				if menuStatus == 0:
					# Play new game
					self.run_game()
				elif menuStatus == 1:
					# Play game from save
					self.run_game(True)
				elif menuStatus == 2:
					# Exit game
					quit()

	def run_game(self, load=False):
		# Initialize audio status
		vcFile = ""
		bgmFile = ""

		# Load save and script files
		script = self.load_script('script.txt')
		if load:
			nbr, bgImgFile, bgmFile = self.load_state()
			bgm = self.load_bgm(bgmFile)
			bgm.start()
		else:
			nbr, bgImgFile = 0, ""

		# Load in textbox
		tbImgFile = 'dthh.png'
		tbImg = self.load_tb(tbImgFile)

		# Read script line for line
		n = -1
		for line in script:
			n = n + 1

			# Catch up to save point
			if nbr != 0:
				nbr = nbr - 1
				continue

			# Check if line contains a scene definition
			if line.split(':')[0]=='SCENE':
				if bgmFile:
					bgm.terminate()

				# Load scene first with no characters
				bgmFile = line.split(':')[1]
				bgImgFile = line.split(':')[2][:-1]
				bgImg = self.load_bg(bgImgFile)
				cbImg = self.convert(bgImg)
				bgm = self.load_bgm(bgmFile)
				bgm.start()
			else:
				# Parse character image, name, and text from script
				fgImgFile = line.split(':')[0]
				vcFile = line.split(':')[1]
				charName = line.split(':')[2]
				text = line.split(':')[3][:-1]
				#print(fgImgFile, vcFile, charName, text)

				# Compile all info into a single image
				fgImg = self.load_fg(fgImgFile)
				bgImg = self.load_bg(bgImgFile)
				cbImg = self.combine_bgfg(bgImg, fgImg)
				cbImg = self.combine_center(cbImg, tbImg)
				cbImg = self.convert(cbImg)
				cbImg = self.update_speaker(cbImg, charName)

				# Update window
				if vcFile:
					vc = self.load_vc(vcFile)
					vc.start()
				self.update_text(cbImg, text)

			# Display image until player inputs
			cv2.imshow('Visual Novel - Main Screen', cbImg)
			key = cv2.waitKey(0)
			if key == 27:
				if vcFile:
					vc.terminate()
				bgm.terminate()
				self.save_state(n, bgImgFile, bgmFile)
				quit()

			if vcFile:
				vc.terminate()

		# End game
		bgm.terminate()
		cv2.destroyAllWindows()
		quit()

	def load_menu(self):
		with open(os.path.join('data','menu.csv'), newline='') as csvfile:
			spamreader = csv.reader(csvfile, delimiter=',', quotechar='|')
			for row in spamreader:
				bg = row[0]
				bgm = row[1]
				tit = row[2]
				ng = row[3]
				cg = row[4]
				ex = row[5]

		return bg, bgm, tit, ng, cg, ex

	def load_state(self):
		n = 0
		bif = "default.png"

		if not os.path.exists(os.path.join('data','save.csv')):
			file = open(os.path.join('data','save.csv'),'a+')
			file.close()
		else:		
			with open(os.path.join('data','save.csv'), newline='') as csvfile:
				spamreader = csv.reader(csvfile, delimiter=',', quotechar='|')
				for row in spamreader:
					n = row[0]
					bif = row[1]
					bgm = row[2]

		return int(n), bif, bgm

	def save_state(self, n, bif, bgm):
		if not os.path.exists('save.csv'):
			file = open(os.path.join('data','save.csv'),'a+')
			file.close()

		with open(os.path.join('data','save.csv'), 'w', newline='') as csvfile:
			writer = csv.writer(csvfile, delimiter=',', quotechar='|')
			writer.writerow([n, bif, bgm])
			csvfile.close()

	def load_script(self, fname):
		txt = open(os.path.join('data',fname), 'r')
		return txt.readlines()

	def load_bg(self, bif):
		back = Image.open(os.path.join('bg',bif))
		return back.resize((1200,800))

	def load_fg(self, fif):
		fore = Image.open(os.path.join('fg',fif))
		w, h = fore.size
		return fore.resize((int(w * 1.5), int(h * 1.5)))

	def load_tb(self, tif):
		fore = Image.open(os.path.join('tb',tif))
		w, h = fore.size
		return fore.resize((1200, 800))

	def load_vc(self, vc):
		return multiprocessing.Process(target=ps.playsound, args=(os.path.join('vc',vc),))

	def load_bgm(self, ost):
		return multiprocessing.Process(target=self.play_bgm, args=(ost,))

	def play_bgm(self, ost):
		while True:
			ps.playsound(os.path.join('ost',ost), True)

	def combine_bgfg(self, bg, fg):
		# Place foreground image in center of background
		wb, hb = bg.size
		wf, hf = fg.size
		x = wb//2 - wf//2
		y = hb - hf
		bg.paste(fg, (x, y), fg)
		return bg

	def combine_center(self, bg, fg):
		wb, hb = bg.size
		wf, hf = fg.size
		x = wb//2 - wf//2
		y = hb//2 - hf//2
		bg.paste(fg, (x, y), fg)
		return bg

	def convert(self, pil_img):
		# Convert PIL image to OpenCV
		open_cv_image = np.array(pil_img)
		return open_cv_image[:, :, ::-1].copy()

	def update_menu(self, img, tit, ng, cg, ex, stat):
		w, h, l = img.shape

		# Font stylings
		font = cv2.FONT_HERSHEY_TRIPLEX
		fontScale = 1
		color = (51, 47, 46)
		sel_color = (255, 255, 255)
		thickness = 2

		# Title text
		x, y = w // 4, h // 4
		cv2.putText(img, tit, (x, y), font, 2.5*fontScale, color, 3*thickness, cv2.LINE_AA)

		# Highlight based on state
		if stat == 0:
			x, y = w // 2, h // 3
			cv2.putText(img, ng, (x, y), font, 1.5 * fontScale, sel_color, 3*thickness, cv2.LINE_AA)
		elif stat == 1:
			x, y = w // 2, h // 3 + 50
			cv2.putText(img, cg, (x, y), font, 1.5 * fontScale, sel_color, 3*thickness, cv2.LINE_AA)
		elif stat == 2:
			x, y = w // 2, h // 3 + 100
			cv2.putText(img, ex, (x, y), font, 1.5 * fontScale, sel_color, 3*thickness, cv2.LINE_AA)

		# New Game, Continue, Exit texts
		x, y = w // 2, h // 3
		cv2.putText(img, ng, (x, y), font, 1.5*fontScale, color, thickness, cv2.LINE_AA)
		x, y = w // 2, h // 3 + 50
		cv2.putText(img, cg, (x, y), font, 1.5*fontScale, color, thickness, cv2.LINE_AA)
		x, y = w // 2, h // 3 + 100
		return cv2.putText(img, ex, (x, y), font, 1.5*fontScale, color, thickness, cv2.LINE_AA)

	def update_speaker(self, img, txt):
		w, h, l = img.shape

		# Font stylings
		font = cv2.FONT_HERSHEY_SIMPLEX
		org = (10, h // 2 - 50)
		fontScale = 1
		color = (0, 0, 255)
		thickness = 2

		return cv2.putText(img, txt, org, font, fontScale, color, thickness, cv2.LINE_AA)

	def update_text(self, img, txt):
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
	multiprocessing.freeze_support()
	vn = VisualRunner()
	

