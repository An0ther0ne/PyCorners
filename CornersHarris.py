#-*- coding: utf-8 -*-

import os
import cv2
import PySimpleGUI 	as sg
from math import sin, pi

def viewImage(image, name_of_window):
	cv2.namedWindow(name_of_window, cv2.WINDOW_NORMAL)
	cv2.imshow(name_of_window, image)
	
imagefname = 'img/geometry.jpg'
color = [0,220,255]
maxcolorrange = 100

layout = [[
		sg.Image(filename='', key='-image-')
	],[
		sg.Text('', size=(30,1), text_color='Yellow', font='bold', key='-values-')
	],[
		sg.Text('K:', size=(10,1)), 
		sg.Slider(range=(1,100), disable_number_display=True, default_value=50, orientation='h', size=(33,20), key='-K_slide-')
	],[
		sg.Text('Block Size:', size=(10,1)),
		sg.Slider(range=(1,10), disable_number_display=True, default_value=2, orientation='h', size=(33,20), key='-Block_size-')
	],[
		sg.Text('Kernel Size:', size=(10,1)),
		sg.Slider(range=(1,15), disable_number_display=True, default_value=2, orientation='h', size=(33,20), key='-K_size-')
	],[
		sg.Text('Color:', size=(10,1)),
		sg.Slider(range=(1,maxcolorrange), disable_number_display=True, default_value=1, orientation='h', size=(33,20), key='-color-')
	],[
		sg.Button('Load Image', size=(12,1), pad=(80,1), font='Hevletica 14', key='-load-'), sg.Button('Exit', size=(7,1), font='Hevletica 14')
	],]

window = sg.Window('Corners Harris counting', layout, no_titlebar=False, location=(0,0))

image_elem  = window['-image-']
values_elem = window['-values-']

image = cv2.imread(imagefname)
igray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

old_Kslide_value = -1
old_Block_size = -1
old_K_size = -1
old_Scolor = -1

while True:
	event, values = window.read(timeout=50)
	if event == 'Exit' or event == None:
		break
	elif event == '-load-':
		path = sg.PopupGetFile(
					'Load Image', 
					title = 'Load image from file:', 
					default_extension = '.jpg',
					save_as = False,
					file_types = (('Images', '*.bmp;*gif;*.png;*.pcx;*.jpg'), ('bmp', '*.bmp'), ('gif', '*.gif'), ('pcx', '*.pcx'), ('png', '*.png'), ('jpg', '*.jpg'), ('All', '*.*')),
					no_window = True,
				)
		if os.path.exists(path) and os.path.isfile(path):
			imagefname = path
			image = cv2.imread(imagefname)
			igray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
			frame = image.copy()
			imgbytes = cv2.imencode('.png', frame)[1].tobytes()  # ditto
			image_elem.update(data=imgbytes)
	Kslide_value = values['-K_slide-']
	Block_size = int(values['-Block_size-'])
	K_size = int(values['-K_size-']) * 2 - 1 
	S_color = values['-color-']
	if (Kslide_value != old_Kslide_value) or (Block_size != old_Block_size) or (K_size != old_K_size) or (S_color != old_Scolor):
		if S_color != old_Scolor:
			old_Scolor = S_color
			R = min(255, int(300*sin(pi*float(S_color)/maxcolorrange)))
			G = min(255, max(0, int(300*sin(pi*float(S_color + maxcolorrange//3)/maxcolorrange))))
			B = min(255, max(0, int(300*sin(pi*float(S_color - maxcolorrange//3)/maxcolorrange))))
			color = [B,G,R]
		elif old_Kslide_value != Kslide_value:
			old_Kslide_value = Kslide_value
		elif old_Block_size != Block_size:
			old_Block_size = Block_size
		elif old_K_size != K_size:
			old_K_size = K_size
		dst = cv2.cornerHarris(igray, Block_size, K_size, Kslide_value/1000)	# img, blockSize, ksize, k
		dst = cv2.dilate(dst, None)
		frame = image.copy()
		frame[dst > 0.02 * dst.max()] = color
		imgbytes = cv2.imencode('.png', frame)[1].tobytes()  # ditto
		image_elem.update(data=imgbytes)
		values_elem.update("Block_size = {:2}, K_size = {:2}, K = {}".format(Block_size, K_size, Kslide_value/1000))
