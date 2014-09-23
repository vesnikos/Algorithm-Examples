# Found at http://stackoverflow.com/questions/5816383/model-view-qcompleter-in-a-qlineedit
# Check as WORKING

import sys
from PyQt4 import QtCore, QtGui

class LineEdit(QtGui.QLineEdit):
    def __init__(self, parent, completerContents):
        super(LineEdit, self).__init__(parent)

        self.completerList = QtCore.QStringList()
        for content in completerContents:
            self.completerList.append(QtCore.QString(content))
        self.completer = QtGui.QCompleter(self.completerList, self)
        self.completer.setCompletionMode(QtGui.QCompleter.PopupCompletion)
        self.completer.setCaseSensitivity(QtCore.Qt.CaseInsensitive)
        self.setCompleter(self.completer)

if __name__ == '__main__':
    class Example(QtGui.QMainWindow):
        def __init__(self):
            QtGui.QMainWindow.__init__(self)

            self.centralWidget = QtGui.QWidget(self)
            self.layout = QtGui.QVBoxLayout(self.centralWidget)

            # Example LineEdit Call
            self.lineEdit = LineEdit(parent=self.centralWidget, completerContents=('test', 'blah', 'heh', 'yep', 'hello', 'hi'))

            self.layout.addWidget(self.lineEdit)
            self.setCentralWidget(self.centralWidget)

    app = QtGui.QApplication(sys.argv)
    QtWin = Example()
    QtWin.show()
    sys.exit(app.exec_())