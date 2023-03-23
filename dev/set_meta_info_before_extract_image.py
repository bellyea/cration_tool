import sys

from PyQt5.QtGui import QFont
from PyQt5.QtMultimedia import QMediaPlayer
from PyQt5.QtMultimediaWidgets import QVideoWidget
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *


class SetMetaInfoBeforeExtractImageWindow(QWidget):

    def __init__(self):
        super().__init__()
        self.init_ui()

    def init_ui(self):
        main_layout = QWidget()

        # 틀 생성
        main_vbox = QVBoxLayout()
        list_hbox = QHBoxLayout()
        meta_info = QScrollArea()

        list_hbox.addWidget(QListWidget())
        list_hbox.addWidget(QListWidget())

        # Create a QWidget to hold the group boxes
        widget = QWidget()

        # Create a QVBoxLayout to hold the group boxes
        layout = QVBoxLayout()

        # Create a QGroupBox and add two labels to it
        meta_info_box = QGroupBox()

        type = QLabel("Label 1")
        data = QLabel("Label 2")
        meta_info_box_layout = QVBoxLayout()
        meta_info_box_layout.addWidget(type)
        meta_info_box_layout.addWidget(data)
        meta_info_box.setLayout(meta_info_box_layout)

        # Add the QGroupBox to the QVBoxLayout
        layout.addWidget(meta_info_box)

        # Create another QGroupBox and add two labels to it
        group_box2 = QGroupBox()
        label3 = QLabel("Label 3")
        label4 = QLabel("Label 4")
        group_box2_layout = QVBoxLayout()
        group_box2_layout.addWidget(label3)
        group_box2_layout.addWidget(label4)
        group_box2.setLayout(group_box2_layout)

        # Add the second QGroupBox to the QVBoxLayout
        layout.addWidget(group_box2)

        # Set the QVBoxLayout as the layout for the QWidget
        widget.setLayout(layout)

        # Set the QWidget as the widget for the QScrollArea
        meta_info.setWidget(widget)

        btn_save = QPushButton("save")
        btn_cancel = QPushButton("cancel")
        btn_save.clicked.connect(self.save_function)
        btn_cancel.clicked.connect(self.cancel_function)

        btn_hbox = QHBoxLayout()
        btn_hbox.addWidget(btn_save)
        btn_hbox.addWidget(btn_cancel)

        main_vbox.addLayout(list_hbox)
        main_vbox.addWidget(QLabel(""))
        main_vbox.addWidget(QLabel("Meta information of images to extract"))
        main_vbox.addWidget(meta_info)
        main_vbox.addLayout(btn_hbox)



        # main_vbox.addLayout(video_hbox)
        # main_vbox.addWidget(QLabel('graph area'))
        #
        # label = QLabel('Curation Tool')
        # label.setFont(QFont('Arial', 30))
        # label.setAlignment(Qt.AlignVCenter)
        # label.setAlignment(Qt.AlignCenter)
        #
        # info_area = self.right_area()
        # video_hbox.addWidget(QLabel('video'))
        # video_hbox.addLayout(info_area)
        #
        # main_layout.setLayout(main_vbox)

        self.setLayout(main_vbox)
        self.setWindowTitle('Centering')
        self.resize(553, 380)
        self.center()
        self.show()

    def center(self):
        qr = self.frameGeometry()
        cp = QDesktopWidget().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())

    def save_function(self):
        print("save")

    def cancel_function(self):
        print("cancel")


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = MyApp()
    sys.exit(app.exec_())