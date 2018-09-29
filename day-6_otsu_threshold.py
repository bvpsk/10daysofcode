import numpy as np
import cv2
import argparse
import imutils
def otsu(img):
    hist = np.zeros(256)
    for_hist = img.copy().flatten()
    for i in for_hist:
        hist[i] += 1
    total_pixels = img.shape[0]*img.shape[1]
    reci_of_pixels = 1.0/float(total_pixels)
    order = np.arange(256)
    cumulative_weights = np.zeros(256)
    cumulative_weights[0] = float(hist[0])/total_pixels
    for i in range(1,len(hist)):
        cumulative_weights[i] = cumulative_weights[i-1] + float(hist[i])/total_pixels
    for_mu = order*hist
    threshold = 0
    between_class_variance = -1
    for t in range(1,256):
        # wb = cumulative_weights[t-1]
        # wf = reci_of_pixels - wb
        # mu_b = np.sum(for_mu[:t-1])/(wb*total_pixels)
        # mu_f = np.sum(for_mu[t-1:])/(wf*total_pixels)
        pcb = np.sum(hist[:t])
        pcf = np.sum(hist[t:])
        wb = pcb/total_pixels
        wf = pcf/total_pixels
        mu_b = np.sum(order[:t]*hist[:t])/float(pcb)
        mu_f = np.sum(order[t:]*hist[t:])/float(pcf)
        if between_class_variance < wb*wf*(mu_b - mu_f)**2:
            between_class_variance = wb*wf*(mu_b - mu_f)**2
            threshold = t
    return threshold

ap = argparse.ArgumentParser()
ap.add_argument("-i","--image",required = True)
args = vars(ap.parse_args())

image = cv2.imread(args['image'])
img = cv2.cvtColor(image,cv2.COLOR_BGR2GRAY)

threshold = otsu(img)
ret,thr = cv2.threshold(img, 0, 255, cv2.THRESH_OTSU)
print threshold
print ret
thresh = img.copy()
thresh[thresh < threshold] = 0
thresh[thresh != 0] = 255
thr = imutils.resize(thr,width = 400)
thresh = imutils.resize(thresh,width = 400)
image = imutils.resize(image,width = 400)
cv2.imshow("cv2",thr)
cv2.imshow("thresh",thresh)
cv2.imshow("original",image)
while cv2.waitKey(33) != 27:
    pass
cv2.destroyAllWindows()
