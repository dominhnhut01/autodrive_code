import os

def delete(jpg_dir,npy_dir):
	jpg_files = os.listdir(jpg_dir)
	for i in range(len(jpg_files)):
		temp = jpg_files[i]
		jpg_files[i]=temp[:-4]
	for npy_file in os.listdir(npy_dir):
		if npy_file not in jpg_files:
			try:
				os.remove('{}/{}'.format(npy_dir,npy_file))
				print('Done')
			except:
				continue

if __name__ == '__main__':
	jpg_dir = input('Input the directory of your jpg folder: ')
	npy_dir = input('Input the directory of your npy folder: ')
	delete(jpg_dir,npy_dir)