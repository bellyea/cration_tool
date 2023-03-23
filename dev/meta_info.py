import sys
import json
from PyQt5.QtCore import Qt, QUrl
from PyQt5.QtWidgets import *

from dev.modify_meta import ModifyMetaWindow


class SaveFormat:
    SaveFormat = {
        "Json", "Binary"}

    # SaveFormat = Enum("Json", "Binary")


class MetaInfoWindow(QWidget):
    SaveFormat = {
        "Json", "Binary"}
    def __init__(self):
        super().__init__()
        print("Initializing MetaInfoWindow...")
        self.init_ui()

    def init_ui(self):
        label = QLabel("Meta 정보 설정")
        label.setAlignment(Qt.AlignVCenter)
        label.setAlignment(Qt.AlignCenter)

        btn_create = QPushButton(self)
        btn_create.setText('Create')
        btn_create.clicked.connect(self.create_function)

        btn_modify = QPushButton(self)
        btn_modify.setText('Modify')
        btn_modify.clicked.connect(self.modify_function)

        hbox = QHBoxLayout()
        hbox.addWidget(btn_create)
        hbox.addWidget(btn_modify)

        groupbox = QGroupBox()
        groupbox.setLayout(hbox)

        vbox = QVBoxLayout()
        vbox.addWidget(label)
        vbox.addWidget(groupbox)

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

    def create_function(self):
        file_data = {}
        file_path, _ = QFileDialog.getSaveFileName(self, "Save Json File", "", "Json Files (*.json)")
        if file_path != '':
            with open(file_path, 'w') as f:
                json.dump({}, f)
            file_data['file_path'] = file_path
            try:
                self.modify_meta_window = ModifyMetaWindow(file_data)
                self.modify_meta_window.show()
            except Exception as e:
                print(f"create_function Exception: {e}")
        else:
            return False

    def modify_function(self):
        try:
            file_data = {}
            file_path, _ = QFileDialog.getOpenFileName(self, "Open Json File", "", "Json Files (*.json)")
            if file_path != '':
                global url
                url = QUrl.fromLocalFile(file_path)
                with open(file_path, 'r') as f:
                    json_data = f.read()
                self.is_json(json_data)
                file_data['json_data'] = json.loads(json_data)
                file_data['file_path'] = file_path
                self.modify_meta_window = ModifyMetaWindow(file_data)
                self.modify_meta_window.show()
            else:
                return False
        except Exception as e:
            print(f"modify_function Exception: {e}")

    def is_json(self, json_data):
        try:
            json_object = json.loads(json_data)
            iterator = iter(json_object)
            return True
        except Exception as e:
            print(f"is_json Exception: {e}")
            QMessageBox.critical(self, 'Invalid JSON data', '올바른 JSON 파일이 아닙니다.')
            return False


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = MetaInfoWindow()
    sys.exit(app.exec_())