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
        self.Img1_Comb_2.currentIndexChanged.connect(
            lambda: self.Disp(1, False))

    def Init(self):
        self.ImgUp = [False, False]
        self.Img1 = np.empty(0)
        self.Img2 = np.empty(0)
        self.Img = [self.Img1, self.Img2]

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

        if self.ImgUp[i] == True:
            self.Viewers[i].setImage(self.Img[i].T)
            self.Viewers[i + 2].setImage(Comp(self.Img[i].T,self.Combs[i].currentIndex()))
            if self.Combs[i].currentIndex() == 0:
                self.Combs[i].setCurrentIndex(1)

        if self.ImgUp[0] and self.ImgUp[1]:
            self.EnableMixer()
        else:
            self.DisableMixer()


def main():
    app = QtWidgets.QApplication(sys.argv)
    mainWindow = QtWidgets.QMainWindow()
    ApplicationWindow(mainWindow)
    mainWindow.show()
    sys.exit(app.exec_())


if __name__ == "__main__":
    main()
