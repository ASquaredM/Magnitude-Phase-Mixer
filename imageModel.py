## This is the abstract class that the students should implement  

import cv2 as cv
import numpy as np

from modesEnum import Modes


class ImageModel():

    """
    A class that represents the ImageModel"
    """
    def __init__(self, imgPath: str):
        self.imgPath = imgPath
        print(imgPath)
        ###
        # ALL the following properties should be assigned correctly after reading imgPath 
        ###
        self.imgByte = cv.imread(self.imgPath,cv.IMREAD_GRAYSCALE)  
        self.dft = np.fft.fft2(self.imgByte)
        self.real = np.real(self.dft)
        self.imaginary = np.imag(self.dft)
        self.magnitude = np.abs(self.dft)
        self.phase = np.angle(self.dft)
        
        #Shifted and Normalized Atrributes for displaying
        self.Sdft = np.fft.fftshift(self.dft)
        self.SNreal = 20*np.log(np.real(self.Sdft))
        self.Simaginary = np.imag(self.Sdft)
        self.SNmagnitude = 20*np.log(np.abs(self.Sdft))
        self.Nphase = np.angle(self.Sdft)

        #Uniform components
        self.Umagnitude = np.ones(len(self.magnitude))
        self.Uphase = np.zeros(len(self.phase))
        self.ENABLE_UNIFORM_MAGNITUDE = False
        self.ENABLE_UNIFORM_PHASE = False

        self.Comp = [self.SNmagnitude, self.SNmagnitude, self.Nphase, self.SNreal, self.Simaginary, self.magnitude,
            self.phase, self.real, self.imaginary,self.Umagnitude,self.Uphase]
                
    def mix(self, imageToBeMixed: 'ImageModel', magnitudeOrRealRatio: float, phaesOrImaginaryRatio: float, mode: 'Modes') -> np.ndarray:
        """
        a function that takes ImageModel object mag ratio, phase ratio 
        """
        ### 
        # implement this function
        ###
        if mode == Modes.magnitudeAndPhase:
            if self.ENABLE_UNIFORM_MAGNITUDE:
                C1 = magnitudeOrRealRatio * self.Umagnitude + ((1 - magnitudeOrRealRatio) * imageToBeMixed.magnitude)
            else:
                C1 = magnitudeOrRealRatio * self.magnitude + ((1 - magnitudeOrRealRatio) * imageToBeMixed.magnitude)
            
            if self.ENABLE_UNIFORM_PHASE:
                C2 = phaesOrImaginaryRatio * self.Uphase + ((1 - phaesOrImaginaryRatio) * imageToBeMixed.phase)
            else:
                C2 = phaesOrImaginaryRatio * self.phase + ((1 - phaesOrImaginaryRatio) * imageToBeMixed.phase)
            Mixed = np.real(np.fft.ifft2(np.multiply(C1,np.exp(1j * C2))))
        
        elif mode == Modes.realAndImaginary:
            C1 = magnitudeOrRealRatio * self.real + ((1 - phaesOrImaginaryRatio) * imageToBeMixed.real)
            C2 = phaesOrImaginaryRatio * self.imaginary + ((1 - phaesOrImaginaryRatio) * imageToBeMixed.imaginary)
            Mixed = np.real(np.fft.ifft2(C1 + C2*1j))
       
        return Mixed
