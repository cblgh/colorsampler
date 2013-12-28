import sys
import pyperclip
from PySide import QtCore
from PySide.QtGui import *
# Hover over a color and left click to get that color's hex code in your clipboard
# left click to sample the color you're hovering above
# right click to sample its complementary color
# escape/middle mouse button to exit, without sampling a color

class Colorsampler(QWidget):
    def __init__(self):
        super(Colorsampler, self).__init__()
        self.initUI()
        
    def initUI(self):      
        # remove the window borders
        hbox = QHBoxLayout(self)
        desktop = QApplication.desktop()
        # saved destkop.x() as self.desktopX because it is used in multiple places
        self.desktopX = desktop.x()
        self.image = QPixmap.grabWindow(desktop.winId(), self.desktopX, desktop.y(), desktop.width(),
                desktop.height()).toImage()
        pixmap = QPixmap(self.image)

        lbl = QLabel(self)
        lbl.setPixmap(pixmap)
        hbox.addWidget(lbl)
        hbox.setContentsMargins(0, 0, 0, 0)
        self.setLayout(hbox)

        self.colorLabel = QLabel(self)
        self.colorLabel.resize(20, 40)
        self.complementLabel = QLabel(self)
        self.complementLabel.resize(20, 40)
        
        # self.desktopX to handle multiscreen environments
        self.setWindowTitle('Colorsampler')
        self.setWindowFlags(QtCore.Qt.FramelessWindowHint)
        self.showFullScreen()
        self.move(self.desktopX, desktop.y())

    def eventFilter(self, source, event):
        if event.type() == QtCore.QEvent.KeyPress:
            if event.key() == QtCore.Qt.Key_Escape:
                sys.exit()
        elif event.type() == QtCore.QEvent.MouseMove:
            if event.button() == QtCore.Qt.NoButton:
                pos = event.pos()
                width = self.image.size().width()
                height = self.image.size().height()
                x = event.globalX()
                y = event.globalY()

                # if cursor is in the bottom right corner
                if  x - self.desktopX >= width - 61 and y >= height - 71:
                    self.colorLabel.move(width - 40, height - 40)
                    self.complementLabel.move(width - 20, height - 40)
                    pass
                elif x - self.desktopX >= width - 61:
                    self.colorLabel.move(width - 40, y + 30)
                    self.complementLabel.move(width - 20, y + 30)
                elif y >= height - 71:
                    self.colorLabel.move(x - self.desktopX + 20, height - 40)
                    self.complementLabel.move(x - self.desktopX + 40, height - 40)
                else:
                    self.colorLabel.move(x - self.desktopX + 20, y + 30)
                    self.complementLabel.move(x - self.desktopX + 40, y + 30)

                c = self.image.pixel(x - self.desktopX, y)
                color = QColor(c)
                complementColor = QColor(c)
                borderColor = "#000"
                if color.lightness() < 127:
                    borderColor = "#FFF"
                hue = color.getHsl()[0]
                if hue != - 1:
                    complementColor.setHsl(
                            hue + 180, color.getHsl()[1], color.getHsl()[2],color.getHsl()[3])

                stylesheet = "background-color: {}; border-style: {}; border-color: {}; border-width:1px"
                colorBorder = "dashed none dashed dashed"
                complementBorder = "dashed dashed dashed none"

                self.colorLabel.setStyleSheet(stylesheet.format(
                    color.name(), colorBorder, borderColor))
                self.complementLabel.setStyleSheet(stylesheet.format(
                    complementColor.name(), complementBorder, borderColor))
                if  x - self.desktopX >= width - 52 and y >= height - 62:
                    transparency = "background-color:rgba({},{},{}, 75%)"
                    self.colorLabel.setStyleSheet(transparency.format(color.red(),
                        color.green(), color.blue()))
                    self.complementLabel.setStyleSheet(transparency.format(complementColor.red(),
                        complementColor.green(), complementColor.blue()))
        elif event.type() == QtCore.QEvent.MouseButtonRelease:
            # get the color of the pixel the cursor is over
            c = self.image.pixel( - self.desktopX  +  event.globalX(), event.globalY())
            color = QColor(c)

            hue = color.getHsl()[0]
            complementColor = QColor(c)
            if hue !=  - 1:
                complementColor.setHsl(
                        hue + 180, color.getHsl()[1], color.getHsl()[2],color.getHsl()[3])

            # if right button, choose the complementary color
            if event.button() == QtCore.Qt.RightButton:
                color = complementColor
            # push to the chosen color to the clipboard
            if event.button() == QtCore.Qt.MidButton:
                sys.exit()
            else:
                pyperclip.copy(color.name()[1:].upper())
                sys.exit()
        return QMainWindow.eventFilter(self, source, event)

app = QApplication(sys.argv)
sampler = Colorsampler()
app.installEventFilter(sampler)
sys.exit(app.exec_())
