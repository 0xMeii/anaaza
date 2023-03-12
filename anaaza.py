import sys
import os
import shutil
import random 
import string 
import base64
import time
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QHBoxLayout, QLabel, QPushButton, QFileDialog, QProgressBar, QMessageBox
from PyQt5.QtGui import QIcon, QPixmap, QPalette, QColor, QBrush
from PyQt5.QtCore import Qt, QSize

def obfuscate(content):
    OFFSET = 10
    VARIABLE_NAME = ''.join(random.choices(string.ascii_letters, k=10))
    b64_content = base64.b64encode(content.encode()).decode()
    chunks = [b64_content[i:i+OFFSET] for i in range(0, len(b64_content), OFFSET)]
    str_chunks = [r"\x" + "".join([f"{ord(c):02x}" for c in chunk]) for chunk in chunks]
    str_chunks_code = "+".join([f'"{chunk}"' for chunk in str_chunks])
    code = f'{VARIABLE_NAME} = {str_chunks_code}\n'
    code += f'exec(__import__("base64").b64decode({VARIABLE_NAME}.encode("utf-8")).decode("utf-8"))'
    return code

class AnaazaObfuscator(QWidget):
    def __init__(self):
        super().__init__()

        self.title = "Anaaza Obfuscator"
        self.left = 100
        self.top = 100
        self.width = 350
        self.height = 150

        self.initUI()

    def initUI(self):
        palette = QPalette()
        palette.setColor(QPalette.Window, QColor(53, 53, 53))
        palette.setColor(QPalette.WindowText, Qt.white)
        self.setPalette(palette)

        self.setWindowTitle(self.title)
        self.setGeometry(self.left, self.top, self.width, self.height)

        oImage = QPixmap("img/background.jpg")
        palette = self.palette()
        palette.setBrush(QPalette.Window, QBrush(oImage))
        self.setPalette(palette)

        self.setWindowIcon(QIcon("img/icon.png"))

        vbox = QVBoxLayout()
        hbox = QHBoxLayout()
        vbox.setAlignment(Qt.AlignCenter)
        hbox.setAlignment(Qt.AlignCenter)
        vbox.addStretch(1)
        hbox.addStretch(1)
        vbox.addLayout(hbox)
        vbox.addStretch(1)
        self.setLayout(vbox)

        self.label = QLabel(self)
        self.label.setStyleSheet("color: white; border: 1px solid black; padding: 5px; background-color: black;")
        self.label.setAutoFillBackground(True)
        self.label.setText("Seleccione el archivo que desea obfuscar:")
        hbox.addWidget(self.label)

        self.btn_file_dialog = QPushButton(self)
        self.btn_file_dialog.setStyleSheet("color: white; border: 1px solid black; padding: 5px; background-color: black;")
        self.btn_file_dialog.setText("Seleccionar Archivo")
        self.btn_file_dialog.clicked.connect(self.show_file_dialog)
        hbox.addWidget(self.btn_file_dialog)

        hbox = QHBoxLayout()
        hbox.setAlignment(Qt.AlignCenter)

        self.progress_bar = QProgressBar(self)
        self.progress_bar.hide()
        vbox.addWidget(self.progress_bar)

        self.btn_obfuscate = QPushButton(self)
        self.btn_obfuscate.setStyleSheet("color: white; border: 1px solid black; padding: 5px; background-color: black;")
        self.btn_obfuscate.setText("Obfuscar Archivo")
        self.btn_obfuscate.clicked.connect(self.run_obfuscator)
        self.btn_obfuscate.hide()
        vbox.addWidget(self.btn_obfuscate)

        self.show()

    def show_file_dialog(self):
        file_dialog = QFileDialog()
        file_path, _ = file_dialog.getOpenFileName(self, 'Open file', '', 'Python Files (*.py)')
        if file_path:
            self.file_path = file_path
            self.btn_obfuscate.show()
            self.run_obfuscator(file_path)

    def run_obfuscator(self, path=None):
        try:
            file_path = self.file_path
            if not os.path.exists(path):
                QMessageBox.critical(self, 'Error', 'Archivo no encontrado')
                return

            if not os.path.isfile(path) or not path.endswith('.py'):
                QMessageBox.critical(self, 'Error', 'Archivo no valido')
                return

            with open(path, 'r', encoding='utf-8', errors='ignore') as file:
                file_content = file.read()

            obfuscated_content = obfuscate(file_content)

            obfuscated_file_name = f'{file_path.split(".")[0]}_obfuscated.py'
            with open(obfuscated_file_name, 'w') as file:
                file.write(obfuscated_content)

            QMessageBox.information(self, "Obfuscation Completed", "Archivo obfuscado exitosamente!")
        except:
            QMessageBox.critical(self, 'Error', 'Se ha producido un error')

def main():
    app = QApplication(sys.argv)
    obfuscator = AnaazaObfuscator()
    obfuscator.show()
    sys.exit(app.exec_())

if __name__ == '__main__':
    main()