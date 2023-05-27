import socket

import sys

def main():

    if len(sys.argv) <= 3:

        print("INVALID INPUT!")

        sys.exit()

    if sys.argv[1] == "default":

        h = '127.0.0.1'

    else:

        h = sys.argv[1]

    if sys.argv[2] == "default":

        p = 3500

    else:

        p = sys.argv[2]

    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    s.connect((h, int(p)))

    while True:

        if sys.argv[3] == "subscribe":

            if len(sys.argv[4:]) < 1:

                print("NO TOPIC DETECTED!")

                print("Please try again")

                sys.exit()

            msg = "subscribe"

            for m in sys.argv[4:]:

                msg += " " + m

            send(s, msg)

        elif sys.argv[3] == "publish":

            msg = "publish "

            if len(sys.argv[4:]) == 0:

                print("NO TOPIC OR MESSAGE DETECTED!")

                sys.exit()

            if len(sys.argv[4:]) == 1:

                print("NO MESSAGE DETECTED!")

                sys.exit()

            msg += sys.argv[4] + " "

            for m in sys.argv[5:]:

                msg += " " + m

            send(s, msg)

        elif sys.argv[3] == "ping":

            ping(s)

        else:

            print("INVALID INPUT!")

            sys.exit()

        try:

            server(s)

        except socket.error:

            print("TIMEOUT: No response from server")


def send(client, msg):

    message = msg.encode('ascii')

    msg_length = len(message)

    msg_length = str(msg_length).encode('ascii')

    msg_length += b' ' * (1024 - len(msg_length))

    client.send(msg_length)

    client.send(message)


def server(c: socket.socket):

    c.settimeout(10.0)

    while True:

        message_length = int(c.recv(1024).decode('ascii'))

        msg = c.recv(message_length)

        if not msg:

            continue

        msg = msg.decode('ascii')

        print(msg)

        message = msg

        c.settimeout(None)

        split_msg = message.split()

        if split_msg[0] == "subAck:":

            print("Subscribing on ")

            for m in split_msg[1:]:

                print(m)

        elif msg == "pubAck":

            print("Message published successfully")

            sys.exit()

        elif msg == "INVALID TOPIC!":

            print(msg)

            sys.exit()

        elif split_msg[0] == 'pong':

            sys.exit()

        elif split_msg[0] == 'ping':

            pong(c)


def ping(client: socket.socket):

    send(client, "ping")


def pong(client: socket.socket):

    send(client, "pong")


if __name__ == '__main__':

    main()
