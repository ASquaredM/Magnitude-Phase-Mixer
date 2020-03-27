import numpy as np
import cv2 as cv

def Comp(Img, OP_CODE):
    f = np.fft.fft2(Img)
    FS = np.fft.fftshift(f)
    if  OP_CODE == 0 or OP_CODE == 1:
        magnitude_spectrum = 20*np.log(np.abs(FS))
        return magnitude_spectrum

    if OP_CODE == 2:
        phase_spectrum = np.angle(FS)
        return phase_spectrum

    if OP_CODE == 3:
        real_comp = 20*np.log(np.real(FS))
        return real_comp

    if OP_CODE == 4:
        imag_comp = np.imag(FS)
        return imag_comp
    
    if  OP_CODE == 5:
        magnitude_spectrum = np.abs(f)
        return magnitude_spectrum

    if OP_CODE == 6:
        phase_spectrum = np.angle(f)
        return phase_spectrum

    if OP_CODE == 7:
        real_comp = np.real(f)
        return real_comp

    if OP_CODE == 8:
        imag_comp = np.imag(f)
        return imag_comp