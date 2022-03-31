from json import loads
from socket import socket, AF_INET, SOCK_STREAM
from sys import exit, argv

from PyQt5.QtCore import QRect
from PyQt5.QtWidgets import QMainWindow, QWidget, QApplication, QMessageBox

import home_ui
import login_ui
import register_ui
from home import send_message, group, ok, search
from login import btn_login_clicked, showRegister
from register import openLogin, register


class Client(object):
    def __init__(self):
        self.messages = []
        self.isRoom = False
        self.nickname = ''
        self.idRoom = ''
        self.mainWindow = QMainWindow()

        # add widgets to the application window
        self.loginWidget = QWidget(self.mainWindow)
        self.homeWidget = QWidget(self.mainWindow)
        self.registerWidget = QWidget(self.mainWindow)

        self.homeWidget.setHidden(True)
        self.registerWidget.setHidden(True)

        # Chat UI
        self.home_ui = home_ui.Ui_Form()
        self.home_ui.setupUi(self.homeWidget)
        self.home_ui.pushButton.clicked.connect(lambda: send_message(self))
        self.home_ui.pushButton_4.clicked.connect(lambda: group(self))
        self.home_ui.pushButton_3.clicked.connect(lambda: ok(self))
        self.home_ui.pushButton_2.clicked.connect(lambda: search(self))

        # Login UI
        self.login_ui = login_ui.Ui_Form()
        self.login_ui.setupUi(self.loginWidget)
        self.login_ui.pushButton.clicked.connect(lambda: btn_login_clicked(self, BUFFER_SIZE))
        self.login_ui.pushButton_6.clicked.connect(self.mainWindow.close)
        self.login_ui.pushButton_5.clicked.connect(lambda: showRegister(self))

        # Register UI
        self.register_ui = register_ui.Ui_Form()
        self.register_ui.setupUi(self.registerWidget)
        self.register_ui.pushButton_5.clicked.connect(lambda: openLogin(self))
        self.register_ui.pushButton_3.clicked.connect(lambda: register(self, BUFFER_SIZE))

        self.mainWindow.setGeometry(QRect(350, 50, 1170, 735))
        self.mainWindow.show()

        self.tcp_client = socket(AF_INET, SOCK_STREAM)
        self.tcp_client.connect(ADDRESS)
        # self.home_ui.listWidget.itemWidget()

    def show_message(self, message):
        print(message)
        db = loads(message)
        type = db['type']
        if type == 'send':
            self.home_ui.textBrowser.append(db['message'])
        elif type == 'group':
            user = db['user']
            self.home_ui.listWidget.addItem(user)
        elif type == 'room':
            self.isRoom = True
            self.idRoom = db['id']
            room = list(db['room'][1:-1].split(', '))
            name = ''
            for user in room:
                if user[1:-1] != self.nickname:
                    name += user[1:-1] + ', '
                self.home_ui.label.setText(f'Username: {name[:-2]}')
        elif type == 'home':
            msg = db['name'].split("_")[0]
            welcome = f'Welcome {msg} to Server: {HOST}'
            # name = msg
            self.home_ui.label.setText(welcome)
            self.nickname = db['name']
            print(self.nickname)

    def show_error(self, error_type, message):
        errorDialog = QMessageBox()
        errorDialog.setText(message)
        errorDialog.setWindowTitle(error_type)
        errorDialog.setStandardButtons(QMessageBox.Ok)
        errorDialog.exec_()


if __name__ == "__main__":
    HOST = '127.0.0.1'
    PORT = 8686
    ADDRESS = (HOST, PORT)
    BUFFER_SIZE = 1024
    app = QApplication(argv)
    c = Client()
    exit(app.exec())
