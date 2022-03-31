from socket import socket, AF_INET, SOCK_STREAM, SOL_SOCKET, SO_REUSEADDR
from threading import Thread
from json import loads
from time import sleep
import sqlite3 as sql


class Server(object):
    def __init__(self, hostname, port):
        self.clients = {}

        # create server socket
        self.tcp_server = socket(AF_INET, SOCK_STREAM)
        self.tcp_server.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)

        # start server
        self.tcp_server.bind((hostname, port))
        self.tcp_server.listen(10)

        print("[INFO] Server running on {}:{}".format(hostname, port))
        while True:
            connection, address = self.tcp_server.accept()
            while True:
                db = loads(connection.recv(BUFFER_SIZE))
                type = db['type']
                if type == 'login':
                    isLogin = self.login(db, connection)
                    if isLogin:
                        break
                elif type == 'register':
                    self.register(db, connection)

            nickname = ''
            for user in self.clients:
                if self.clients[user] == connection:
                    nickname = user
                    break

            # start a thread for the client
            Thread(target=self.receive_message, args=(connection, nickname), daemon=True).start()
            print("[INFO] Connection from {}:{} AKA {}".format(address[0], address[1], nickname))

    def receive_message(self, connection, nickname):
        print("[INFO] Waiting for messages")
        while True:
            try:
                msg = connection.recv(BUFFER_SIZE)
                db = loads(msg)
                type = db['type']

                if type == 'send':
                    message = db['message']
                    db = '{' + f'"type":"send", "message": "{nickname + ": " + message}"' + '}'
                    self.send_message(db, nickname)
                    print(nickname + ": " + message)
                elif type == 'group':
                    for user in self.clients:
                        if user != nickname:
                            db = '{' + f'"type":"group", "user":"{user}"' + '}'
                            self.send_me(db, connection)
                            sleep(0.01)
                elif type == 'chat':
                    user_list = list(db['user'][1:-1].split(', '))
                    idRoom = db['id']
                    room[idRoom] = []
                    for user in user_list:
                        room[idRoom].append(user[1:-1])
                    db = '{' + f'"type": "room","id":"{idRoom}","room":"{room[idRoom]}"' + '}'
                    print(room[idRoom])
                    self.send_room(db, nickname, idRoom)
                    self.send_me(db, connection)
                elif type == 'sendRoom':
                    message = db['message']
                    id_Room = db['id']
                    db = '{' + f'"type":"send", "message": "{nickname + ": " + message}"' + '}'
                    self.send_room(db, nickname, id_Room)
                    print(nickname + ": " + message)
                elif type == 'home':
                    db = '{' + f'"type": "home", "name":"{nickname}"' + '}'
                    self.send_me(db, connection)

            except:
                connection.close()
                # remove user from users list
                del (self.clients[nickname])
                break

        print(nickname, " disconnected")

    def login(self, obj, client):
        user = obj['username']
        password = obj['password']

        conn = sql.connect('zalo.db')
        c = conn.cursor()
        c.execute('SELECT username, password FROM Login WHERE username = (?)', [user])
        user_pass = c.fetchone()
        c.execute('SELECT name FROM Login WHERE username = (?)', [user])
        username = c.fetchone()[0]
        conn.commit()
        conn.close()

        isLogin = False
        msgLogin = False
        if user in self.clients:
            msgLogin = True
        elif (user, password) == user_pass:
            isLogin = True
            self.clients[f'{username}'] = client

        db = '{ ' + f'"login": "{isLogin}", "msglogin": "{msgLogin}"' + ' }'
        client.send(db.encode())
        return isLogin

    def register(self, obj, client):
        user = obj['username']
        password = obj['password']
        name = obj['name']

        conn = sql.connect('zalo.db')
        c = conn.cursor()
        c.execute(f'SELECT username FROM Login WHERE username = (?)', [user])

        list_user = c.fetchone()
        conn.commit()
        conn.close()

        isReg = False
        if list_user:
            isReg = True
        else:
            conn = sql.connect('zalo.db')
            c = conn.cursor()
            c.execute(f'INSERT INTO Login VALUES (?,?,?)', (user, password, name))
            conn.commit()
            conn.close()

        db = '{' + f'"isReg": "{isReg}"' + '}'
        client.send(db.encode())

    def send_message(self, message, sender):
        if len(self.clients) > 0:
            for nickname in self.clients:
                if nickname != sender:
                    self.clients[nickname].send(bytes(message, 'utf8'))

    def send_room(self, message, sender, idRoom):
        if len(room) > 0:
            for name in room[idRoom]:
                if name != sender:
                    self.clients[name].send(bytes(message, 'utf8'))

    def send_me(self, data, client):
        client.send(data.encode())


if __name__ == "__main__":
    PORT = 8686
    HOST = "127.0.0.1"
    BUFFER_SIZE = 1024
    room = {}
    chat_server = Server(HOST, PORT)
