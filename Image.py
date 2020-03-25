import numpy as np
import cv2 as cv

def Mag(Img):
    f = np.fft.fft2(Img)
    f = np.fft.fftshift(f)
    magnitude_spectrum = 20*np.log(np.abs(f))
    return magnitude_spectrum

def Phase(Img):
    f = np.fft.fft2(Img)
    f = np.fft.fftshift(f)
    phase_spectrum = np.angle(f)
    return phase_spectrum

def Real(Img):
    f = np.fft.fft2(Img)
    f = np.fft.fftshift(f)
    real_comp = 20*np.log(np.real(f))
    return real_comp

def Imag(Img):
    f = np.fft.fft2(Img)
    imag_comp = np.imag(f)
    return imag_comp
