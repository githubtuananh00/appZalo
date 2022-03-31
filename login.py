from hashlib import sha256
from json import loads

from PyQt5.QtCore import QThread, pyqtSignal


class ReceiveThread(QThread):
    signal = pyqtSignal(str)

    def __init__(self, client_socket):
        super(ReceiveThread, self).__init__()
        self.client_socket = client_socket

    def run(self):
        while True:
            self.receive_message()

    def receive_message(self):
        message = self.client_socket.recv(1024)
        message = message.decode()

        # print(message)
        self.signal.emit(message)


def showRegister(ui):
    ui.loginWidget.setHidden(True)
    ui.registerWidget.setVisible(True)


def btn_login_clicked(ui, BUFFER_SIZE):
    username = ui.login_ui.lineEdit_2.text()
    password = sha256(str(ui.login_ui.lineEdit.text()).encode()).hexdigest()

    if len(username) * len(password) == 0:
        ui.login_ui.label_6.setText('Place input all fields')
    else:
        db = '{ ' + f'"username": "{username}", "password": "{password}", "type": "login"' + ' }'
        ui.tcp_client.send(bytes(db, 'utf8'))
        data = loads(ui.tcp_client.recv(BUFFER_SIZE).decode('utf8'))

        isLogin = data['login']
        msg = data['msglogin']
        if msg == 'True':
            ui.login_ui.label_6.setText('Tài Khoản hiện đang đăng nhập. Vui lòng đăng xuất trước khi đăng nhập')
            ui.login_ui.lineEdit.setText('')
            ui.login_ui.lineEdit_2.setText('')
        elif isLogin == 'True':
            ui.login_ui.label_6.setText('')
            ui.loginWidget.setHidden(True)
            ui.homeWidget.setVisible(True)

            ui.recv_thread = ReceiveThread(ui.tcp_client)
            ui.recv_thread.signal.connect(ui.show_message)
            ui.recv_thread.start()

            db = '{ "type":"home"}'
            ui.tcp_client.send(db.encode())
            print("[INFO] recv thread started")
        else:
            ui.login_ui.label_6.setText('Invalid username or password')
            ui.login_ui.lineEdit.setText('')
            ui.login_ui.lineEdit_2.setText('')
