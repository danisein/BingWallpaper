
# -*- coding: UTF-8 -*-
import urllib as ulb
import urllib.request as ulb2
import json
import os
import sys
import ctypes
params = {}
params['format'] = 'js'
params['idx'] = '0'  #0 for today, 1 for yesterday and so on
params['n'] = '1'    #number of pics
params['uhd'] = '1'
params['uhdwidth'] = '3840'
params['uhdheight'] = '2160'

monitorIndex = -1; # 0 for monitor 1, 1 for monitor 2, -1 for all monitor
def update():
	#get the json info
	web_path = "http://www.bing.com/HPImageArchive.aspx"
	data = ulb.parse.urlencode(params)
	web_path = web_path + '?' + data
	# print(web_path)
	response = ulb2.urlopen(web_path)
	result = response.read()
	info = json.loads(result)
	# print(info)
	#get the image
	img_path = info['images'][0]['url']
	if img_path.find('http') < 0:
		img_path = 'http://www.bing.com' + img_path
	# print(img_path)
	response = ulb2.urlopen(img_path)
	result = response.read()
	if (len(result) > 0):
		img_file = '1.jpg'
		#write into a file
		f = open(img_file, 'wb')
		f.write(result)
		f.close()
		return img_file
	else:
		return ''

def setWallPaper(imagePath):
	dll = ctypes.windll.LoadLibrary(".\\IDesktopWallpaper.dll")
	# must be absolute path
	abspath = os.path.abspath(imagePath)
	dll.SetWallpaper(-1, abspath)


if __name__ == "__main__":
	if len(sys.argv) > 1:
		monitorIndex = int(sys.argv[1]);
	
	if monitorIndex >= 0:
		print("Update wallpaper for monitor ", monitorIndex + 1, ".")
	else:
		print("Update wallpaper for all monitor.")
	img_file = update()
	if img_file != '':
		setWallPaper(img_file)