import socket

import threading

members = {}

def main():

    host = ('127.0.0.1', 3500)

    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    s.bind(host)

    print("Server is listening ...")

    s.listen()

    while True:

        c, address = s.accept()

        t = threading.Thread(target = clientHandle, args = (c, address))

        t.start()


def clientHandle(c, address):

    print("[NEW CONNECTION] connected from {}".format(address))

    Connected = True

    while Connected:

        try:

            length = int(c.recv(1024).decode('ascii'))

            message = c.recv(length)
    
            if not message:

                continue

            message = message.decode('ascii')

            print("[MESSAGE RECEIVED] {}".format(message))

            if message == "DISCONNECT":

                Connected = False

            else:

                split_message = message.split()

                if split_message[0] == "subscribe":

                    for msg in split_message[1:]:

                        if msg in members.keys():

                            if c not in members[msg]:

                                members[msg].append(c)

                        else:

                            members[msg] = [c]

                    msg = "subAck:"

                    for member in members.keys():

                        if c in members[member]:

                            msg += " " + member

                    send(c, msg)

                elif split_message[0] == "publish":

                    print(message)

                    message = split_message[2]

                    topic = split_message[1]

                    msg = topic + ":"

                    msg += split_message[2]

                    if topic not in members.keys():

                        send(c, "INVALID TOPIC!")

                    else:

                        send(c, "pubAck")

                        for client in members[topic]:

                            try:

                                send(client, msg)

                            except:

                                for tm in members:

                                    if c in members[tm]:
                            
                                        members[tm].remove(c)

                                c.close()

                                print(members)


                elif split_message[0] == "ping":

                    pong(c)

                elif split_message[0] == "pong":

                    ping(c)

        except:

            for tm in members:

                if c in members[tm]:

                    members[tm].remove(c)

            c.close()

            print(members)

            print('Disconnected suddenly by', address)

            break

    c.close()

def send(server, msg):

    message = msg.encode('ascii')

    msg_length = len(message)

    msg_length = str(msg_length).encode('ascii')

    msg_length += b' ' * (1024 - len(msg_length))

    server.send(msg_length)

    server.send(message)


def ping(c: socket.socket):

    send(c, "ping")


def pong(c: socket.socket):

    send(c, "pong")

if __name__ == "__main__":

    main()
