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
        self.labelHeight = 40
        self.labelWidth = 20
        self.colorLabel.resize(self.labelWidth, self.labelHeight)
        self.complementLabel = QLabel(self)
        self.complementLabel.resize(self.labelWidth, self.labelHeight)
        
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
                width = self.image.size().width()
                height = self.image.size().height()
                mouseX = event.globalX()
                mouseY = event.globalY()
                offsetY = 30

                # color acquiring time
                c = self.image.pixel(mouseX - self.desktopX, mouseY)
                color = QColor(c)
                complementColor = QColor(c)
                borderColor = "#000"
                if color.lightness() < 127:
                    borderColor = "#FFF"

                hue = color.getHsl()[0]
                if hue != - 1:
                    complementColor.setHsl(hue + 180, color.getHsl()[1], color.getHsl()[2], color.getHsl()[3])

                # now if that ain't stylin i just don't know what is
                stylesheet = "background-color: {}; border-style: {}; border-color: {}; border-width: 1px"
                colorBorder = "dashed none dashed dashed"
                complementBorder = "dashed dashed dashed none"

                self.colorLabel.setStyleSheet(stylesheet.format(color.name(), colorBorder, borderColor))
                self.complementLabel.setStyleSheet(stylesheet.format(
                    complementColor.name(), complementBorder, borderColor))
                # if the cursor is ontop of the label
                if  mouseX - self.desktopX >= width - 2* self.labelWidth and mouseY >= height - self.labelHeight:
                    # adjust the transparency of the label, so that we can see what we're sampling
                    transparency = "background-color:rgba({},{},{}, 75%)"
                    self.colorLabel.setStyleSheet(transparency.format(color.red(),
                        color.green(), color.blue()))
                    self.complementLabel.setStyleSheet(transparency.format(complementColor.red(),
                        complementColor.green(), complementColor.blue()))

                # label moving time
                # if cursor is in the bottom right corner
                if  mouseX - self.desktopX >= width - 61 and mouseY >= height - (offsetY + self.labelHeight):
                    self.colorLabel.move(width - 2 * self.labelWidth, height - self.labelHeight)
                    self.complementLabel.move(width - self.labelWidth, height - self.labelHeight)
                # right side limit
                elif mouseX - self.desktopX >= width - 61:
                    self.colorLabel.move(width - 2 * self.labelWidth, mouseY + offsetY)
                    self.complementLabel.move(width - self.labelWidth, mouseY + offsetY)
                # bottom limit
                elif mouseY >= height - (offsetY + self.labelHeight):
                    self.colorLabel.move(mouseX - self.desktopX + self.labelWidth, height - self.labelHeight)
                    self.complementLabel.move(mouseX - self.desktopX + 2 * self.labelWidth, height - self.labelHeight)
                else:
                    self.colorLabel.move(mouseX - self.desktopX + self.labelWidth, mouseY + offsetY)
                    self.complementLabel.move(mouseX - self.desktopX + 2 * self.labelWidth, mouseY + offsetY)
        elif event.type() == QtCore.QEvent.MouseButtonRelease:
            # if mid button, exit
            if event.button() == QtCore.Qt.MidButton:
                sys.exit()

            # get the color of the pixel the cursor is over
            c = self.image.pixel(event.globalX() - self.desktopX , event.globalY())
            color = QColor(c)
            hue = color.getHsl()[0]
            complementColor = QColor(c)
            if hue !=  - 1:
                complementColor.setHsl(hue + 180, color.getHsl()[1], color.getHsl()[2],color.getHsl()[3])

            # if right button, choose the complementary color
            if event.button() == QtCore.Qt.RightButton:
                color = complementColor

            # push the chosen color to the clipboard
            pyperclip.copy(color.name()[1:].upper())
            sys.exit()
        return QMainWindow.eventFilter(self, source, event)

app = QApplication(sys.argv)
sampler = Colorsampler()
app.installEventFilter(sampler)
sys.exit(app.exec_())
