import os
import numpy as np
import cv2 as cv
#from PIL import Image
#def make_square(img, min_size=28, fill_color=(0, 0, 0, 0)):
#	im  = Image.open(img)	
#	x, y = im.size
#	size = max(min_size, x, y)
#	new_im = Image.new('RGB', (size, size), fill_color)
#	new_im.paste(im, (int((size - x) / 2), int((size - y) / 2)))
#	new_im.save(img)

path = './digits3'
dig = os.listdir('./digits3')
dig.sort()
dloc = []
maxsz = 0
for i in range(9):
	dig[i] = path + '/' + dig[i]
	dimg = os.listdir(dig[i])
	temp = []
	for imloc in dimg:
		temp.append(dig[i] + '/' + imloc)	
	dloc.append(temp)
#for i in dloc:
#	for j in i:
#		make_square(j)
arr = []
cnt = []
for i in dloc:
	cont = 0
	for j in i:
		img  = cv.imread(j)
		img = cv.resize(img, (28, 28))
		gray = cv.cvtColor(img,cv.COLOR_BGR2GRAY)
		arr.append(gray)
		cont = cont + 1
	cnt.append(cont)
x = np.array(arr)
print(x.shape)
train = x[:].reshape(-1,784).astype(np.float32)
train_labels = []
num = 0
for i in cnt:
	num = num+1
	for j in range(i) :
		train_labels.append([num])
train_labels = np.array(train_labels)
print(len(train_labels),len(train))
np.savez('print_digit3.npz',train=train, train_labels=train_labels)

