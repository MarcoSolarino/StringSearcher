import sys
from PyQt5.QtWidgets import QApplication, QWidget, QLineEdit, QVBoxLayout, QPushButton, QLabel
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QPixmap


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


class TextEditDemo(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)

        self.setWindowTitle("Manuela Finder")
        self.resize(400, 400)
        self.setAcceptDrops(True)

        self.text_edit = QLineEdit()
        self.file_container = FileContainer()
        self.submit_btn = QPushButton("Submit")

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
        # if event.mimeData().hasImage:
        #     event.setDropAction(Qt.CopyAction)
        #     file_path = event.mimeData().urls()[0].toLocalFile()
        #     self.set_image(file_path)
        if event.mimeData().hasUrls():
            files = [(u.toLocalFile()) for u in event.mimeData().urls()]
            for f in files:
                if 'csv' in f or 'xls' in f:
                    print('Drag', f)
                    self.set_text(f)

            event.accept()
        else:
            event.ignore()

    def set_image(self, file_path):
        self.file_container.setPixmap(QPixmap(file_path))

    def set_text(self, string):
        self.file_container.setTextInBox(string)

    def btn_submit_pressed(self):
        self.text_edit.setText("Nessuna manueloide trovata")


if __name__ == '__main__':
    app = QApplication(sys.argv)
    win = TextEditDemo()
    win.show()
    sys.exit(app.exec_())
