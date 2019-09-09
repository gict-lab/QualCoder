# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'ui_dialog_codes.ui'
#
# Created by: PyQt5 UI code generator 5.5.1
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_Dialog_codes(object):
    def setupUi(self, Dialog_codes):
        Dialog_codes.setObjectName("Dialog_codes")
        Dialog_codes.resize(1243, 798)
        self.gridLayout = QtWidgets.QGridLayout(Dialog_codes)
        self.gridLayout.setObjectName("gridLayout")
        self.groupBox = QtWidgets.QGroupBox(Dialog_codes)
        self.groupBox.setMinimumSize(QtCore.QSize(0, 100))
        self.groupBox.setMaximumSize(QtCore.QSize(16777215, 100))
        self.groupBox.setTitle("")
        self.groupBox.setObjectName("groupBox")
        self.pushButton_view_file = QtWidgets.QPushButton(self.groupBox)
        self.pushButton_view_file.setGeometry(QtCore.QRect(10, 0, 151, 32))
        self.pushButton_view_file.setObjectName("pushButton_view_file")
        self.pushButton_auto_code = QtWidgets.QPushButton(self.groupBox)
        self.pushButton_auto_code.setGeometry(QtCore.QRect(170, 0, 181, 32))
        self.pushButton_auto_code.setObjectName("pushButton_auto_code")
        self.label_coder = QtWidgets.QLabel(self.groupBox)
        self.label_coder.setGeometry(QtCore.QRect(360, 6, 301, 28))
        self.label_coder.setObjectName("label_coder")
        self.label_file = QtWidgets.QLabel(self.groupBox)
        self.label_file.setGeometry(QtCore.QRect(660, 7, 551, 28))
        self.label_file.setObjectName("label_file")
        self.label_coded = QtWidgets.QLabel(self.groupBox)
        self.label_coded.setGeometry(QtCore.QRect(520, 70, 561, 28))
        self.label_coded.setObjectName("label_coded")
        self.label_code = QtWidgets.QLabel(self.groupBox)
        self.label_code.setGeometry(QtCore.QRect(0, 70, 501, 28))
        self.label_code.setObjectName("label_code")
        self.checkBox_show_coders = QtWidgets.QCheckBox(self.groupBox)
        self.checkBox_show_coders.setGeometry(QtCore.QRect(10, 40, 251, 22))
        self.checkBox_show_coders.setObjectName("checkBox_show_coders")
        self.label = QtWidgets.QLabel(self.groupBox)
        self.label.setGeometry(QtCore.QRect(270, 40, 201, 26))
        self.label.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.label.setObjectName("label")
        self.lineEdit_search = QtWidgets.QLineEdit(self.groupBox)
        self.lineEdit_search.setGeometry(QtCore.QRect(480, 37, 281, 32))
        self.lineEdit_search.setObjectName("lineEdit_search")
        self.label_search_frequency = QtWidgets.QLabel(self.groupBox)
        self.label_search_frequency.setGeometry(QtCore.QRect(800, 40, 151, 26))
        self.label_search_frequency.setText("")
        self.label_search_frequency.setObjectName("label_search_frequency")
        self.label_search_frequency_2 = QtWidgets.QLabel(self.groupBox)
        self.label_search_frequency_2.setGeometry(QtCore.QRect(790, 40, 151, 26))
        self.label_search_frequency_2.setText("")
        self.label_search_frequency_2.setObjectName("label_search_frequency_2")
        self.pushButton_search_results = QtWidgets.QPushButton(self.groupBox)
        self.pushButton_search_results.setGeometry(QtCore.QRect(775, 37, 161, 32))
        self.pushButton_search_results.setObjectName("pushButton_search_results")
        self.gridLayout.addWidget(self.groupBox, 0, 0, 1, 1)
        self.splitter = QtWidgets.QSplitter(Dialog_codes)
        self.splitter.setOrientation(QtCore.Qt.Horizontal)
        self.splitter.setObjectName("splitter")
        self.leftsplitter = QtWidgets.QSplitter(self.splitter)
        self.leftsplitter.setOrientation(QtCore.Qt.Vertical)
        self.treeWidget = QtWidgets.QTreeWidget(self.leftsplitter)
        self.listWidgetLinks = QtWidgets.QListWidget(self.leftsplitter)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.treeWidget.sizePolicy().hasHeightForWidth())
        self.treeWidget.setSizePolicy(sizePolicy)
        self.treeWidget.setMinimumSize(QtCore.QSize(200, 0))
        self.treeWidget.setBaseSize(QtCore.QSize(200, 0))
        self.treeWidget.setObjectName("treeWidget")
        self.treeWidget.headerItem().setText(0, "1")
        self.textEdit = QtWidgets.QTextEdit(self.splitter)
        self.textEdit.setObjectName("textEdit")
        self.gridLayout.addWidget(self.splitter, 1, 0, 1, 1)

        self.retranslateUi(Dialog_codes)
        QtCore.QMetaObject.connectSlotsByName(Dialog_codes)

    def retranslateUi(self, Dialog_codes):
        _translate = QtCore.QCoreApplication.translate
        Dialog_codes.setWindowTitle(_translate("Dialog_codes", "Codes"))
        self.pushButton_view_file.setToolTip(_translate("Dialog_codes", "Select a file to view"))
        self.pushButton_view_file.setText(_translate("Dialog_codes", "View File"))
        self.pushButton_auto_code.setText(_translate("Dialog_codes", "Auto code"))
        self.label_coder.setText(_translate("Dialog_codes", "Coder:"))
        self.label_file.setText(_translate("Dialog_codes", "File:"))
        self.label_coded.setText(_translate("Dialog_codes", "Right click below to mark and unmark selected text"))
        self.label_code.setText(_translate("Dialog_codes", "Right click below to create new codes and categories"))
        self.checkBox_show_coders.setToolTip(_translate("Dialog_codes", "Mark this to show all coded text by all other coders."))
        self.checkBox_show_coders.setText(_translate("Dialog_codes", "Show other coders"))
        self.label.setText(_translate("Dialog_codes", "Search for text:"))
        self.lineEdit_search.setToolTip(_translate("Dialog_codes", "Case sensitive search"))
        self.pushButton_search_results.setText(_translate("Dialog_codes", "0 of 0"))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    Dialog_codes = QtWidgets.QDialog()
    ui = Ui_Dialog_codes()
    ui.setupUi(Dialog_codes)
    Dialog_codes.show()
    sys.exit(app.exec_())

