import UI
from PyQt5 import QtCore, QtGui, QtWidgets
import sys
import numpy as np
from GetDataFromFile import getDataFromAFile
import cv2 as cv
from Image import Mag,Phase,Real,Imag


class ApplicationWindow(UI.Ui_MainWindow):
    def __init__(self,mainWindow):
        super(ApplicationWindow,self).setupUi(mainWindow)
        
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
            self.Img1_Comb,
            self.Img1_Comb_2,
            self.Output_Comb,
            self.Comp1_CombS,
            self.Comp1C_CombS,
            self.Comp2_CombS,
            self.Comp2C_CombS
        ]
        
        self.i = 0
        while(self.i < 6):
            self.Viewers[self.i].ui.histogram.hide()
            self.Viewers[self.i].ui.roiBtn.hide()
            self.Viewers[self.i].ui.roiPlot.hide()
            self.Viewers[self.i].ui.menuBtn.hide()
            self.i += 1

        self.Upbtn1.clicked.connect(lambda: self.Disp(0,True))
        self.Upbtn2.clicked.connect(lambda: self.Disp(1,True))

        self.Img1_Comb.currentIndexChanged.connect(lambda: self.Disp(0,False))
        self.Img1_Comb_2.currentIndexChanged.connect(lambda: self.Disp(1,False))

    def Init(self):
        self.ImgUp = [False,False]

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

    def GetImage(self,i):
        filePath=QtWidgets.QFileDialog.getOpenFileName(None,  'load', "./","All Files *;")
        if i == 0:
            self.Img1 = getDataFromAFile(filePath) #if getDataFromAFile(filePath) is not None else self.MainData
            self.Img2 = getDataFromAFile(filePath)
        if i == 1:
            self.Img2 = getDataFromAFile(filePath) #if getDataFromAFile(filePath) is not None else self.MainData
        self.Img = [self.Img1,self.Img2]

        if str(type(self.Img[i])) == "<class 'NoneType'>":
            self.ImgUp[i] = False
        else:
            self.ImgUp[i] = True

    def Disp(self,i,GI):
        if GI == True:
            self.GetImage(i)

        if self.ImgUp[i] == True:
            self.Viewers[i].setImage(self.Img[i].T)
            print(self.Img[i])
            if self.Combs[i].currentIndex() == 0:
                self.Viewers[i+2].setImage(Mag(self.Img[i].T))
                self.Combs[i].setCurrentIndex(1)
            if self.Combs[i].currentIndex() == 1:
                self.Viewers[i+2].setImage(Mag(self.Img[i].T))
            if self.Combs[i].currentIndex() == 2:
                self.Viewers[i+2].setImage(Phase(self.Img[i].T))
            if self.Combs[i].currentIndex() == 3:
                self.Viewers[i+2].setImage(Real(self.Img[i].T))
            if self.Combs[i].currentIndex() == 4:
                self.Viewers[i+2].setImage(Imag(self.Img[i].T))
        




def main():
    app=QtWidgets.QApplication(sys.argv)
    mainWindow=QtWidgets.QMainWindow()
    ApplicationWindow(mainWindow)
    mainWindow.show()
    sys.exit(app.exec_())
    
if __name__ == "__main__":
    main()