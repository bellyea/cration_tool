import sys

from PyQt5.QtGui import QFont
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *

from dev.curation import CurationWindow
from dev.meta_info import MetaInfoWindow


class MainWindow(QWidget):

    def __init__(self):
        super().__init__()
        self.init_ui()
        sys.exit(app.exec_())

    def init_ui(self):
        label = QLabel('Curation Tool')
        label.setFont(QFont('Arial', 30))
        label.setAlignment(Qt.AlignVCenter)
        label.setAlignment(Qt.AlignCenter)

        btn_set_meta_info = QPushButton(self)
        btn_set_meta_info.setText('Set up meta info')
        btn_set_meta_info.clicked.connect(self.show_meta_info_window)
        btn_curation = QPushButton(self)
        btn_curation.setText('Curation')
        btn_curation.clicked.connect(self.show_curation_window)
        btn_bring = QPushButton(self)
        btn_bring.setText('Bring a previous work')

        hbox = QHBoxLayout()
        hbox.addWidget(btn_set_meta_info)
        hbox.addWidget(btn_curation)
        hbox.addWidget(btn_bring)

        groupbox = QGroupBox()
        groupbox.setLayout(hbox)

        vbox = QVBoxLayout()
        vbox.addWidget(label)
        vbox.addWidget(groupbox)

        self.setLayout(vbox)
        self.setWindowTitle('Curation Tool')
        self.resize(553, 380)
        self.center()
        self.show()

    def center(self):
        qr = self.frameGeometry()
        cp = QDesktopWidget().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())
        
    def show_meta_info_window(self):
        try:
            self.meta_info_window = MetaInfoWindow()
            self.meta_info_window.show()
            app = QApplication.instance()
            app.aboutToQuit.connect(self.curation_window.onExit)
        except Exception as e:
            print(f"show_meta_info_window Exception: {e}")

    def show_curation_window(self):
        try:
            self.curation_window = CurationWindow()
            self.curation_window.show()
            result = self.curation_window.open_file()
            if not result:
                self.curation_window.close()
        except Exception as e:
            print(f"show_curation_window Exception: {e}")

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = MainWindow()
    sys.exit(app.exec_())
