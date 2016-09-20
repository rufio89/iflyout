from pytesseract import image_to_string
import PIL
import os
from PIL import Image, ImageEnhance
from os import walk
import re
import cv2
import shutil
import numpy as np




def get_subs(a_dir):
    return [name for name in os.listdir(a_dir)
            if os.path.isdir(os.path.join(a_dir, name))]

def delete_resize_files(folder):
	for the_file in os.listdir(folder):
		file_path = os.path.join(folder, the_file)
		try:
			if os.path.isfile(file_path):
				os.unlink(file_path)
			elif os.path.isdir(file_path): shutil.rmtree(file_path)
		except Exception as e:
			print(e)


def grab_data():
	path = '/home/www-data/web2py/applications/travel/static/images/user_images/'
	resize_path = '/home/www-data/web2py/applications/travel/static/images/resized/'
	usr_dirs = get_subs(path)

	for usr_dir in usr_dirs:
		f1 = []
		f2 = []
		image_text = [] 
		resize_path = resize_path + usr_dir
		path = path + usr_dir
		src_dirs = get_subs(path)
	#	print 'resize: ' + resize_path
	#	print 'path: ' + path
	#	print  src_dirs	
		for src_dir in src_dirs:
			resize_path = resize_path + '/' + src_dir
			path = path + '/' + src_dir
			dest_dirs = get_subs(path)
			delete_resize_files(resize_path)
	#		print 'resize: ' +resize_path
	#		print 'path: ' + path
	#		print  src_dirs	
			
			for dest in dest_dirs:
				resize_path = resize_path + '/' + dest
				path = path + '/' + dest
	#			print 'resize: ' +resize_path
	#			print 'path: ' + path

				if not os.path.exists(resize_path):
	    				os.makedirs(resize_path)


				for (dirpath, dirnames, filenames) in walk(path):
	        			f1.extend(filenames)
	#        			print filenames
					break
				filenames.sort()

				for f in filenames:
					basewidth = 1000
					reg_path = path + '/' + f
	#				print 'reg_path: ' + reg_path
					img2 = cv2.imread(reg_path,1)
					height, width, channels = img2.shape
					img2 = cv2.cvtColor(img2,cv2.COLOR_BGR2GRAY)
					img2 = img2[400:(height-148), 0:150]
					cv2.imwrite(resize_path + '/' +  f, img2)
					img = Image.open(resize_path + '/' +  f)
					wpercent = (basewidth/float(img.size[0]))
					hsize = int((float(img.size[1])*float(wpercent)))
					img = img.resize((basewidth,hsize), PIL.Image.ANTIALIAS)
					img.save(resize_path + '/' +  f,  dpi=(300,300))
					

				for (dirpath, dirnames, filenames_2) in walk(resize_path):
					f2.extend(filenames_2)
	    				break

				for idx, f2 in enumerate(filenames_2):
					newpath = resize_path  + '/' + f2
					im = Image.open(newpath)
					image_text.append(image_to_string(im))
					image_list = image_text[idx].splitlines()
					image_list = map(lambda image_list: image_list.replace(',',''), image_list)
					image_list = filter(None, image_list)
					image_list = filter(lambda name: name.strip(), image_list)
					for item in  image_list:
	# 					print item
						new_item = re.search(ur'([$])(\d+(?:\.\d{2})?)', item)
						if new_item is not None:	
							print  src_dir
							print  dest
							print f2
							print new_item.groups()[1]
							print f2.replace('flight', '')[:-16]
							print f2.replace('flight', '').replace('->','')[10:][:-4]
							
		
				resize_path = resize_path.replace('/' + dest, '')
				path = path.replace('/' + dest, '')
				f1 = []
				f2 = []
				image_text = []
				image_list = []
		resize_path = resize_path.replace(usr_dir + '/' + src_dir, '')
		path = path.replace(usr_dir + '/' + src_dir, '')
				

grab_data()