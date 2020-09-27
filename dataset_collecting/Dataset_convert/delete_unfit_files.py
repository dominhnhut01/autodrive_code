import os

def delete(jpg_dir,npy_dir):
	files_keep = os.listdir(jpg_dir)
	for i in range(len(files_keep)):
		temp = files_keep[i]
		files_keep[i]='NYC_{}.tif'.format(temp[12:-4])
	print(files_keep)
	for npy_file in os.listdir(npy_dir):
		if npy_file not in files_keep:
			try:
				os.remove('{}/{}'.format(npy_dir,npy_file))
				print('Done')
			except:
				continue
				
if __name__ == '__main__':
	jpg_dir = input('Input the directory of your jpg folder: ')
	npy_dir = input('Input the directory of your npy folder: ')
	delete(jpg_dir,npy_dir)