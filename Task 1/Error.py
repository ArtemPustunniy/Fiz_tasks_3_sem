# # -*- coding: utf-8 -*-
#
# from PyQt5 import QtCore, QtGui, QtWidgets
#
#
# class Ui_Dialog(object):
#     def setupUi(self, Dialog):
#         Dialog.setObjectName("Dialog")
#         Dialog.resize(400, 300)
#         Dialog.setMinimumSize(QtCore.QSize(400, 300))
#         Dialog.setMaximumSize(QtCore.QSize(400, 400))
#         self.Error = QtWidgets.QTextBrowser(Dialog)
#         self.Error.setGeometry(QtCore.QRect(50, 30, 291, 101))
#         self.Error.setObjectName("Error")
#         self.pushButton = QtWidgets.QPushButton(Dialog)
#         self.pushButton.setGeometry(QtCore.QRect(120, 190, 131, 31))
#         self.pushButton.setObjectName("pushButton")
#
#         self.retranslateUi(Dialog)
#         QtCore.QMetaObject.connectSlotsByName(Dialog)
#
#     def retranslateUi(self, Dialog):
#         _translate = QtCore.QCoreApplication.translate
#         Dialog.setWindowTitle(_translate("Dialog", "Dialog"))
#         self.Error.setHtml(_translate("Dialog", "<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
# "<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"
# "p, li { white-space: pre-wrap; }\n"
# "</style></head><body style=\" font-family:\'MS Shell Dlg 2\'; font-size:7.8pt; font-weight:400; font-style:normal;\">\n"
# "<p align=\"center\" style=\"-qt-paragraph-type:empty; margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><br /></p></body></html>"))
#         self.pushButton.setText(_translate("Dialog", "Ok"))
#
#
# class CustomDialog(QtWidgets.QDialog, Ui_Dialog):
#     def __init__(self):
#         super().__init__()
#         self.setupUi(self)
#
#     def resizeEvent(self, event):
#         self.updateBackgroundImage()
#         super().resizeEvent(event)
#
#     def updateBackgroundImage(self):
#         # Получаем размеры окна
#         size = self.size()
#         # Создаем QPixmap с изменением размера под размер окна
#         pixmap = QtGui.QPixmap("error_photo.jpg").scaled(size, QtCore.Qt.KeepAspectRatioByExpanding, QtCore.Qt.SmoothTransformation)
#         # Устанавливаем изображение как фон через стиль
#         palette = self.palette()
#         palette.setBrush(QtGui.QPalette.Background, QtGui.QBrush(pixmap))
#         self.setPalette(palette)
#
#
# if __name__ == "__main__":
#     import sys
#     app = QtWidgets.QApplication(sys.argv)
#     Form = CustomDialog()
#     Form.show()
#     sys.exit(app.exec_())

# -*- coding: utf-8 -*-

from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_Dialog(object):
    def setupUi(self, Dialog):
        Dialog.setObjectName("Dialog")
        Dialog.setFixedSize(400, 300)  # Фиксированный размер окна

        # Создаем QLabel для отображения изображения на фоне
        self.background = QtWidgets.QLabel(Dialog)
        self.background.setGeometry(0, 0, 400, 300)  # Задаем размер на всю форму
        self.background.setPixmap(

            QtGui.QPixmap("error_photo.jpg").scaled(400, 300, QtCore.Qt.KeepAspectRatioByExpanding,
                                                    QtCore.Qt.SmoothTransformation))
        self.background.setObjectName("background")
        self.overlay = QtWidgets.QLabel(Dialog)
        self.overlay.setGeometry(0, 0, 400, 300)
        self.overlay.setStyleSheet("background-color: rgba(230, 230, 230, 230); ")  # Черный полупрозрачный слой
        self.overlay.setObjectName("overlay")

        # Окно с текстом
        # self.Error = QtWidgets.QTextBrowser(Dialog)
        # self.Error.setGeometry(QtCore.QRect(50, 30, 291, 101))
        # self.Error.setObjectName("Error")
        # self.Error.hide()

        self.Error = QtWidgets.QLabel(Dialog)
        self.Error.setGeometry(QtCore.QRect(100, 30, 281, 41))
        font = QtGui.QFont()
        font.setPointSize(12)
        font.setBold(True)
        font.setWeight(75)
        self.Error.setFont(font)
        self.Error.setObjectName("Error")

        # Кнопка
        self.pushButton = QtWidgets.QPushButton(Dialog)
        self.pushButton.setGeometry(QtCore.QRect(135, 190, 131, 31))
        self.pushButton.setObjectName("pushButton")

        self.retranslateUi(Dialog)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

    def retranslateUi(self, Dialog):
        _translate = QtCore.QCoreApplication.translate
        Dialog.setWindowTitle(_translate("Dialog", "Dialog"))
#         self.Error.setHtml(_translate("Dialog", "<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
# "<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"
# "p, li { white-space: pre-wrap; }\n"
# "</style></head><body style=\" font-family:\'MS Shell Dlg 2\'; font-size:7.8pt; font-weight:400; font-style:normal;\">\n"
# "<p align=\"center\" style=\"-qt-paragraph-type:empty; margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><br /></p></body></html>"))
        self.pushButton.setText(_translate("Dialog", "Ok"))
        # self.Top_label.setText(_translate("Dialog", "Получившийся результат"))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    Form = QtWidgets.QDialog()
    ui = Ui_Dialog()
    ui.setupUi(Form)
    Form.show()
    sys.exit(app.exec_())
