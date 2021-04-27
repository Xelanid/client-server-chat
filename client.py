"""
Реализация клиентской части чата.
Программа состоит из следующих компонентов:
    1) Подключение к серверу по IP-адресу и номеру порта
    2) Функции:
        2.1) receive - получение сообщения
        2.2) write - отправка сообщения
"""

import socket
import threading

name = input("Your name: ")

host = socket.gethostbyname(socket.gethostname())
port = 7000
client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect((host, port))

""" 
    Получение сообщения:
    Если получено 'NICKNAME', то было введено имя пользователя.
    Иначе публикуется сообщение. 
    Если сообщение не получено, то клиент отключается.
"""


def receive():
    while True:
        try:
            message = client.recv(1024).decode("utf-8")
            if message == 'NICKNAME':
                client.send(name.encode("utf-8"))
            else:
                print(f"{message}")
        except:
            print("An error occured!")
            client.close()
            break


""" Отправка сообщения. """


def write():
    while True:
        message = f"{name}: {input()}"
        client.send(message.encode("utf-8"))


""" 
     Запуск.
     Включение многопоточности для функций получения и отправки сообщений.
"""


def start():
    receive_thread = threading.Thread(target=receive)
    receive_thread.start()

    write_thread = threading.Thread(target=write)
    write_thread.start()


start()
