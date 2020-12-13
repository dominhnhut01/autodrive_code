from PIL import Image
import numpy as np
import random as rd
import os
from img_resize import resize

def crop(img_dir,mask_dir):
	ran = range(50,100)
	for file in filter(os.path.isfile,[img_dir+'/'+file for file in os.listdir(img_dir)]):
		file_name=os.path.basename(file)
		h_ratio= rd.choice(ran)/100.00
		w_ratio= rd.choice(ran)/100.00
		img=Image.open(img_dir+'/'+file_name)
		mask=Image.open(mask_dir+'/'+file_name)
		w,h=img.size
		new_h=int(round(h*h_ratio,0))
		new_w=int(round(w*w_ratio,0))
		new_img=img.crop((0,0,new_w,new_h))
		new_img.save(img_dir+'/'+'crop/'+file_name)
		new_mask=mask.crop((0,0,new_w,new_h))
		new_mask.save(mask_dir+'/'+'crop/'+file_name)
	resize(img_dir+'/crop')
	resize(mask_dir+'/crop')

def rename(img_dir,mask_dir):
	i=4458
	crop_img_dir=img_dir
	crop_mask_dir=mask_dir
	for file in filter(os.path.isfile,[crop_img_dir+'/'+file for file in os.listdir(crop_img_dir)]):
		old_name=os.path.basename(file)
		new_name='NYC_{}_.png'.format(i)
		os.rename(crop_img_dir+'/'+old_name,crop_img_dir+'/'+new_name)
		os.rename(crop_mask_dir+'/'+old_name,crop_mask_dir+'/'+new_name)
		i+=1
	print(i)
	print('done')
	for file in filter(os.path.isfile,[crop_img_dir+'/'+file for file in os.listdir(crop_img_dir)]):
		old_name=os.path.basename(file)
		new_name=old_name[:-5]+'.png'
		os.rename(crop_img_dir+'/'+old_name,crop_img_dir+'/'+new_name)
		os.rename(crop_mask_dir+'/'+old_name,crop_mask_dir+'/'+new_name)
if __name__=='__main__':
	img_dir = input('Please input your satellite image directory: ')
	mask_dir = input('Please input your mask directory: ')
	#crop(img_dir,mask_dir)
	rename(img_dir,mask_dir)