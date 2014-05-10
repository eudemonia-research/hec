# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'hec.ui'
#
# Created: Sun May 11 03:57:06 2014
#      by: PyQt5 UI code generator 5.2.1
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(400, 300)
        MainWindow.setStyleSheet("QPushButton::pressed {\n"
"    background-color: #0f0;\n"
"    color: black;\n"
"}\n"
"QWidget {\n"
"    background-color: black;\n"
"    color: #0f0;\n"
"}\n"
"QPlainTextEdit, QLineEdit, QPushButton {\n"
"    border: 1px solid green;\n"
"    padding: 0.2em;\n"
"    border-radius: 3px;\n"
"}\n"
"QStatusBar {\n"
"    color: #999;\n"
"}")
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.centralwidget)
        self.verticalLayout.setObjectName("verticalLayout")
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.status = QtWidgets.QLabel(self.centralwidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.MinimumExpanding, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.status.sizePolicy().hasHeightForWidth())
        self.status.setSizePolicy(sizePolicy)
        self.status.setAlignment(QtCore.Qt.AlignCenter)
        self.status.setObjectName("status")
        self.horizontalLayout.addWidget(self.status)
        self.quit = QtWidgets.QPushButton(self.centralwidget)
        self.quit.setObjectName("quit")
        self.horizontalLayout.addWidget(self.quit)
        self.verticalLayout.addLayout(self.horizontalLayout)
        self.message = QtWidgets.QPlainTextEdit(self.centralwidget)
        self.message.setObjectName("message")
        self.verticalLayout.addWidget(self.message)
        self.gridLayout = QtWidgets.QGridLayout()
        self.gridLayout.setObjectName("gridLayout")
        self.decrypt = QtWidgets.QPushButton(self.centralwidget)
        self.decrypt.setObjectName("decrypt")
        self.gridLayout.addWidget(self.decrypt, 1, 1, 1, 1)
        self.address = QtWidgets.QLineEdit(self.centralwidget)
        self.address.setObjectName("address")
        self.gridLayout.addWidget(self.address, 0, 0, 1, 1)
        self.secret_exponent = QtWidgets.QLineEdit(self.centralwidget)
        self.secret_exponent.setObjectName("secret_exponent")
        self.gridLayout.addWidget(self.secret_exponent, 1, 0, 1, 1)
        self.encrypt = QtWidgets.QPushButton(self.centralwidget)
        self.encrypt.setObjectName("encrypt")
        self.gridLayout.addWidget(self.encrypt, 0, 1, 1, 1)
        self.verticalLayout.addLayout(self.gridLayout)
        MainWindow.setCentralWidget(self.centralwidget)
        self.statusBar = QtWidgets.QStatusBar(MainWindow)
        self.statusBar.setObjectName("statusBar")
        MainWindow.setStatusBar(self.statusBar)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "HEC"))
        self.status.setText(_translate("MainWindow", "HELLO ENCRYPT THINGS"))
        self.quit.setText(_translate("MainWindow", "Quit"))
        self.message.setPlainText(_translate("MainWindow", "Enter message to be encrypted/decrypted."))
        self.decrypt.setText(_translate("MainWindow", "Decrypt"))
        self.address.setPlaceholderText(_translate("MainWindow", "Address"))
        self.secret_exponent.setPlaceholderText(_translate("MainWindow", "Secret exponent (blank searches wallet.dat)"))
        self.encrypt.setText(_translate("MainWindow", "Encrypt"))

