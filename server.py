"""
Реализация серверной части чата.
Программа состоит из следующих компонентов:
    1) Связывание сервера с IP-адресом и номером порта
    2) Функции:
        2.1) sending_messages - отправка сообщения клиентом
        2.2) disconnect - отключение клиента от сети и, соответственно,
             удаление его из всех списков
        2.3) message_refactor - обработка входящего сообщения
        2.4) client_network - взаимодействие с клиентами: получение сообщений
        2.5) joining - присоединение очередного клиента
        2.6) start - начало работы чата
"""

import socket
import threading

host = socket.gethostbyname(socket.gethostname())
port = 7000

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind((host, port))
server.listen(10)

clients = []
names = []
addresses = []

""" Отображение сообщения у всех участников. """


def sending_messages(message):
    for client in clients:
        client.send(message)


""" Удаление элемента из списков, созданных в joining. """


def disconnect(conn, name):
    clients.remove(conn)
    conn.close()
    names.remove(name)


""" Обработка сообщения, приходящая от участника: удаление подписи автора. """


def message_refactor(message):
    flag = False

    if ':' not in message:
        flag = True

    for i in message:
        if i == ':':
            flag = True
        if not flag:
            message = message.replace(i, '', 1)
        message = message.replace(': ', '', 1)

    return message


"""
Сеть общения клиентов:
ожидание сообщения, после чего трансляция его на сервере и отправление всем участникам,
если же есть какая-то заминка, то отсоединение клиента и оповещение об этом.
"""


def client_network(conn):
    while True:
        number = clients.index(conn)
        try:
            message = conn.recv(1024)

            sending_messages(message)
            print(f"[{names[number]}][{addresses[number][1]}]: {message_refactor(message.decode('utf-8'))}")
        except:
            name = names[number]
            sending_messages(f"{name} left chatting".encode("utf-8"))
            disconnect(conn, name)
            break


""" 
Занесение данных присоединившегося участника в соответствующие списки.
Публикация приветственных и информационных сообщений.
"""


def joining(name, conn, addr):
    names.append(name)
    clients.append(conn)
    addresses.append(addr)

    print(f"Nickname is {name}")
    sending_messages(f"{name} joined!".encode("utf-8"))
    conn.send("Connected to server!".encode("utf-8"))


""" Подключение к серверу и получения имя пользователя, начало чата. """


def start():
    while True:
        conn, addr = server.accept()
        print(f"Connected with {addr}")

        conn.send('NICKNAME'.encode("utf-8"))
        name = conn.recv(1024).decode("utf-8")

        joining(name, conn, addr)

        thread = threading.Thread(target=client_network, args=(conn,))
        thread.start()


start()
