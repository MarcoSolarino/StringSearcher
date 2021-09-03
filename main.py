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
                extension = ''
                if 'csv' in f:
                    extension = 'csv'
                elif 'xls' in f:
                    extension = 'xls'
                elif 'xlsx' in f:
                    extension = 'xlsx'

                # copy the file in fileToHandle folder if it has a supported extension
                if 'csv' in f or 'xls' in f or 'xlsx' in f:
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

    def set_image(self, file_path):
        self.file_container.setPixmap(QPixmap(file_path))

    def set_text(self, string):
        self.file_container.setTextInBox(string)

    def btn_submit_pressed(self):
        self.handle_file()
        self.text_edit.setText("Nessuna manueloide trovata")

    def handle_file(self):
        path = 'fileToHandle'
        files = [f for f in listdir(path) if isfile(join(path, f))]
        file = files[0]
        dataframe = pd.read_excel(path + '/' + file)
        print('file letto')


if __name__ == '__main__':
    app = QApplication(sys.argv)
    win = StringSearcherApp()
    win.show()
    sys.exit(app.exec_())
