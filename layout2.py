# Form implementation generated from reading ui file 'layout2.ui'
#
# Created by: PyQt6 UI code generator 6.7.1
#
# WARNING: Any manual changes made to this file will be lost when pyuic6 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt6 import QtCore, QtGui, QtWidgets


class Ui_DuoPliko(object):
    def setupUi(self, DuoPliko):
        DuoPliko.setObjectName("DuoPliko")
        DuoPliko.resize(1085, 836)
        self.verticalLayoutWidget = QtWidgets.QWidget(parent=DuoPliko)
        self.verticalLayoutWidget.setGeometry(QtCore.QRect(0, 0, 1081, 821))
        self.verticalLayoutWidget.setObjectName("verticalLayoutWidget")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.verticalLayoutWidget)
        self.verticalLayout.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout.setObjectName("verticalLayout")
        self.horizontalLayout_4 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_4.setObjectName("horizontalLayout_4")
        self.label_2 = QtWidgets.QLabel(parent=self.verticalLayoutWidget)
        self.label_2.setObjectName("label_2")
        self.horizontalLayout_4.addWidget(self.label_2)
        self.label = QtWidgets.QLabel(parent=self.verticalLayoutWidget)
        self.label.setObjectName("label")
        self.horizontalLayout_4.addWidget(self.label)
        self.verticalLayout.addLayout(self.horizontalLayout_4)
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.textEdit1 = QtWidgets.QTextEdit(parent=self.verticalLayoutWidget)
        self.textEdit1.setObjectName("textEdit1")
        self.horizontalLayout.addWidget(self.textEdit1)
        self.textEdit2 = QtWidgets.QTextEdit(parent=self.verticalLayoutWidget)
        self.textEdit2.setObjectName("textEdit2")
        self.horizontalLayout.addWidget(self.textEdit2)
        self.verticalLayout.addLayout(self.horizontalLayout)
        self.progressBar = QtWidgets.QProgressBar(parent=self.verticalLayoutWidget)
        self.progressBar.setProperty("value", 24)
        self.progressBar.setObjectName("progressBar")
        self.verticalLayout.addWidget(self.progressBar)
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.checkBox_2 = QtWidgets.QCheckBox(parent=self.verticalLayoutWidget)
        self.checkBox_2.setObjectName("checkBox_2")
        self.horizontalLayout_2.addWidget(self.checkBox_2)
        self.checkBox = QtWidgets.QCheckBox(parent=self.verticalLayoutWidget)
        self.checkBox.setObjectName("checkBox")
        self.horizontalLayout_2.addWidget(self.checkBox)
        self.verticalLayout.addLayout(self.horizontalLayout_2)
        self.horizontalLayout_3 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_3.setObjectName("horizontalLayout_3")
        self.return_2 = QtWidgets.QPushButton(parent=self.verticalLayoutWidget)
        self.return_2.setObjectName("return_2")
        self.horizontalLayout_3.addWidget(self.return_2)
        self.save = QtWidgets.QPushButton(parent=self.verticalLayoutWidget)
        self.save.setObjectName("save")
        self.horizontalLayout_3.addWidget(self.save)
        self.verticalLayout.addLayout(self.horizontalLayout_3)

        self.retranslateUi(DuoPliko)
        QtCore.QMetaObject.connectSlotsByName(DuoPliko)

    def retranslateUi(self, DuoPliko):
        _translate = QtCore.QCoreApplication.translate
        DuoPliko.setWindowTitle(_translate("DuoPliko", "Dialog"))
        self.label_2.setText(_translate("DuoPliko", "Plik 1"))
        self.label.setText(_translate("DuoPliko", "Plik 2"))
        self.checkBox_2.setText(_translate("DuoPliko", "Wielkość liter"))
        self.checkBox.setText(_translate("DuoPliko", "Znaki polskie"))
        self.return_2.setText(_translate("DuoPliko", "Wroc"))
        self.save.setText(_translate("DuoPliko", "Zapisz"))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    DuoPliko = QtWidgets.QDialog()
    ui = Ui_DuoPliko()
    ui.setupUi(DuoPliko)
    DuoPliko.show()
    sys.exit(app.exec())