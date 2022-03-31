from PyQt5.QtWidgets import QMessageBox


def send_message(ui):
    message = ui.home_ui.textEdit.toPlainText()
    if ui.isRoom:
        db = '{' + f'"type":"sendRoom","message":"{message}","id":"{ui.idRoom}"' + '}'
    else:
        db = '{' + f'"type":"send","message":"{message}"' + '}'

    ui.home_ui.textBrowser.append("Me: " + message)

    print("Me: " + message)

    try:
        ui.tcp_client.send(db.encode())
    except Exception as e:
        error = "Unable to send message '{}'".format(str(e))
        print("[INFO]", error)
        ui.show_error("Server Error", error)
    ui.home_ui.textEdit.clear()


def group(ui):
    db = '{ "type":"group" }'
    ui.tcp_client.send(db.encode())
    ui.home_ui.listWidget.clear()


def ok(ui):
    list_name = [ui.nickname]
    currents_index = ui.home_ui.listWidget.selectedIndexes()
    for index in currents_index:
        list_name.append(index.data())
    db = '{' + f'"type":"chat","user":"{list_name}","id":"{ui.nickname}"' + '}'
    ui.tcp_client.send(db.encode())
    ui.home_ui.textBrowser.clear()
    temp = ', '
    name = temp.join(list_name[1:])
    # ui.home_ui.label.setText(name)
    msg = QMessageBox()
    msg.setText(f'Bắt đầu nhắn tin với: {name}')
    msg.setWindowTitle('Thông báo')
    msg.exec_()


def search(ui):
    txt_search = ui.home_ui.lineEdit.text()
    for i in range(ui.home_ui.listWidget.count()):
        if ui.home_ui.listWidget.item(i).text() == txt_search:
            ui.home_ui.listWidget.clear()
            ui.home_ui.listWidget.addItem(txt_search)
            break
        else:
            msg = QMessageBox()
            msg.setWindowTitle('Thông Báo')
            msg.setText('Người dùng không tồn tại!!!')
            msg.exec_()
    ui.home_ui.lineEdit.setText('')
