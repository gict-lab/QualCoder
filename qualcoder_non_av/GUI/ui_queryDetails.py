# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'ui_queryDetails.ui'
#
# Created: Wed Feb  3 08:16:37 2016
#      by: PyQt5 UI code generator 5.2.1
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_Dialog_QueryDetails(object):
    def setupUi(self, Dialog_QueryDetails):
        Dialog_QueryDetails.setObjectName("Dialog_QueryDetails")
        Dialog_QueryDetails.resize(353, 272)
        self.buttonBox = QtWidgets.QDialogButtonBox(Dialog_QueryDetails)
        self.buttonBox.setGeometry(QtCore.QRect(110, 220, 211, 32))
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(QtWidgets.QDialogButtonBox.Cancel|QtWidgets.QDialogButtonBox.Ok)
        self.buttonBox.setObjectName("buttonBox")
        self.lineEdit_QueryName = QtWidgets.QLineEdit(Dialog_QueryDetails)
        self.lineEdit_QueryName.setGeometry(QtCore.QRect(10, 30, 311, 27))
        self.lineEdit_QueryName.setObjectName("lineEdit_QueryName")
        self.label = QtWidgets.QLabel(Dialog_QueryDetails)
        self.label.setGeometry(QtCore.QRect(10, 10, 181, 17))
        self.label.setObjectName("label")
        self.textEdit_description = QtWidgets.QTextEdit(Dialog_QueryDetails)
        self.textEdit_description.setGeometry(QtCore.QRect(10, 100, 311, 101))
        self.textEdit_description.setObjectName("textEdit_description")
        self.label_QueryDescription = QtWidgets.QLabel(Dialog_QueryDetails)
        self.label_QueryDescription.setGeometry(QtCore.QRect(10, 70, 231, 17))
        self.label_QueryDescription.setObjectName("label_QueryDescription")

        self.retranslateUi(Dialog_QueryDetails)
        self.buttonBox.accepted.connect(Dialog_QueryDetails.accept)
        self.buttonBox.rejected.connect(Dialog_QueryDetails.reject)
        QtCore.QMetaObject.connectSlotsByName(Dialog_QueryDetails)

    def retranslateUi(self, Dialog_QueryDetails):
        _translate = QtCore.QCoreApplication.translate
        Dialog_QueryDetails.setWindowTitle(_translate("Dialog_QueryDetails", "Query Details"))
        self.label.setText(_translate("Dialog_QueryDetails", "Query Name"))
        self.label_QueryDescription.setText(_translate("Dialog_QueryDetails", "Query Description"))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    Dialog_QueryDetails = QtWidgets.QDialog()
    ui = Ui_Dialog_QueryDetails()
    ui.setupUi(Dialog_QueryDetails)
    Dialog_QueryDetails.show()
    sys.exit(app.exec_())
