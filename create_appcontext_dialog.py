from PyQt4.QtGui import QDialog, QPushButton, QGridLayout, QLabel, QFileDialog, QLineEdit
from textwrap import dedent

class CreateAppcontextDialog(QDialog):
    def __init__(self):
        QDialog.__init__(self)
        msg = dedent('''
            Select an app context to modify:
        ''')
        msglabel = QLabel(msg)
        self.layout = QGridLayout(self)
        self.layout.addWidget(msglabel, 0, 0, 1, 3)
        self.addFileBrowserWidgets()
        self.addBottomButtons()

    def showFileBrowser(self):
        openfile = QFileDialog.getOpenFileName(self)
        self.fileField.setText(openfile)
        f = open(openfile, 'r')
        data = f.read()

    def addFileBrowserWidgets(self):
        field = QLineEdit(self)
        self.fileField = field
        browse = QPushButton('Browse', self)
        browse.clicked.connect(self.showFileBrowser)
        self.layout.addWidget(field, 1, 1)
        self.layout.addWidget(browse, 1, 2)

    def addBottomButtons(self):
        ok = QPushButton('Ok', self)
        ok.clicked.connect(self.accept)
        ok.setDefault(True)
        cancel = QPushButton('Cancel')
        cancel.clicked.connect(self.reject)
        self.layout.addWidget(ok, 2, 1)
        self.layout.addWidget(cancel, 2, 2)
