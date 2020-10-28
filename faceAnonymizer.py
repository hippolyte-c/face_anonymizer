
import sys, os
import cv2
from PIL import Image, ImageFilter
from PIL.ImageQt import ImageQt
from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QVBoxLayout
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QPixmap
from PyQt5 import QtGui


CASC_PATH = "haarcascade_frontalface_default.xml"
W_SIZE = 500


class ImageLabel(QLabel):
    def __init__(self):
        super().__init__()

        self.setAlignment(Qt.AlignCenter)
        self.setText('\n\n Déposez une image \n\n')
        self.setStyleSheet('''
            QLabel{
                border: 4px dashed #aaa
            }
        ''')

    def setPixmap(self, image):
        super().setPixmap(image)

class AppDemo(QWidget):
    def __init__(self):
        super().__init__()
        self.resize(W_SIZE, W_SIZE)
        self.setAcceptDrops(True)

        mainLayout = QVBoxLayout()

        self.photoViewer = ImageLabel()
        mainLayout.addWidget(self.photoViewer)

        self.setLayout(mainLayout)

    def dragEnterEvent(self, event):
        if event.mimeData().hasImage:
            event.accept()
        else:
            event.ignore()

    def dragMoveEvent(self, event):
        if event.mimeData().hasImage:
            event.accept()
        else:
            event.ignore()

    def dropEvent(self, event):
        if event.mimeData().hasImage:
            event.setDropAction(Qt.CopyAction)
            imagePath = event.mimeData().urls()[0].toLocalFile()
            self.set_image(imagePath)

            event.accept()
        else:
            event.ignore()

    def set_image(self, imagePath):
        blurFaces(getFaces(imagePath), imagePath)
        pictureName = imagePath.split("/", imagePath.count("/"))[imagePath.count("/")]
        print(pictureName)
        pixmap = QPixmap("C:/Users/Hippolyte/OneDrive/python/faceAnonymizer/blurredFaces/" + pictureName.split(".")[0] + "Anonymized." + pictureName.split(".")[1])
        self.photoViewer.setPixmap(pixmap)


def getFaces(imagePath):
    faceCascade = cv2.CascadeClassifier(CASC_PATH)

    image = cv2.imread(imagePath)
    greyImage = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    faces = faceCascade.detectMultiScale(
        greyImage,
        scaleFactor=1.1,
        minNeighbors=5,
        minSize=(30, 30)
    )

    return faces


def blurFaces(faces, imagePath):
    image = Image.open(imagePath)

    for (x, y, w, h) in faces:
        croppedImage = image.crop((x, y, x+w, y+h))
        blurredImage = croppedImage.filter(ImageFilter.GaussianBlur(radius=50))
        #blurredImage = croppedImage.filter(ImageFilter.BoxBlur(radius=100))
        image.paste(blurredImage, (x, y, x+w, y+h))

    #croppedImage.show()
    #blurredImage.show()
    #image.show()

    data = list(image.getdata())

    imageVidee = Image.new(image.mode, image.size)
    imageVidee.putdata(data)


    x, y = image.size
    a = max(x, y)/(W_SIZE-100)
    imageVidee = imageVidee.resize((int(x/a), int(y/a)))
    #image.save(imagePath.split(".")[0] + "Anon." + imagePath.split(".")[1])
    pictureName = imagePath.split("/", imagePath.count("/"))[imagePath.count("/")]

    try:
        imageVidee.save("C:/Users/Hippolyte/OneDrive/python/faceAnonymizer/blurredFaces/" + pictureName.split(".")[0] + "Anonymized." + pictureName.split(".")[1])
    except:
        pass


if __name__ == '__main__':
    app = QApplication(sys.argv)
    demo = AppDemo()
    demo.show()
    sys.exit(app.exec_())
