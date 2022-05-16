from PyQt5 import QtWidgets, QtCore, QtGui

class HeaderItem(QtWidgets.QWidget):
    def __init__(self, parent, text, backcall):
        super().__init__(parent)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.sizePolicy().hasHeightForWidth())
        self.setSizePolicy(sizePolicy)
        self.setMinimumSize(QtCore.QSize(0, 23))

        self.hitemLayout = QtWidgets.QHBoxLayout(self)
        self.hitemLayout.setContentsMargins(0, 0, 0, 0)

        self.headerLabel = QtWidgets.QLabel(self)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.headerLabel.sizePolicy().hasHeightForWidth())
        self.headerLabel.setSizePolicy(sizePolicy)
        self.hitemLayout.addWidget(self.headerLabel)
        self.headerLabel.setText(text)

        self.deleteButton = QtWidgets.QPushButton(self)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.deleteButton.sizePolicy().hasHeightForWidth())
        self.deleteButton.setSizePolicy(sizePolicy)
        self.deleteButton.setText('Delete')
        self.hitemLayout.addWidget(self.deleteButton)
        self.deleteButton.clicked.connect(self.delete)

        self.text = text
        self.backcall = backcall

    def delete(self):
        if self.backcall.active == self:
            self.backcall.active = None
        self.backcall.saved = False
        self.backcall.set_window_title()
        self.deleteLater()

    def mousePressEvent(self, a0: QtGui.QMouseEvent):
        self.backcall.open_note(self)

    def hide_delete(self):
        self.deleteButton.setHidden(True)

    def show_delete(self):
        self.deleteButton.setHidden(False)

    def set_active(self):
        myFont = QtGui.QFont()
        myFont.setBold(True)
        self.headerLabel.setFont(myFont)

    def set_inactive(self):
        myFont = QtGui.QFont()
        myFont.setBold(False)
        self.headerLabel.setFont(myFont)

