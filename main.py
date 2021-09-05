import os
from os import listdir
from os.path import isfile, join
import sys
from PyQt5.QtWidgets import QApplication, QWidget, QLineEdit, QVBoxLayout, QPushButton, QLabel
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QPixmap
import shutil
import pandas as pd
import xlrd


class FileContainer(QLabel):
    def __init__(self):
        super().__init__()

        self.setAlignment(Qt.AlignCenter)
        self.setText('\n\n Drop File Here \n\n')
        self.setStyleSheet('''
            QLabel{
                border: 4px dashed #aaa
            }
        ''')

    def setPixmap(self, image):
        super().setPixmap(image)

    def setTextInBox(self, string):
        super().setText(string)


class StringSearcherApp(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)

        self.setWindowTitle("Manuela Finder")
        self.resize(500, 500)
        self.setAcceptDrops(True)

        self.text_edit = QLineEdit()
        self.file_container = FileContainer()
        self.submit_btn = QPushButton("Search")

        layout = QVBoxLayout()
        layout.addWidget(self.text_edit)
        layout.addWidget(self.file_container)
        layout.addWidget(self.submit_btn)
        self.setLayout(layout)

        self.submit_btn.clicked.connect(self.btn_submit_pressed)

    def dragEnterEvent(self, event):
        if event.mimeData().hasImage:
            event.accept()
        else:
            event.ignore()

    def dragMoveEvent(self, event):
        if event.mimeData().hasImage:
            event.accept()
        else:
            event.ignore()

    def dropEvent(self, event):
        if event.mimeData().hasUrls():
            files = [(u.toLocalFile()) for u in event.mimeData().urls()]
            for f in files:
                # read the file extension
                extension = get_file_extension(f)

                # copy the file in fileToHandle folder if it has a supported extension
                if self.is_compatible(extension):
                    output_string = f'file at location \n{f} \nloaded'
                    self.set_text(output_string)

                    # clean directory and copy the target file
                    target = 'fileToHandle'
                    for t in os.listdir(target):
                        os.remove(os.path.join(target, t))
                    shutil.copyfile(f, f'fileToHandle/target.{extension}')

                else:
                    self.set_text("The file you tried to drop is not supported")

            event.accept()
        else:
            self.set_text("The file you tried to drop is not supported")
            event.ignore()

    def is_compatible(self, extension):
        compatible = ['csv', 'xls', 'xlsx', 'xlsm', 'xlsb', 'odf', 'ods', 'odt']
        if extension in compatible:
            return True
        return False

    def set_image(self, file_path):
        self.file_container.setPixmap(QPixmap(file_path))

    def set_text(self, string):
        self.file_container.setTextInBox(string)

    def btn_submit_pressed(self):
        string_to_search = self.text_edit.text()
        self.handle_file(string_to_search)

    def handle_file(self, string):
        path = 'fileToHandle'
        files = [f for f in listdir(path) if isfile(join(path, f))]
        file = files[0]

        if get_file_extension(file) == 'csv':
            dataframe = pd.read_csv(path + '/' + file)
        else:
            dataframe = pd.read_excel(path + '/' + file)
        dataframe = dataframe.applymap(lambda s: s.upper() if type(s) == str else s)
        string = string.upper()
        row = dataframe[dataframe.isin([string]).any(axis=1)]
        output = row.to_csv(header=None, index=False).strip('\n').split('\n')
        output = list_to_string(output)
        if output == '\n':
            self.set_text('String NOT found')
        else:
            self.set_text(output)


def list_to_string(list_of_strings):
    output = ''
    for elem in list_of_strings:
        output += elem + '\n'
    return output


def get_file_extension(file):
    split = file.split('.')
    output = split[1]
    return output


if __name__ == '__main__':
    app = QApplication(sys.argv)
    win = StringSearcherApp()
    win.show()
    sys.exit(app.exec_())
