from PyQt5 import QtWidgets, QtCore, QtGui


class AddEntryLine(QtWidgets.QLineEdit):
    def __init__(self, parent, backcall):
        super().__init__(parent)
        self.setMinimumSize(QtCore.QSize(0, 20))
        self.setHidden(True)
        self.backcall = backcall

    def focusOutEvent(self, a0: QtGui.QFocusEvent) -> None:
        super().focusOutEvent(a0)
        self.backcall.add_entry_line_pressed()