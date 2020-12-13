from PIL import Image
import os

def resize(direc):
	for file in os.listdir(direc):
		filename = file[:-4]
		n_width = 220
		n_len = 436
		img=Image.open('{}/{}'.format(direc,file))
		img = img.resize((n_len,n_width), Image.ANTIALIAS)
		img.save('{}/{}.png'.format(direc,filename))

if __name__=='__main__':
	direc= input('Please input your directory: ')
	resize(direc)