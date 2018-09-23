import numpy as np
import argparse
import cv2
import imutils
from skimage.exposure import rescale_intensity

upper_threshold = 75
lower_threshold = upper_threshold*0.35

ap = argparse.ArgumentParser()
ap.add_argument("-i","--image",required = True)
args = vars(ap.parse_args())

img = cv2.imread(args['image'],0)
# img = imutils.resize(img,300)

def convolve(output,img,kernel,stride):
    (o_h,o_w) = output.shape
    (k_h,k_w) = kernel.shape
    for i in range(0,o_h,stride):
        for j in range(0,o_w,stride):
            output[i,j] = np.sum(kernel*img[i:i+k_h,j:j+k_w])
    # output = rescale_intensity(output, in_range=(0, 255))
    output = np.absolute(output)
    output = output/np.max(output)
    output = (output * 255).astype("uint8")
    return output


# Gaussian filter script starts here.......
gaussian_kernel_size = 3
gaussian_s = 0.84
gaussian_stride = 1
def gaussian_kernel(l = 5,s = 0.84):
    r = int(l/2)
    a = np.mgrid[-r:r+1,-r:r+1]
    g = np.exp(-(a[0]**2 + a[1]**2)/(2*(s**2)))
    return g/np.sum(g)
def gaussian_blur(img,kernel):
    (h,w) = (img.shape[0],img.shape[1])
    (kh,kw) = (kernel.shape[0],kernel.shape[1])
    for i in range(0,h,gaussian_stride):
        for j in range(0,w,gaussian_stride):
            try:
                img[int((2*i + kh)/2)][int((2*j + kw)/2)] = np.sum(kernel*img[i:i+kh,j:j+kw])
            except:
                pass

print("[INFO]Building Gaussian kernel of size {}...".format(gaussian_kernel_size))
gaussian_kernel = gaussian_kernel(l = gaussian_kernel_size,s = gaussian_s)
#gaussian_blur(img,kernel)

#   Gaussian filter finished.........

#   Sobel edge detection script starts here........

sobel_kernel_x = np.array(([[-1,0,1],[-2,0,2],[-1,0,1]]),dtype = 'int')
sobel_kernel_y = np.array(([[-1,-2,-1],[0,0,0],[1,2,1]]),dtype = 'int')
sobel_stride = 1
print("[INFO]Applying Gaussian Blur...")
gaussian_blur(img,np.rot90(gaussian_kernel,2))
grad_x = np.zeros(((img.shape[0] - sobel_kernel_x.shape[0])/sobel_stride + 1,(img.shape[1] - sobel_kernel_x.shape[1])/sobel_stride + 1))
grad_y = np.zeros(((img.shape[0] - sobel_kernel_y.shape[0])/sobel_stride + 1,(img.shape[1] - sobel_kernel_y.shape[1])/sobel_stride + 1))
print("[INFO]Calculating sobelX...")
grad_x = convolve(grad_x,img,np.rot90(sobel_kernel_x,0),sobel_stride)
print("[INFO]Calculating sobelY...")
grad_y = convolve(grad_y,img,np.rot90(sobel_kernel_y,0),sobel_stride)
print("[INFO]Applying Bitwise OR...")
grad = cv2.bitwise_or(np.uint8(np.absolute(grad_x)),np.uint8(np.absolute(grad_y)))

#   Sobel edge detection completed........

#   Starting Non-Maximum Suppression.......

print("[INFO]Calculating Angles...")
theta = np.arctan2(grad_y,grad_x)*180.0/np.pi
for i in range(theta.shape[0]):
    for j in range(theta.shape[1]):
        if theta[i,j] >= -22.5 and theta[i,j] < 22.5:
            theta[i,j] = 0
        elif theta[i,j] >= 22.5 and theta[i,j] < 67.5:
            theta[i,j] = 1
        elif theta[i,j] >= 67.5 and theta[i,j] < 112.5:
            theta[i,j] = 2
        elif theta[i,j] >= 122.5 and theta[i,j] < 157.5:
            theta[i,j] = 3
        elif theta[i,j] > -157.5 and theta[i,j] <= 157.5:
            theta[i,j] = 0
        elif theta[i,j] > -122.5 and theta[i,j] <= -157.5:
            theta[i,j] = 1
        elif theta[i,j] > -67.5 and theta[i,j] <= -122.5:
            theta[i,j] = 2
        elif theta[i,j] > -22.5 and theta[i,j] <= -67.5:
            theta[i,j] = 3
nonmax = grad.copy()
print("[INFO]Applying Nonmax suppression...")
for h in range(0,grad.shape[0],1):
    for w in range(0,grad.shape[1],1):
        try:
            key = theta[(2*h+3)/2,(2*w+3)/2]
            if key == 0:
                if not(grad[(2*h+3)/2,(2*w+3)/2] > grad[(2*h+3)/2,(2*w+3)/2 - 1] and grad[(2*h+3)/2,(2*w+3)/2] > grad[(2*h+3)/2,(2*w+3)/2 + 1]):
                    nonmax[(2*h+3)/2,(2*w+3)/2] = 0
            elif key == 1:
                if not(grad[(2*h+3)/2,(2*w+3)/2] > grad[(2*h+3)/2 - 1,(2*w+3)/2 + 1] and grad[(2*h+3)/2,(2*w+3)/2] > grad[(2*h+3)/2 + 1,(2*w+3)/2] - 1):
                    nonmax[(2*h+3)/2,(2*w+3)/2] = 0
            elif key == 2:
                if not(grad[(2*h+3)/2,(2*w+3)/2] > grad[(2*h+3)/2 - 1,(2*w+3)/2] and grad[(2*h+3)/2,(2*w+3)/2] > grad[(2*h+3)/2 + 1,(2*w+3)/2]):
                    nonmax[(2*h+3)/2,(2*w+3)/2] = 0
            elif key == 3:
                if not(grad[(2*h+3)/2,(2*w+3)/2] > grad[(2*h+3)/2 - 1,(2*w+3)/2 - 1] and grad[(2*h+3)/2,(2*w+3)/2] > grad[(2*h+3)/2 + 1,(2*w+3)/2 + 1]):
                    nonmax[(2*h+3)/2,(2*w+3)/2] = 0
        except:
            pass

#   Non max suppression completed.......

#   Starting Hysterisis thresholding.........

thresh = nonmax.copy()

thresh[thresh<upper_threshold] = 0
cv2.imshow("i",thresh)

print("[INFO]Applying Hysterisis Thresholding...")
for h in range(0,grad.shape[0],1):
    for w in range(0,grad.shape[1],1):
        if thresh[h,w] != 0:
            try:
                key = theta[(2*h+3)/2,(2*w+3)/2]
                if key == 0:
                    if (theta[(2*h+3)/2,(2*w+3)/2 - 1] == key and grad[(2*h+3)/2,(2*w+3)/2 - 1] > lower_threshold) or(theta[(2*h+3)/2,(2*w+3)/2 + 1] == key and grad[(2*h+3)/2,(2*w+3)/2 + 1] > lower_threshold):
                        thresh[(2*h+3)/2,(2*w+3)/2 - 1] = grad[(2*h+3)/2,(2*w+3)/2 - 1]
                        thresh[(2*h+3)/2,(2*w+3)/2 + 1] = grad[(2*h+3)/2,(2*w+3)/2 + 1]
                elif key == 1:
                    if (theta[(2*h+3)/2 -1,(2*w+3)/2 + 1] == key and grad[(2*h+3)/2 - 1,(2*w+3)/2 + 1] > lower_threshold) or(theta[(2*h+3)/2 + 1,(2*w+3)/2 - 1] == key and grad[(2*h+3)/2 + 1,(2*w+3)/2 - 1] > lower_threshold):
                        thresh[(2*h+3)/2 - 1,(2*w+3)/2 + 1] = grad[(2*h+3)/2 - 1,(2*w+3)/2 + 1]
                        thresh[(2*h+3)/2 + 1,(2*w+3)/2 - 1] = grad[(2*h+3)/2 + 1,(2*w+3)/2 - 1]
                elif key == 2:
                    if (theta[(2*h+3)/2 -1,(2*w+3)/2] == key and grad[(2*h+3)/2 - 1,(2*w+3)/2] > lower_threshold) or(theta[(2*h+3)/2 + 1,(2*w+3)/2] == key and grad[(2*h+3)/2 + 1,(2*w+3)/2] > lower_threshold):
                        thresh[(2*h+3)/2 - 1,(2*w+3)/2] = grad[(2*h+3)/2 - 1,(2*w+3)/2]
                        thresh[(2*h+3)/2 + 1,(2*w+3)/2] = grad[(2*h+3)/2 + 1,(2*w+3)/2]
                elif key == 3:
                    if (theta[(2*h+3)/2 -1,(2*w+3)/2 - 1] == key and grad[(2*h+3)/2 - 1,(2*w+3)/2 - 1] > lower_threshold) or(theta[(2*h+3)/2 + 1,(2*w+3)/2 + 1] == key and grad[(2*h+3)/2 + 1,(2*w+3)/2 + 1] > lower_threshold):
                        thresh[(2*h+3)/2 - 1,(2*w+3)/2 - 1] = grad[(2*h+3)/2 - 1,(2*w+3)/2 - 1]
                        thresh[(2*h+3)/2 + 1,(2*w+3)/2 + 1] = grad[(2*h+3)/2 + 1,(2*w+3)/2 + 1]
            except:
                pass


#   Hysterisis Thresholding completed.......

cv2.imshow('nonmax',nonmax)
cv2.imshow('thresh',thresh)
while cv2.waitKey(3) != 27:
    pass
cv2.destroyAllWindows()
