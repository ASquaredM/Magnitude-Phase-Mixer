import sys

import cv2 as cv
import numpy as np
from PyQt5 import QtCore, QtGui, QtWidgets

import UI
from GetDataFromFile import getDataFromAFile
from Image import Comp


class ApplicationWindow(UI.Ui_MainWindow):
    def __init__(self, mainWindow):
        super(ApplicationWindow, self).setupUi(mainWindow)

        self.DisableMixer()
        self.Init()

        self.Viewers = [
            self.Img1_Disp,
            self.Img2_Disp,
            self.Img1_CDisp,
            self.Img2_CDisp,
            self.Out1,
            self.Out2,
        ]

        self.Combs = [
            self.Img1_Comb, self.Img1_Comb_2, self.Output_Comb,
            self.Comp1_CombS, self.Comp1C_CombS, self.Comp2_CombS,
            self.Comp2C_CombS
        ]

        self.i = 0
        while (self.i < 6):
            self.Viewers[self.i].ui.histogram.hide()
            self.Viewers[self.i].ui.roiBtn.hide()
            self.Viewers[self.i].ui.roiPlot.hide()
            self.Viewers[self.i].ui.menuBtn.hide()
            self.i += 1

        self.Upbtn1.clicked.connect(lambda: self.Disp(0, True))
        self.Upbtn2.clicked.connect(lambda: self.Disp(1, True))

        self.Img1_Comb.currentIndexChanged.connect(lambda: self.Disp(0, False))
        self.Img1_Comb_2.currentIndexChanged.connect(lambda: self.Disp(1, False))
        self.Output_Comb.currentIndexChanged.connect(lambda: self.Mixer(self.Output_Comb.currentIndex()))

        self.SlidersInit()

    def Init(self):
        self.ImgUp = [False, False,False,False]
        self.Img1 = np.empty(0,dtype=complex)
        self.Img2 = np.empty(0,dtype=complex)
        self.Mix1 = np.empty(0,dtype=complex)
        self.Mix2 = np.empty(0,dtype=complex)
        self.Img = [self.Img1, self.Img2,self.Mix1,self.Mix2]

    def DisableMixer(self):
        self.Output_Comb.setEnabled(False)
        self.Comp1_CombS.setEnabled(False)
        self.Slider1.setEnabled(False)
        self.Comp1C_CombS.setEnabled(False)
        self.Comp2_CombS.setEnabled(False)
        self.Slider2.setEnabled(False)
        self.Comp2C_CombS.setEnabled(False)

    def EnableMixer(self):
        self.Output_Comb.setEnabled(True)
        self.Comp1_CombS.setEnabled(True)
        self.Slider1.setEnabled(True)
        self.Comp1C_CombS.setEnabled(True)
        self.Comp2_CombS.setEnabled(True)
        self.Slider2.setEnabled(True)
        self.Comp2C_CombS.setEnabled(True)

    def SlidersInit(self):
        self.Slider1.setMaximum(100)
        self.Slider1.setSingleStep(10)
        self.Slider1.setSliderPosition(50)
        self.Slider1.setTracking(False)
        self.Slider1.valueChanged.connect(lambda: print(self.Slider1.sliderPosition()))
        self.Slider2.setMaximum(100)
        self.Slider2.setSingleStep(10)
        self.Slider2.setSliderPosition(50)
        self.Slider2.setTracking(False)
        self.Slider2.valueChanged.connect(lambda: print(self.Slider1.sliderPosition()))

    def GetImage(self, i):
        filePath = QtWidgets.QFileDialog.getOpenFileName(
            None, 'load', "./", "All Files *;")
        self.Img[i] = getDataFromAFile(filePath)
        if str(type(self.Img[i])) == "<class 'NoneType'>":
            self.ImgUp[i] = False
        else:
            if any(self.ImgUp):
                if self.ImgUp[i] == False:
                    if self.Img[0].shape == self.Img[1].shape:
                        self.ImgUp[i] = True
                    else:
                        self.Img[i] = np.empty(0)
                        self.Viewers[i].clear()
                        self.Viewers[i + 2].clear()
                        #todo: add popUp
                elif (self.ImgUp[i] == True) and (self.ImgUp[0] == self.ImgUp[1]):
                    if self.Img[0].shape == self.Img[1].shape:
                        self.ImgUp[i] = True
                    else:
                        self.Img[i] = np.empty(0)
                        self.ImgUp[i] = False
                        self.Viewers[i].clear()
                        self.Viewers[i + 2].clear()
                        #todo: add popUp
            else:
                self.ImgUp[i] = True

    def Disp(self, i, GI):
        if GI == True:
            self.GetImage(i)

        if i == 3 or i == 4:
            self.Viewers[i+1].setImage(self.Img[i-1])
        elif self.ImgUp[i] == True: 
            self.Viewers[i].setImage(self.Img[i].T)
            self.Viewers[i + 2].setImage(Comp(self.Img[i].T,self.Combs[i].currentIndex()))
            if self.Combs[i].currentIndex() == 0:
                self.Combs[i].setCurrentIndex(1)

        if self.ImgUp[0] and self.ImgUp[1]:
            self.EnableMixer()
        else:
            self.DisableMixer()

    def Mixer(self, i):
        if self.Output_Comb.currentIndex() == 0:
            self.Output_Comb.setCurrentIndex(1)
            i = 1
        if self.Comp1_CombS.currentIndex() == 0:
            self.Comp1_CombS.setCurrentIndex(1)
        if self.Comp2_CombS.currentIndex() == 0:
            self.Comp2_CombS.setCurrentIndex(2)
        if self.Comp1C_CombS.currentIndex() == 0:
            self.Comp1C_CombS.setCurrentIndex(1)
        if self.Comp2C_CombS.currentIndex() == 0:
            self.Comp2C_CombS.setCurrentIndex(2)
        
        R1 = (self.Slider1.value() / 100.0)
        R2 = (self.Slider2.value() / 100.0)
        
        if (self.Comp1_CombS.currentIndex()-1):
            C1 = (R1*Comp(self.Img[1].T, self.Comp1C_CombS.currentIndex()+4)) + ((1-R1)*Comp(self.Img[0].T, self.Comp1C_CombS.currentIndex()+4)) 
        else:
            C1 = (R1*Comp(self.Img[0].T, self.Comp1C_CombS.currentIndex()+4)) + ((1-R1)*Comp(self.Img[1].T, self.Comp1C_CombS.currentIndex()+4))
        
        if (self.Comp2_CombS.currentIndex()-1):
            C2 = (R2*Comp(self.Img[1].T, self.Comp2C_CombS.currentIndex()+4)) + ((1-R2)*Comp(self.Img[0].T, self.Comp2C_CombS.currentIndex()+4)) 
        else:
            C2 = (R2*Comp(self.Img[0].T, self.Comp2C_CombS.currentIndex()+4)) + ((1-R2)*Comp(self.Img[1].T, self.Comp2C_CombS.currentIndex()+4))
        
        if self.Comp1C_CombS.currentIndex() == 1 or self.Comp1C_CombS.currentIndex() == 5:
            self.Img[i + 1] = np.real(np.fft.ifft2(np.multiply(C1,np.exp(1j * C2))))
            self.Disp(i + 2, False)
        elif self.Comp1C_CombS.currentIndex() == 2 or self.Comp1C_CombS.currentIndex() == 6:
            self.Img[i + 1] = np.real(np.fft.ifft2(np.multiply(C2,np.exp(1j * C1))))
            self.Disp(i + 2, False)
def main():
    app = QtWidgets.QApplication(sys.argv)
    mainWindow = QtWidgets.QMainWindow()
    ApplicationWindow(mainWindow)
    mainWindow.show()
    sys.exit(app.exec_())


if __name__ == "__main__":
    main()
