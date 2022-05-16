from PyQt5 import QtWidgets, QtGui


class NoteBody(QtWidgets.QTextEdit):
    def __init__(self, parent, backcall):
        super().__init__(parent)
        self.setReadOnly(True)
        self.backcall = backcall

    def focusOutEvent(self, e: QtGui.QFocusEvent) -> None:
        super().focusOutEvent(e)
        if self.textChanged:
            self.backcall.save_into_current_note(self.toHtml())