import numpy as np
import cv2
import argparse
kernel_size = 4
s = 0.84
stride = 1
def gaussian_kernel(l = 5,s = 0.84):
    r = int(l/2)
    a = np.mgrid[-r:r+1,-r:r+1]
    g = np.exp(-(a[0]**2 + a[1]**2)/(2*(s**2)))
    return g/np.sum(g)
def gaussian_blur(img,kernel):
    (h,w) = (img.shape[0],img.shape[1])
    (kh,kw) = (kernel.shape[0],kernel.shape[1])
    for i in range(0,h,stride):
        for j in range(0,w,stride):
            try:
                img[int((2*i + kh)/2)][int((2*j + kw)/2)] = np.sum(kernel*img[i:i+kh,j:j+kw])
            except:
                pass

kernel = gaussian_kernel(l = kernel_size,s = s)

ap = argparse.ArgumentParser()
ap.add_argument("-i","--image",required = True)
args = vars(ap.parse_args())

img = cv2.imread(args['image'],0)

gaussian_blur(img,kernel)
cv2.imshow('blurred',img)
while cv2.waitKey(3) != 27:
    pass
cv2.destroyAllWindows()
