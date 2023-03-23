import sys

from PyQt5.QtWidgets import *


class AfterCurationWindow(QWidget):

    def __init__(self):
        super().__init__()
        self.init_ui()

    def init_ui(self):

        btn_extract_image = QPushButton(self)
        btn_extract_image.setText('extract_image')
        btn_extract_data = QPushButton(self)
        btn_extract_data.setText('extract_data')

        btn_back_to_home = QPushButton(self)
        btn_back_to_home.setText('back_to_home')

        hbox = QHBoxLayout()
        hbox.addWidget(btn_extract_image)
        hbox.addWidget(btn_extract_data)

        vbox = QVBoxLayout()
        vbox.addLayout(hbox)
        vbox.addWidget(btn_back_to_home)

        self.setLayout(vbox)
        self.setWindowTitle('Curation Tool')
        self.resize(353, 280)
        self.center()
        self.show()

    def center(self):
        qr = self.frameGeometry()
        cp = QDesktopWidget().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = AfterCurationWindow()
    sys.exit(app.exec_())