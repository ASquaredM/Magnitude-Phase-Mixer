import sys

import cv2 as cv
import numpy as np
from PyQt5 import QtCore, QtGui, QtWidgets

import UI
from imageModel import ImageModel as IM
from modesEnum import Modes


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
        self.Img1 = IM("results/test.jpg")
        self.Img2 = IM("results/test2.jpg")
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
        options = QtWidgets.QFileDialog.Options()
        options |= QtWidgets.QFileDialog.DontUseNativeDialog
        self.filePath, self.format = QtWidgets.QFileDialog.getOpenFileName(
            None,
            "Load Image",
            "",
            "Images (*.png *.xpm *.jpg);;",
            options=QtWidgets.QFileDialog.DontUseNativeDialog,
        )
        print("filepath is >>>>>",self.filePath)
        if self.filePath == "":
            pass
        else:
            self.Img[i] = IM(self.filePath)
            if str(type(self.Img[i].imgByte)) == "<class 'NoneType'>":
                self.ImgUp[i] = False
            else:
                if any(self.ImgUp):
                    if self.ImgUp[i] == False:
                        if self.Img[0].imgByte.shape == self.Img[1].imgByte.shape:
                            self.ImgUp[i] = True
                        else:
                            self.Img[i] = np.empty(0)
                            self.Viewers[i].clear()
                            self.Viewers[i + 2].clear()
                            #todo: add popUp
                    elif (self.ImgUp[i] == True) and (self.ImgUp[0] == self.ImgUp[1]):
                        if self.Img[0].imgByte.shape == self.Img[1].imgByte.shape:
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
            self.Viewers[i+1].setImage(self.Img[i-1].T)
        elif self.ImgUp[i] == True: 
            self.Viewers[i].setImage(self.Img[i].imgByte.T)
            self.Viewers[i + 2].setImage(self.Img[i].Comp[self.Combs[i].currentIndex()])
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
        
        
        R2 = (self.Slider2.value() / 100.0)
        
        if (self.Combs[3].currentIndex()-1):
            if self.Combs[4].currentIndex() == 1 or self.Combs[4].currentIndex() == 3:
                R1 = (self.Slider1.value() / 100.0)
                self.Img[1].ENABLE_UNIFORM_MAGNITUDE = False
            elif self.Combs[4].currentIndex() == 2 or self.Combs[4].currentIndex() == 4:
                R1 = (self.Slider2.value() / 100.0)
                self.Img[1].ENABLE_UNIFORM_PHASE = False
            
            if self.Combs[4].currentIndex() == 5:
                R1 = (self.Slider1.value() / 100.0)
                self.Img[1].ENABLE_UNIFORM_MAGNITUDE = True
            elif self.Combs[4].currentIndex() == 6:
                R1 = (self.Slider2.value() / 100.0)
                self.Img[1].ENABLE_UNIFORM_PHASE = True
        else:
            if self.Combs[4].currentIndex() == 1 or self.Combs[4].currentIndex() == 3:
                R1 = 1 - (self.Slider1.value() / 100.0)
                self.Img[0].ENABLE_UNIFORM_MAGNITUDE = False
            elif self.Combs[4].currentIndex() == 2 or self.Combs[4].currentIndex() == 4:
                R1 = 1 - (self.Slider2.value() / 100.0)
                self.Img[0].ENABLE_UNIFORM_PHASE = False
            elif self.Combs[4].currentIndex() == 5:
                R1 = 1 - (self.Slider1.value() / 100.0)
                self.Img[0].ENABLE_UNIFORM_MAGNITUDE = True
            elif self.Combs[4].currentIndex() == 6:
                R1 = 1 - (self.Slider2.value() / 100.0)
                self.Img[0].ENABLE_UNIFORM_PHASE = True
            #C1 = (R1*Comp(self.Img[1].imgByte.T, self.Comp1C_CombS.currentIndex()+4)) + ((1-R1)*Comp(self.Img[0].imgByte.T, self.Comp1C_CombS.currentIndex()+4))

        if (self.Combs[5].currentIndex() - 1):
            if self.Combs[6].currentIndex() == 1 or self.Combs[6].currentIndex() == 3:
                R2 = (self.Slider1.value() / 100.0)
                self.Img[1].ENABLE_UNIFORM_MAGNITUDE = False
            elif self.Combs[6].currentIndex() == 2 or self.Combs[6].currentIndex() == 4:
                R2 = (self.Slider2.value() / 100.0)
                self.Img[1].ENABLE_UNIFORM_PHASE = False
            
            if self.Combs[6].currentIndex() == 5:
                R2 = (self.Slider1.value() / 100.0)
                self.Img[1].ENABLE_UNIFORM_MAGNITUDE = True
            elif self.Combs[6].currentIndex() == 6:
                R2 = (self.Slider2.value() / 100.0)
                self.Img[1].ENABLE_UNIFORM_PHASE = True
        else:
            if self.Combs[4].currentIndex() == 1 or self.Combs[4].currentIndex() == 3:
                R2 = 1 - (self.Slider1.value() / 100.0)
                self.Img[0].ENABLE_UNIFORM_MAGNITUDE = False
            elif self.Combs[4].currentIndex() == 2 or self.Combs[4].currentIndex() == 4:
                R2 = 1 - (self.Slider2.value() / 100.0)
                self.Img[0].ENABLE_UNIFORM_PHASE = False
            elif self.Combs[4].currentIndex() == 5:
                R2 = 1 - (self.Slider1.value() / 100.0)
                self.Img[0].ENABLE_UNIFORM_MAGNITUDE = True
            elif self.Combs[4].currentIndex() == 6:
                R2 = 1 - (self.Slider2.value() / 100.0)
                self.Img[0].ENABLE_UNIFORM_PHASE = True
            #C2 = (R2*Comp(self.Img[0].imgByte.T, self.Comp2C_CombS.currentIndex()+4)) + ((1-R2)*Comp(self.Img[1].imgByte.T, self.Comp2C_CombS.currentIndex()+4))
        
        if self.Combs[4].currentIndex() == 1 or self.Combs[4].currentIndex() == 5:
            self.Img[i+1] = IM.mix(self.Img[1],self.Img[0],R1,R2,Modes.magnitudeAndPhase)
            self.Disp(i + 2, False)
        elif self.Combs[4].currentIndex() == 2 or self.Combs[4].currentIndex() == 6:
            self.Img[i+1] = IM.mix(self.Img[0],self.Img[1],R1,R2,Modes.magnitudeAndPhase)
            self.Disp(i + 2, False)
        elif self.Combs[4].currentIndex() == 3:
            self.Img[i+1] = IM.mix(self.Img[1],self.Img[0],R1,R2,Modes.realAndImaginary)
            self.Disp(i + 2, False)
        elif self.Combs[4].currentIndex() == 4:
            self.Img[i+1] = IM.mix(self.Img[0],self.Img[1],R1,R2,Modes.realAndImaginary)
            self.Disp(i + 2, False)

        
def main():
    app = QtWidgets.QApplication(sys.argv)
    mainWindow = QtWidgets.QMainWindow()
    ApplicationWindow(mainWindow)
    mainWindow.show()
    sys.exit(app.exec_())


if __name__ == "__main__":
    main()
