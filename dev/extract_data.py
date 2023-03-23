import sys

from PyQt5.QtGui import QFont
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *


class ExtractWindow(QWidget):

    def __init__(self):
        super().__init__()
        self.init_ui()

    def init_ui(self):
        label = QLabel('저장할 단위를 선택해 주세요.')
        label.setFont(QFont('Arial', 10))
        label.setAlignment(Qt.AlignVCenter)
        label.setAlignment(Qt.AlignCenter)

        btn_time = QPushButton(self)
        btn_time.setText('Time')
        btn_frame = QPushButton(self)
        btn_frame.setText('Frame')

        hbox = QHBoxLayout()
        hbox.addWidget(btn_time)
        hbox.addWidget(btn_frame)

        groupbox = QGroupBox()
        groupbox.setLayout(hbox)

        vbox = QVBoxLayout()
        vbox.addWidget(label)
        vbox.addWidget(groupbox)

        self.setLayout(vbox)
        self.setWindowTitle('데이터 추출')
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
    ex = ExtractWindow()
    sys.exit(app.exec_())