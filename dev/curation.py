import json
import os
import sys
import threading
from math import floor, trunc

import cv2
import numpy
from PyQt5 import QtWidgets, QtGui, QtCore
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *

class CurationWindow(QWidget):

    def __init__(self, parent=None):
        super().__init__(parent)
        self.lock = threading.Lock()
        self.json_file_path = ""
        self.mp4_file_path = ""
        self.running = False
        self.paused = False
        self.save_mode = False
        self.current_ms = 0
        self.duration_ms_text = ""
        self.current_ms_text = ""
        self.position = 0
        self.file_name_label = QLabel()
        self.frame_label = QLabel()
        self.time_label = QLabel()
        self.save_mode_label = QLabel()
        self.selected_texts = {}
        self.init_ui()

    def init_ui(self):
        try:
            # 틀 생성
            main_vbox = QVBoxLayout()
            video_hbox = QHBoxLayout()
            graph_hbox = QHBoxLayout()
            graph_info_vbox = QVBoxLayout()
            graph_hbox.addLayout(graph_info_vbox)
            graph_hbox.addWidget(QLabel('graph area'))

            video_hbox.addLayout(self.left_area())
            video_hbox.addLayout(self.right_area())

            main_vbox.addLayout(video_hbox)
            main_vbox.addLayout(graph_hbox)

            self.setLayout(main_vbox)
            self.resize(800, 500)
            self.center()
            self.show()
        except Exception as e:
            print(f"Error in init_ui: {e}")
            raise e

    def center(self):
        qr = self.frameGeometry()
        cp = QDesktopWidget().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())

    def left_area(self):
        # 비디오 출력 프레임 부분 생성
        self.video_label = QLabel()

        # 플레이버튼 생성
        self.btn_start = QPushButton()
        self.btn_start.setEnabled(False)
        self.btn_start.setIcon(self.style().standardIcon(QStyle.SP_MediaPlay))
        self.btn_start.clicked.connect(self.start)

        self.btn_pause = QPushButton()
        self.btn_pause.setEnabled(False)
        self.btn_pause.hide()
        self.btn_pause.setIcon(self.style().standardIcon(QStyle.SP_MediaPause))
        self.btn_pause.clicked.connect(self.pause)

        self.btn_forward = QPushButton('>')
        self.btn_forward.setEnabled(False)
        self.btn_forward.hide()
        self.btn_forward.clicked.connect(self.forward)

        self.btn_backward = QPushButton('<')
        self.btn_backward.setEnabled(False)
        self.btn_backward.hide()
        self.btn_backward.clicked.connect(self.backward)

        self.btn_forward_f = QPushButton('>>')
        self.btn_forward_f.setEnabled(False)
        self.btn_forward_f.hide()
        self.btn_forward_f.clicked.connect(self.forward_f)

        self.btn_backward_f = QPushButton('<<')
        self.btn_backward_f.setEnabled(False)
        self.btn_backward_f.hide()
        self.btn_backward_f.clicked.connect(self.backward_f)

        self.btn_layout = QHBoxLayout()
        self.btn_layout.addWidget(self.btn_backward_f)
        self.btn_layout.addWidget(self.btn_backward)
        self.btn_layout.addWidget(self.btn_start)
        self.btn_layout.addWidget(self.btn_pause)
        self.btn_layout.addWidget(self.btn_forward)
        self.btn_layout.addWidget(self.btn_forward_f)

        # 플레이용 수평 슬라이드 바 생성
        self.slider = QSlider(Qt.Horizontal)
        self.slider.setRange(0, 0)
        self.slider.sliderMoved.connect(self.set_position)

        # 비디오와 플레이 버튼, 슬라이드바를 레이아웃에 담기
        left_vbox = QVBoxLayout()
        left_vbox.addWidget(self.video_label)
        left_vbox.addLayout(self.btn_layout)
        left_vbox.addWidget(self.slider)
        left_vbox.setContentsMargins(0, 0, 0, 0)

        return left_vbox

    def right_area(self):
        groupbox1 = QGroupBox()
        groupbox2 = QGroupBox()

        # 기본 정보
        self.video_info = QVBoxLayout()
        self.video_info.addWidget(self.file_name_label)
        self.video_info.addWidget(self.frame_label)
        self.video_info.addWidget(self.time_label)
        self.video_info.addWidget(self.save_mode_label)
        self.video_info.setAlignment(Qt.AlignTop)
        groupbox1.setLayout(self.video_info)

        # 버튼
        button_vbox = QVBoxLayout()
        self.btn_save_mode = QPushButton(self)
        self.btn_save_mode.setText('SAVE MODE\nON')
        self.btn_save_mode.clicked.connect(self.toggle_save_mode)
        save_work = QPushButton(self)
        save_work.setText('작업 내역 저장')

        button_vbox.addWidget(self.btn_save_mode)
        button_vbox.addWidget(save_work)
        groupbox2.setLayout(button_vbox)

        # 기본 정보와 버튼 hbox에 담기
        top_hbox = QHBoxLayout()
        top_hbox.addWidget(groupbox1)
        top_hbox.addWidget(groupbox2)

        # 메타 정보
        type_vbox = QVBoxLayout()
        self.data_vbox = QVBoxLayout()

        self.type_list = QListWidget()
        self.type_list.setMinimumWidth(150)
        self.type_list.itemClicked.connect(self.chk_type_clicked)

        self.data_list = QScrollArea()
        self.data_list.setAlignment(Qt.AlignTop)
        self.data_list.setWidgetResizable(True)
        self.data_list.setMinimumWidth(200)

        # 라벨과 리스트 담기
        type_vbox.addWidget(QLabel('Meta type'))
        type_vbox.addWidget(self.type_list)
        self.data_vbox.addWidget(QLabel('Meta type'))
        self.data_vbox.addWidget(self.data_list)

        # 메타 정보 담기
        meta_info_hbox = QHBoxLayout()
        meta_info_hbox.addLayout(type_vbox)
        meta_info_hbox.addLayout(self.data_vbox)

        # 비디오 오른쪽 영역
        right_vbox = QVBoxLayout()
        right_vbox.addLayout(top_hbox)
        right_vbox.addLayout(meta_info_hbox)

        return right_vbox

    def toggle_save_mode(self):
        if not self.save_mode:
            self.save_mode = True
            self.btn_save_mode.setText('SAVE MODE\nOFF')
        else:
            self.save_mode = False
            self.btn_save_mode.setText('SAVE MODE\nON')
        self.update_info()

    def update_info(self):
        save_mode = 'ON' if self.save_mode else 'OFF'
        self.file_name_label.setText(f'파일명: {os.path.basename(self.mp4_file_path)}')
        self.frame_label.setText(f'프레임: {self.position} / {self.total_frame}')
        if self.convert_ms():
            self.time_label.setText(f'재생 시간: {self.current_ms_text} | {self.duration_ms_text}')
        self.save_mode_label.setText(f'저장 모드: {save_mode}')

    def convert_ms(self):
        try:
            if not self.current_ms == 0:
                if self.current_ms >= 1000:
                    current_seconds = self.current_ms // 1000
                else:
                    current_seconds = self.current_ms
                current_hours = current_seconds // 3600
                current_minutes = (current_seconds % 3600) // 60
                current_seconds = current_seconds % 60

                self.current_ms_text = f"{current_hours:02d}:{current_minutes:02d}:{current_seconds:02d}"
            else:
                self.current_ms_text = '00:00:00'

            if self.duration_ms >= 1000:
                duration_seconds = self.duration_ms // 1000
            else:
                duration_seconds = self.duration_ms
            duration_hours = duration_seconds // 3600
            duration_minutes = (duration_seconds % 3600) // 60
            duration_seconds = duration_seconds % 60

            self.duration_ms_text = f"{duration_hours:02d}:{duration_minutes:02d}:{duration_seconds:02d}"
            return True
        except:
            return False

    def set_position(self, position):
        print("set_position")
        if self.cap is not None:
            self.position = position
            self.cap.set(cv2.CAP_PROP_POS_FRAMES, self.position)
            ret, frame = self.cap.read()
            if ret:
                img = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                h, w, c = img.shape
                qImg = QtGui.QImage(img.data, w, h, w * c, QtGui.QImage.Format_RGB888)
                pixmap = QtGui.QPixmap.fromImage(qImg)
                p = pixmap.scaled(int(w * 480 / h), 480, QtCore.Qt.IgnoreAspectRatio)
                self.video_label.setPixmap(p)
                self.current_ms = int(self.cap.get(cv2.CAP_PROP_POS_MSEC))
                self.update_info()

    def run(self):
        # 재생 버튼 비활성화
        self.btn_start.setEnabled(False)
        self.btn_start.hide()


        # 일시 정지 버튼 활성화
        self.btn_pause.show()
        self.btn_pause.setEnabled(True)
        self.slider.setStyleSheet("QSlider::handle:horizontal {background-color: default;}")
        self.btn_forward.show()
        self.btn_backward.show()
        self.btn_forward_f.show()
        self.btn_backward_f.show()
        try:
            while self.cap.isOpened():
                # 슬라이드 비활성화
                self.slider.blockSignals(True)
                self.slider.setRange(0, self.total_frame)
                self.type_list.setSelectionMode(QAbstractItemView.NoSelection)
                # 라디오 비활성화
                if self.type_list.currentItem() and self.data_list.layout():
                    for i in range(self.data_list.layout().count()):
                        radio_button = self.data_list.layout().itemAt(i).widget()
                        radio_button.setEnabled(False)
                if not self.running:
                    break
                if not self.paused:
                    self.lock.acquire()
                    ret, frame = self.cap.read()
                    self.lock.release()
                    if not ret:
                        break
                    current_frame = int(self.cap.get(cv2.CAP_PROP_POS_FRAMES))
                    self.slider.setValue(current_frame)
                    self.position = current_frame
                    self.cap.set(cv2.CAP_PROP_POS_FRAMES, self.position)
                    img = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                    h, w, c = img.shape
                    qImg = QtGui.QImage(img.data, w, h, w * c, QtGui.QImage.Format_RGB888)
                    pixmap = QtGui.QPixmap.fromImage(qImg)
                    p = pixmap.scaled(int(w * 480 / h), 480, QtCore.Qt.IgnoreAspectRatio)
                    self.video_label.setPixmap(p)
                    self.current_ms = int(self.cap.get(cv2.CAP_PROP_POS_MSEC))// 2
                    self.update_info()

                    # frame 중간에 sleep 주기
                    if cv2.waitKey(self.sleep_ms) == ord('q'):
                        break
                while self.paused:
                    self.type_list.setSelectionMode(QAbstractItemView.SingleSelection)
                    if self.type_list.currentItem() and self.data_list.layout():
                        for i in range(self.data_list.layout().count()):
                            radio_button = self.data_list.layout().itemAt(i).widget()
                            radio_button.setEnabled(True)
                    self.slider.blockSignals(False)
                    if not self.running:
                        break
                    cv2.waitKey(100)
        except Exception as e:
            print(f"run Exception: {e}")
        self.cap.release()
        self.stop()
        cv2.destroyAllWindows()
        print("Thread end")

    def open_file(self):
        print('open video')
        try:
            file_path, _ = QFileDialog.getOpenFileName(self, "Open Video", "", "Video Files (*.mp4)")
            if file_path != '':
                self.mp4_file_path = file_path
                if self.open_json_file():
                    return True
            else:
                QMessageBox.critical(self, 'Missing video', '영상을 불러와 주세요.')
                return False
        except Exception as e:
            print(f"open_file Exception: {e}")
            QMessageBox.critical(self, 'Fail to load', '파일 불러오기에 실패했습니다.')
            return False

    def open_json_file(self):
        print('open json')
        file_path, _ = QFileDialog.getOpenFileName(self, "Open json", "", "json Files (*.json)")
        if file_path != '':
            with open(file_path, 'r') as f:
                json_data = f.read()
            if self.is_json(json_data):
                self.json_data = json.loads(json_data)
            self.btn_start.setEnabled(True)
            self.json_file_path = file_path
            self.cap = cv2.VideoCapture(self.mp4_file_path)
            frame_count = int(self.cap.get(cv2.CAP_PROP_FRAME_COUNT))
            fps = self.cap.get(cv2.CAP_PROP_FPS)
            self.sleep_ms = int(numpy.round((1 / fps) * 500))  # frame 중간 sleep계산
            self.total_frame = int(self.cap.get(cv2.CAP_PROP_FRAME_COUNT))
            self.duration_ms = int(trunc((frame_count / fps)))
            self.update_info()
            print(self.json_data)
            self.add_item_type_list()
            return True
        else:
            QMessageBox.critical(self, 'Missing JSON data', 'json 파일을 불러와 주세요.')
            return False
    def is_json(self, json_data):
        try:
            json_object = json.loads(json_data)
            iterator = iter(json_object)
            return True
        except Exception as e:
            print(f"is_json Exception: {e}")
            QMessageBox.critical(self, 'Invalid JSON data', '올바른 JSON 파일이 아닙니다.')
            return False
    def add_item_type_list(self):
        print('add_item_type_list')
        if self.json_data is not None:
            self.chk_dup(self.json_data)
            for meta_type in self.json_data:
                self.chk_dup(self.json_data[meta_type])
                self.type_list.addItem(meta_type)
                for meta_code in self.json_data[meta_type]:
                    try:
                        while True:
                            num = int(meta_code)
                            break
                    except ValueError:
                        QMessageBox.critical(self, 'Invalid Meta code', 'Meta code는 숫자만 입력 가능합니다.')

    def chk_type_clicked(self):
        print('chk_type_clicked')
        now_type = self.type_list.currentItem().text()
        try:
            radio_vbox = QVBoxLayout()
            radio_vbox.setAlignment(Qt.AlignTop)
            for meta_code, meta_data in self.json_data[now_type].items():
                if meta_code == '-1':
                    radio_button = QRadioButton('선택 안 함')
                else:
                    radio_button = QRadioButton(f'{meta_code}  {meta_data}')
                if self.selected_texts:
                    for chk_meta_type, chk_meta_code in self.selected_texts[self.position].items():
                        if chk_meta_type == now_type and chk_meta_code == meta_code:
                            radio_button.setChecked(True)
                radio_vbox.addWidget(radio_button)
                meta_info = {now_type: meta_code}
                radio_button.clicked.connect(lambda _, text=meta_info: self.update_selected_data(text))
            new_data_list = QScrollArea()
            new_data_list.setAlignment(Qt.AlignTop)
            new_data_list.setWidgetResizable(True)
            new_data_list.setMinimumWidth(200)
            new_data_list.setLayout(radio_vbox)
            self.data_vbox.removeWidget(self.data_list)
            self.data_list = new_data_list
            self.data_vbox.addWidget(self.data_list)
        except Exception as e:
            print(f"chk_type_clicked Exception: {e}")

    def update_selected_data(self, text):
        print('update_selected_texts')
        for key, value in text.items():
            self.selected_texts[self.position] = {key : value}
        print(f'self.selected_texts\n {self.selected_texts}')
        self.update_selected_type()

    def update_selected_type(self):
        now_meta_info = self.selected_texts[self.position]
        if now_meta_info:
            for i in range(self.type_list.count()):
                item = self.type_list.item(i)
                if item.text() in now_meta_info.keys():
                    item.setBackground(QtGui.QColor(211, 221, 255))
                    break

    def chk_dup(self, chk_data):
        seen_data = set()
        for data in chk_data:
            if data in seen_data:
                print(f"Duplicate data found: {data}")
                return False
            else:
                seen_data.add(data)

    def stop(self):
        self.running = False
        self.paused = False
        # 재생 버튼 활성화
        self.btn_start.setEnabled(True)
        # 일시 정지 버튼 비활성화
        self.btn_pause.setEnabled(False)
        print("stopped")

    def forward(self):
        if self.position <= self.total_frame:
            self.position += 1
        self.set_position(self.position)
        print("forward")

    def backward(self):
        if self.position > 0:
            self.position -= 1
        self.set_position(self.position)
        print("backward")

    def forward_f(self):
        if self.position <= self.total_frame - 5:
            self.position += 5
        self.set_position(self.position)
        print("forward_f")

    def backward_f(self):
        if self.position >= 5:
            self.position -= 5
        self.set_position(self.position)
        print("backward_f")

    def pause(self):
        if not self.paused:
            self.paused = True
            self.btn_pause.setIcon(self.style().standardIcon(QStyle.SP_MediaPlay))
            self.btn_forward.setEnabled(True)
            self.btn_backward.setEnabled(True)
            self.btn_forward_f.setEnabled(True)
            self.btn_backward_f.setEnabled(True)
        else:
            self.paused = False
            self.btn_pause.setIcon(self.style().standardIcon(QStyle.SP_MediaPause))
            self.btn_forward.setEnabled(False)
            self.btn_backward.setEnabled(False)
            self.btn_forward_f.setEnabled(False)
            self.btn_backward_f.setEnabled(False)
        print("pause")

    def start(self):
        self.running = True
        th = threading.Thread(target=self.run, daemon=True)
        th.start()
        print("started")

    def onExit(self):
        print("exit")
        self.stop()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = CurationWindow()
    sys.exit(app.exec_())