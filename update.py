
# -*- coding: UTF-8 -*-
import urllib as ulb
import urllib2 as ulb2
import json
import win32gui,win32con,win32api
from PIL import Image
import os
params = {}
params['format'] = 'js'
params['idx'] = '0'  #0 for today, 1 for yesterday and so on
params['n'] = '1'    #number of pics

def update():
	#get the json info
	web_path = "http://www.bing.com/HPImageArchive.aspx"
	data = ulb.urlencode(params)
	web_path = web_path + '?' + data
	# print web_path
	response = ulb2.urlopen(web_path)
	result = response.read()
	info = json.loads(result)
	# print info
	#get the image
	img_path = info['images'][0]['url']
	if img_path.find('http') < 0:
		img_path = 'http://www.bing.com' + img_path
	# print img_path
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


StoreFolder = "c:\\dayImage"

def setWallpaperFromBMP(imagepath):
    k = win32api.RegOpenKeyEx(win32con.HKEY_CURRENT_USER,"Control Panel\\Desktop",0,win32con.KEY_SET_VALUE)
    win32api.RegSetValueEx(k, "WallpaperStyle", 0, win32con.REG_SZ, "2") #2拉伸适应桌面,0桌面居中
    win32api.RegSetValueEx(k, "TileWallpaper", 0, win32con.REG_SZ, "0")
    win32gui.SystemParametersInfo(win32con.SPI_SETDESKWALLPAPER,imagepath, 1+2)

def setWallPaper(imagePath):
    """
    Given a path to an image, convert it to bmp and set it as wallpaper
    """
    bmpImage = Image.open(imagePath)
    newPath = StoreFolder + '\\mywallpaper.bmp'
    try:
    	os.mkdir(StoreFolder)
    except:
    	pass
    bmpImage.save(newPath, "BMP")
    setWallpaperFromBMP(newPath)


if __name__ == "__main__":
	img_file = update()
	if img_file != '':
		setWallPaper(img_file)