import json
import sys

from PyQt5.QtGui import QFont
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *


class ModifyMetaWindow(QWidget):
    def __init__(self, file_data, parent=None):
        super().__init__(parent)
        print("Initializing ModifyMetaWindow...")
        self.line_add_type = QLineEdit()
        self.line_add_code = QLineEdit()
        self.line_add_data = QLineEdit()
        self.type_list = QListWidget()
        self.code_list = QListWidget()
        self.data_list = QListWidget()
        self.url = file_data['file_path']
        if 'json_data' in file_data and file_data['json_data']:
            self.json_data = file_data['json_data']
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
                        QMessageBox.critical(self, '숫자가 아닌 Meta code', 'Meta code는 숫자만 입력 가능합니다.')
        else:
            self.json_data = {}
        self.init_ui()

    def init_ui(self):

        # 틀 생성
        main_vbox = QVBoxLayout()
        meta_info_hbox = QHBoxLayout()
        btn_hbox = QHBoxLayout()

        label = QLabel('Meta 정보 수정')
        label.setFont(QFont('Arial', 10))
        label.setAlignment(Qt.AlignCenter)

        type_vbox = QVBoxLayout()
        code_data_hbox = QHBoxLayout()
        code_data_vbox = QVBoxLayout()

        type_label = QLabel('Meta type')
        type_label.setFont(QFont('Arial', 10))
        type_label.setAlignment(Qt.AlignCenter)
        type_add_hbox = QHBoxLayout()
        btn_add_type = QPushButton('add')
        btn_remove_type = QPushButton('remove')
        type_add_hbox.addWidget(self.line_add_type)
        type_add_hbox.addWidget(btn_add_type)
        type_vbox.addWidget(type_label)
        type_vbox.addWidget(self.type_list)
        type_vbox.addLayout(type_add_hbox)
        type_vbox.addWidget(btn_remove_type)
        type_vbox.setContentsMargins(0,0,0,0)

        type_vbox_widget = QWidget()
        type_vbox_widget.setLayout(type_vbox)
        type_vbox_widget.setMinimumWidth(200)
        meta_info_hbox.addWidget(type_vbox_widget)

        code_vbox = QVBoxLayout()
        data_vbox = QVBoxLayout()

        code_label = QLabel('Meta code')
        code_label.setFont(QFont('Arial', 10))
        code_label.setAlignment(Qt.AlignCenter)
        code_vbox.addWidget(code_label)
        code_vbox.addWidget(self.code_list)
        code_vbox.addWidget(self.line_add_code)

        data_label = QLabel('Meta data')
        data_label.setFont(QFont('Arial', 10))
        data_label.setAlignment(Qt.AlignCenter)
        data_add_hbox = QHBoxLayout()
        btn_add_data = QPushButton('add')
        self.line_add_data.setMinimumWidth(200)
        data_add_hbox.addWidget(self.line_add_data)
        data_add_hbox.addWidget(btn_add_data)
        data_vbox.addWidget(data_label)
        data_vbox.addWidget(self.data_list)
        data_vbox.addLayout(data_add_hbox)
        data_vbox.setContentsMargins(0,0,0,0)

        btn_remove_data = QPushButton('remove')

        code_data_hbox.addLayout(code_vbox)
        code_data_hbox.addLayout(data_vbox)

        code_data_vbox.addLayout(code_data_hbox)
        code_data_vbox.addWidget(btn_remove_data)
        meta_info_hbox.addLayout(code_data_vbox)

        btn_save = QPushButton(self)
        btn_save.setText('save')
        btn_cancel = QPushButton(self)
        btn_cancel.setText('cancel')
        btn_hbox.addWidget(btn_save)
        btn_hbox.addWidget(btn_cancel)

        main_vbox.addWidget(label)
        main_vbox.addLayout(meta_info_hbox)
        main_vbox.addLayout(btn_hbox)

        btn_save.clicked.connect(self.save_function)
        btn_cancel.clicked.connect(self.close)
        self.type_list.itemClicked.connect(self.chk_type_clicked)
        self.code_list.itemClicked.connect(self.chk_code_clicked)
        self.data_list.itemClicked.connect(self.chk_data_clicked)

        btn_add_type.clicked.connect(self.add_type)
        btn_remove_type.clicked.connect(self.remove_type)
        btn_add_data.clicked.connect(self.add_data)
        btn_remove_data.clicked.connect(self.remove_data)

        self.setLayout(main_vbox)
        self.setWindowTitle('Curation Tool')
        self.resize(553, 380)
        self.center()
        self.show()

    def center(self):
        qr = self.frameGeometry()
        cp = QDesktopWidget().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())

    def chk_dup(self, json_data):
        seen_data = set()
        for data in json_data:
            if data in seen_data:
                print(f"Duplicate data found: {data}")
                return False
            else:
                seen_data.add(data)

    def chk_type_clicked(self):
        print('chk_type_clicked')
        now_type = self.type_list.currentItem().text()
        print(self.type_list.currentItem().text())
        self.code_list.clear()
        self.data_list.clear()
        try:
            for meta_code, meta_data in self.json_data[now_type].items():
                if meta_code == '-1':
                    continue
                self.add_code_data(meta_code, meta_data)
        except Exception as e:
            print(f"chk_type_clicked Exception: {e}")

    def add_code_data(self, meta_code, meta_data):
        try:
            while True:
                num = int(meta_code)
                break
            code_item = QListWidgetItem(meta_code)
            code_item.setData(Qt.UserRole, meta_data)
            self.code_list.addItem(code_item)
            data_item = QListWidgetItem(meta_data)
            data_item.setData(Qt.UserRole, meta_code)
            self.data_list.addItem(data_item)
        except ValueError:
            QMessageBox.critical(self, '숫자가 아닌 Meta code', 'Meta code는 숫자만 입력 가능합니다.')
        except Exception as e:
            print(f"add_code_data Exception: {e}")

    def chk_code_clicked(self):
        try:
            now_code = self.code_list.currentItem().text()
            now_data = self.code_list.currentItem().data(Qt.UserRole)
            print(f"Meta code: {now_code}, Meta data: {now_data}")
            for i in range(self.data_list.count()):
                item = self.data_list.item(i)
                if item.text() == now_data:
                    self.data_list.setCurrentItem(item)
            # print(now_code)
        except Exception as e:
            print(f"chk_code_clicked Exception: {e}")

    def chk_data_clicked(self):
        try:
            now_data = self.data_list.currentItem().text()
            now_code = self.data_list.currentItem().data(Qt.UserRole)
            print(f"Meta code: {now_code}, Meta data: {now_data}")
            for i in range(self.code_list.count()):
                item = self.code_list.item(i)
                if item.text() == now_code:
                    self.code_list.setCurrentItem(item)
        except Exception as e:
            print(f"chk_data_clicked Exception: {e}")

    def add_type(self):
        try:
            add_type_text = self.line_add_type.text()
            if add_type_text:
                if add_type_text in self.json_data:
                    QMessageBox.warning(self, '중복된 Meta type', '이미 존재하는 Meta type입니다.')
                    return
                self.json_data[add_type_text] = {'-1': '--'}
                self.type_list.addItem(add_type_text)
            else:
                QMessageBox.critical(self, '빈 Meta type', 'Meta type을 입력해 주세요.')
        except Exception as e:
            print(f"add_type Exception: {e}")

    def remove_type(self):
        try:
            now_type = self.type_list.currentItem().text()
            self.remove_type_row = self.type_list.currentRow()
            del self.json_data[now_type]
            self.type_list.takeItem(self.remove_type_row)
            self.code_list.clear()
            self.data_list.clear()
        except Exception as e:
            print(f"remove_type Exception: {e}")

    def add_data(self):
        try:
            if self.type_list.currentItem():
                now_type = self.type_list.currentItem().text()
                add_data_text = self.line_add_data.text()
                add_code_text = self.line_add_code.text()
                if add_code_text in self.json_data[now_type]:
                    QMessageBox.warning(self, '중복된 Meta code', '이미 존재하는 Meta code입니다.')
                    return
                if add_data_text and add_code_text:
                    self.json_data[now_type][add_code_text] = add_data_text
                    self.add_code_data(add_code_text, add_data_text)
                elif not add_code_text:
                    QMessageBox.critical(self, '빈 Meta type', 'Meta code를 입력해 주세요.')
                elif not add_data_text:
                    QMessageBox.critical(self, '빈 Meta type', 'Meta data를 입력해 주세요.')
            else:
                QMessageBox.critical(self, 'Meta type 미선택', 'Meta type을 선택해 주세요.')
        except Exception as e:
            print(f"add_data Exception: {e}")

    def remove_data(self):
        try:
            if self.type_list.currentItem():
                now_type = self.type_list.currentItem().text()
                now_code = self.code_list.currentItem().text()
                del self.json_data[now_type][now_code]
                self.remove_data_row = self.data_list.currentRow()
                self.data_list.takeItem(self.remove_data_row)
                self.code_list.takeItem(self.remove_data_row)
            else:
                QMessageBox.critical(self, 'Meta type 미선택', 'Meta type을 선택해 주세요.')
        except Exception as e:
            print(f"add_data Exception: {e}")



    def save_function(self):
        print("save")
        # Save the meta data to a file
        with open(self.url, 'w') as f:
            json.dump(self.json_data, f, indent=4)

    def cancel_function(self):
        print("cancel")
        self.close()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = ModifyMetaWindow()
    sys.exit(app.exec_())
