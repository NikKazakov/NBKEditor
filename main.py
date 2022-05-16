import sys
from PyQt5 import QtWidgets, QtCore
import json

import layout_main
from header_item import HeaderItem
from note_body import NoteBody
from add_entry_line import AddEntryLine


class MyApp(QtWidgets.QMainWindow, layout_main.Ui_MainWindow):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.noteBody = NoteBody(self.centralwidget, self)
        self.centralLayout.addWidget(self.noteBody)

        self.addEntryLine = AddEntryLine(self.sidePanelContents, self)
        self.sidePanelLayout.addWidget(self.addEntryLine)
        self.addEntryLine.setHidden(True)

        self.actionNew.triggered.connect(self.file_new)
        self.actionOpen.triggered.connect(self.file_open)
        self.actionSave.triggered.connect(self.file_save)
        self.actionSave_as.triggered.connect(self.file_save_as)
        self.actionExit.triggered.connect(self.file_quit)

        self.actionEditor_Mode.triggered.connect(self.control_editor_mode)
        self.actionViewer_Mode.triggered.connect(self.control_viewer_mode)

        self.sidePanelLayout.setAlignment(QtCore.Qt.AlignTop)

        self.addEntryButton.setHidden(True)
        self.addEntryButton.clicked.connect(self.add_entry)

        self.addEntryLine.setHidden(True)
        self.addEntryLine.returnPressed.connect(self.add_entry_line_pressed)

        self.error = QtWidgets.QErrorMessage()
        self.notes = {}
        self.active = None
        self.viewer_mode = True
        self.current_file = 'Untitled'
        self.saved = False

        self.set_window_title()

    def add_entry(self):
        self.addEntryButton.setHidden(True)
        self.addEntryLine.clear()
        self.addEntryLine.setHidden(False)
        self.addEntryLine.setFocus()

    def add_entry_line_pressed(self):
        text = self.addEntryLine.text()
        if text:
            if text in self.notes:
                self.error.showMessage('Note with this name already exists!')
            else:
                self.noteBody.clear()
                self.notes[text] = ''

                self.addEntryLine.clear()
                self.addEntryLine.setHidden(True)

                if self.active is not None:
                    self.active.set_inactive()

                wgt = HeaderItem(self.sidePanelContents, text, self)
                wgt.set_active()
                self.active = wgt
                self.sidePanelLayout.insertWidget(len(self.sidePanelLayout)-2, wgt)

                self.noteBody.setFocus()

                self.addEntryLine.clear()
        self.addEntryLine.setHidden(True)
        self.addEntryButton.setHidden(False)

    def file_new(self):
        for i in layout_widgets(self.sidePanelLayout):
            if isinstance(i, HeaderItem):
                i.deleteLater()
        self.notes = {}
        self.active = None
        self.current_file = None
        self.noteBody.clear()

        self.current_file = 'Untitled'
        self.saved = False

        self.set_window_title()

    def file_open(self):
        dlg = QtWidgets.QFileDialog(self, 'Open File')
        dlg.setFileMode(QtWidgets.QFileDialog.ExistingFile)
        dlg.setNameFilter('Notebook files (*.nbk)')
        name = ''
        if dlg.exec():
            name = dlg.selectedFiles()
        if name:
            self.file_new()
            with open(name[0], 'r') as re:
                self.notes = json.loads(''.join(re.readlines()))
                if self.notes:
                    self.noEntriesYetItem.setHidden(True)
                for note in self.notes:
                    self.sidePanelLayout.insertWidget(len(self.sidePanelLayout) - 2,
                                                      HeaderItem(self.sidePanelContents, note, self))

            self.current_file = name[0]
            self.saved = True
            self.set_window_title()

    def file_save(self):
        if self.current_file == 'Untitled':
            self.file_save_as()
        else:
            with open(self.current_file, 'w') as wr:
                wr.write(json.dumps(self.notes))
            self.saved = True
            self.set_window_title()

    def file_save_as(self):
        suffix = '.nbk'
        default_name = 'Untitled'
        i = 1
        new_default_name = default_name
        while QtCore.QFile.exists(new_default_name + suffix):
            new_default_name = default_name + f' ({i})'
            i += 1
        name = QtWidgets.QFileDialog.getSaveFileName(self, 'Save as', new_default_name, 'Notebook files (*.nbk)')

        if name:
            with open(name[0], 'w') as wr:
                wr.write(json.dumps(self.notes))
            self.current_file = name[0]
            self.saved = True
            self.set_window_title()

    def file_quit(self):
        quit(0)

    def control_editor_mode(self):
        self.viewer_mode = False
        self.actionEditor_Mode.setVisible(False)
        self.actionViewer_Mode.setVisible(True)

        self.noteBody.setReadOnly(False)

        self.noEntriesYetItem.setHidden(True)
        self.addEntryButton.setHidden(False)

        for item in layout_widgets(self.sidePanelLayout):
            if isinstance(item, HeaderItem):
                item.show_delete()

    def control_viewer_mode(self):
        self.viewer_mode = True
        self.actionViewer_Mode.setVisible(False)
        self.actionEditor_Mode.setVisible(True)

        self.noteBody.setReadOnly(True)

        self.addEntryButton.setHidden(True)
        for item in layout_widgets(self.sidePanelLayout):
            if isinstance(item, HeaderItem):
                item.hide_delete()

    def open_note(self, wgt):
        if self.active is not None:
            self.active.set_inactive()
        wgt.set_active()
        self.active = wgt

        if self.viewer_mode:
            self.noteBody.setHtml(self.notes[wgt.text])
        else:
            self.noteBody.setText(self.notes[wgt.text])

    def save_into_current_note(self, text):
        if not self.viewer_mode:
            if self.active is not None:
                self.notes[self.active.text] = text
                self.saved = False
                self.set_window_title()

    def set_window_title(self):
        self.myWindowTitle = f'NBKEditor - {self.current_file}'
        if not self.saved:
            self.myWindowTitle += '*'
        self.setWindowTitle(self.myWindowTitle)


def layout_widgets(layout):
    return (layout.itemAt(i).widget() for i in range(layout.count()))


def main():
    app = QtWidgets.QApplication(sys.argv)
    window = MyApp()
    window.show()
    app.exec_()


if __name__ == '__main__':
    main()
