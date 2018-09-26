import numpy as np
from time import time
def dft(x):
    N = x.shape[0]
    n = np.arange(N)
    k = n.reshape((N, 1))
    M = np.exp(-2j * np.pi * k * n / N)
    return np.dot(M, x)


def fft(x):
    N = x.shape[0]
    if N <= 1:
        return x
    else:
        even = fft(x[0::2])
        odd  = fft(x[1::2])
        odd = [odd[k] * np.exp(-2j*np.pi*k/N) for k in range(int(N/2))]
        return np.array(list(even+odd)+list(even-odd))


def ifft(x):
    #   ifft(x) = 1/N * (conj(FFT(conj(x))))
    N = x.shape[-1]
    fft_for_conj_x = fft(np.conjugate(x))
    conj_of_fft = np.conjugate(fft_for_conj_x)
    return np.real(conj_of_fft/N)

x = np.arange(8)
print x.shape
f = fft(x)
fi = ifft(f)

t= time()
mf = fft(x)
print("for fft : {}".format(time() - t))
t= time()
fi = ifft(mf)
print("for ifft : {}".format(time() - t))
t= time()
nf = np.fft.fft(x)
print("for numpy fft : {}".format(time() - t))
t= time()
nfi = np.fft.ifft(nf)
print("for numpy ifft : {}".format(time() - t))
print np.allclose(mf,nf)
print np.allclose(fi,nfi)
