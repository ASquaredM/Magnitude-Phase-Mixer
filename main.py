import UI
from PyQt5 import QtCore, QtGui, QtWidgets
import sys
import numpy as np
from GetDataFromFile import getDataFromAFile
import cv2 as cv


class ApplicationWindow(UI.Ui_MainWindow):
    def __init__(self,mainWindow):
        super(ApplicationWindow,self).setupUi(mainWindow)

        self.Viewers = [
            self.Img1_Disp,
            self.Img1_CDisp,
            self.Img2_Disp,
            self.Img2_CDisp,
            self.Out1,
            self.Out2,
        ]
        self.i = 0
        while(self.i < 6):
            self.Viewers[self.i].ui.histogram.hide()
            self.Viewers[self.i].ui.roiBtn.hide()
            self.Viewers[self.i].ui.roiPlot.hide()
            self.Viewers[self.i].ui.menuBtn.hide()
            self.i += 1

        self.Upbtn1.clicked.connect(lambda: self.OpenFile(0))
        self.Upbtn2.clicked.connect(lambda: self.OpenFile(2))

    def OpenFile(self,i):
        filePath=QtWidgets.QFileDialog.getOpenFileName(None,  'load', "./","All Files *;;" "*.wav;;")
        self.Img = getDataFromAFile(filePath) #if getDataFromAFile(filePath) is not None else self.MainData
        self.Viewers[i].setImage(self.Img.T)
        self.f = np.fft.fft2(self.Img)
        self.fshift = np.fft.fftshift(self.f)
        self.magnitude_spectrum = 20*np.log(np.abs(self.fshift))
        self.Viewers[i+1].setImage(self.magnitude_spectrum)




def main():
    app=QtWidgets.QApplication(sys.argv)
    mainWindow=QtWidgets.QMainWindow()
    ApplicationWindow(mainWindow)
    mainWindow.show()
    sys.exit(app.exec_())
    
if __name__ == "__main__":
    main()