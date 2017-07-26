# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'QT.ui'
#
# Created by: PyQt4 UI code generator 4.11.4
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui

try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    def _fromUtf8(s):
        return s

try:
    _encoding = QtGui.QApplication.UnicodeUTF8
    def _translate(context, text, disambig):
        return QtGui.QApplication.translate(context, text, disambig, _encoding)
except AttributeError:
    def _translate(context, text, disambig):
        return QtGui.QApplication.translate(context, text, disambig)

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName(_fromUtf8("MainWindow"))
        MainWindow.resize(818, 553)
        self.centralwidget = QtGui.QWidget(MainWindow)
        self.centralwidget.setObjectName(_fromUtf8("centralwidget"))
        self.textEdit = QtGui.QTextEdit(self.centralwidget)
        self.textEdit.setGeometry(QtCore.QRect(0, 0, 821, 371))
        self.textEdit.setStyleSheet(_fromUtf8("font: 75 14pt \"Bell MT\";"))
        self.textEdit.setObjectName(_fromUtf8("textEdit"))
        self.textBrowser = QtGui.QTextBrowser(self.centralwidget)
        self.textBrowser.setGeometry(QtCore.QRect(0, 370, 821, 151))
        self.textBrowser.setStyleSheet(_fromUtf8("font: 75 12pt \"Adobe Gothic Std B\";"))
        self.textBrowser.setObjectName(_fromUtf8("textBrowser"))
        self.lineEdit = QtGui.QLineEdit(self.centralwidget)
        self.lineEdit.setGeometry(QtCore.QRect(710, 0, 113, 20))
        self.lineEdit.setObjectName(_fromUtf8("lineEdit"))
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtGui.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 818, 23))
        self.menubar.setObjectName(_fromUtf8("menubar"))
        self.menuCaidan = QtGui.QMenu(self.menubar)
        self.menuCaidan.setObjectName(_fromUtf8("menuCaidan"))
        self.menuRun = QtGui.QMenu(self.menubar)
        self.menuRun.setObjectName(_fromUtf8("menuRun"))
        self.menuJump = QtGui.QMenu(self.menubar)
        self.menuJump.setObjectName(_fromUtf8("menuJump"))
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtGui.QStatusBar(MainWindow)
        self.statusbar.setObjectName(_fromUtf8("statusbar"))
        MainWindow.setStatusBar(self.statusbar)
        self.actionOpen = QtGui.QAction(MainWindow)
        self.actionOpen.setObjectName(_fromUtf8("actionOpen"))
        self.actionNew = QtGui.QAction(MainWindow)
        self.actionNew.setObjectName(_fromUtf8("actionNew"))
        self.actionRun = QtGui.QAction(MainWindow)
        self.actionRun.setObjectName(_fromUtf8("actionRun"))
        self.actionSave = QtGui.QAction(MainWindow)
        self.actionSave.setObjectName(_fromUtf8("actionSave"))
        self.actionJump_to_line = QtGui.QAction(MainWindow)
        self.actionJump_to_line.setObjectName(_fromUtf8("actionJump_to_line"))
        self.menuCaidan.addAction(self.actionOpen)
        self.menuCaidan.addAction(self.actionNew)
        self.menuCaidan.addAction(self.actionSave)
        self.menuRun.addAction(self.actionRun)
        self.menuJump.addAction(self.actionJump_to_line)
        self.menubar.addAction(self.menuCaidan.menuAction())
        self.menubar.addAction(self.menuRun.menuAction())
        self.menubar.addAction(self.menuJump.menuAction())

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow", None))
        self.menuCaidan.setTitle(_translate("MainWindow", "File", None))
        self.menuRun.setTitle(_translate("MainWindow", "Run", None))
        self.menuJump.setTitle(_translate("MainWindow", "jump", None))
        self.actionOpen.setText(_translate("MainWindow", "Open", None))
        self.actionNew.setText(_translate("MainWindow", "New", None))
        self.actionRun.setText(_translate("MainWindow", "Compaile", None))
        self.actionSave.setText(_translate("MainWindow", "Save", None))
        self.actionJump_to_line.setText(_translate("MainWindow", "jump to line", None))

