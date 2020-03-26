import numpy as np
import cv2 as cv

def Comp(Img, o):
    f = np.fft.fft2(Img)
    f = np.fft.fftshift(f)
    if  o == 0 or o == 1:
        magnitude_spectrum = 20*np.log(np.abs(f))
        return magnitude_spectrum

    if o == 2:
        phase_spectrum = np.angle(f)
        return phase_spectrum

    if o == 3:
        real_comp = 20*np.log(np.real(f))
        return real_comp

    if o == 4:
        imag_comp = np.imag(f)
        return imag_comp

#def Mix()