from hashlib import sha256
from json import loads

from PyQt5.QtWidgets import QMessageBox


def openLogin(ui):
    ui.registerWidget.setHidden(True)
    ui.loginWidget.setVisible(True)


def register(ui, BUFFER_SIZE):
    user = ui.register_ui.lineEdit.text()
    password1 = ui.register_ui.lineEdit_3.text()
    password2 = ui.register_ui.lineEdit_4.text()
    name = ui.register_ui.lineEdit_2.text()

    if len(user) * len(password1) * len(name) == 0:
        ui.register_ui.label.setText('Please input all fields')
    elif len(user) == 10:
        ui.register_ui.label.setText('Số Điện thoại không tồn tại')
    elif password2 != password1:
        ui.register_ui.label.setText('Password không trùng khớp')
        ui.register_ui.lineEdit_4.setText('')
        ui.register_ui.lineEdit_3.setText('')
    else:
        password = sha256((str(password2)).encode()).hexdigest()
        db = '{ ' + f'"username": "{user}", "password": "{password}", "name": "{name}", "type": "register"' + ' }'
        ui.tcp_client.send(bytes(db, 'utf8'))
        data = loads(ui.tcp_client.recv(BUFFER_SIZE).decode('utf8'))

        isReg = data['isReg']
        if isReg == 'True':
            ui.register_ui.label.setText('Số Điện Thoại đã tồn tại!!!')
            ui.register_ui.lineEdit.setText('')
            ui.register_ui.lineEdit_2.setText('')
            ui.register_ui.lineEdit_3.setText('')
            ui.register_ui.lineEdit_4.setText('')
        else:
            msg = QMessageBox()
            msg.setWindowTitle('Thông Báo')
            msg.setText('Đăng ký tài khoản thành công')
            msg.exec_()
            openLogin()
