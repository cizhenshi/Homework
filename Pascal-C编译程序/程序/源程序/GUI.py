import sys

from PyQt4 import *
from my_yacc_debug import*
from myhighter import MyHighlighter
from QT import *
class MyWidget(QtGui.QMainWindow):
    ui = Ui_MainWindow()
    def __init__(self, parent=None):
        super(MyWidget, self).__init__(parent)
        self.ui.setupUi(self)
        self.highlighter = MyHighlighter(self.ui.textEdit.document())
    @QtCore.pyqtSlot()
    def on_actionOpen_triggered(self):
        fg = QtGui.QFileDialog()
        dir = QtCore.QDir()
        filename = fg.getOpenFileName(fg,"Open File",dir.currentPath(),"Pascal Files (*.pas);;Text Files (*.txt)")
        if(filename==""):
            pass
        else:
            fp = open(filename)
            content = fp.read()
            self.ui.textEdit.setPlainText(content)
            self.setWindowTitle("Pascal--"+filename)
    @QtCore.pyqtSlot()
    def on_actionRun_triggered(self):
        self.ui.textBrowser.clear()
        inout_data = my_yacc(self.ui.textEdit.toPlainText(),self.ui.textBrowser)
    @QtCore.pyqtSlot()
    def on_actionNew_triggered(self):
        if(self.ui.textEdit.document().isModified()):
            message = QtGui.QMessageBox()
            message.information(message,"Error Message","The current file has been modified,Please save the current File")
        else:
            self.ui.textEdit.clear()
            self.ui.textBrowser.clear()
            self.setWindowTitle("Untitled")
    @QtCore.pyqtSlot()
    def on_actionSave_triggered(self):
        fg = QtGui.QFileDialog()
        dir = QtCore.QDir()
        filename = fg.getSaveFileName(fg,"Open File",dir.currentPath())
        if(filename==""):
            pass
        else:
            fp = open(filename,'w')
            content = self.ui.textEdit.toPlainText()
            self.ui.textEdit.document().setModified(False)
    @QtCore.pyqtSlot()
    def on_actionJump_to_line_triggered(self):
        input = self.ui.lineEdit.text()
        self.ui.lineEdit.clear()
        self.ui.lineEdit.clear()
        TextLine = self.ui.textEdit.document().lineCount()
        if (int(input)>TextLine):
            message = QtGui.QMessageBox()
            message.information(message,"Error Message","The linenumer too big!")
        else:
            linenumber = int(input)
            block = self.ui.textEdit.document().findBlockByLineNumber(linenumber-1)
            self.ui.textEdit.setTextCursor(QtGui.QTextCursor(block))

if __name__ == "__main__":
    app = QtGui.QApplication(sys.argv)
    mainwindow = MyWidget()
    mainwindow.show()
    app.exec_()

