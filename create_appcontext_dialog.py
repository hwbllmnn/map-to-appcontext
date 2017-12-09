from PyQt4.QtGui import QDialog, QPushButton, QGridLayout, QLabel
from textwrap import dedent

class CreateAppcontextDialog(QDialog):
    def __init__(self):
        QDialog.__init__(self)
        msg = dedent('''
            The image has been pushed to the io stack.
            Use io.pop() to retrieve the most recently
            pushed image.''')
        msglabel = QLabel(msg)
        self.layout = QGridLayout(self)
        self.layout.addWidget(msglabel, 0, 0, 1, 3)
        self.addButtons()

    def addButtons(self):
        ok = QPushButton('Ok', self)
        ok.clicked.connect(self.accept)
        ok.setDefault(True)
        cancel = QPushButton('Cancel')
        cancel.clicked.connect(self.reject)
        self.layout.addWidget(ok, 1, 1)
        self.layout.addWidget(cancel, 1, 2)
