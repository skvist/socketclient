#!/usr/bin/python3

'''
Socket Client for the Data and telecommunication course at Blekinge Institute of Technology.

Author: Niclas Söderkvist
Student acronym: niso16
Email: niclas.soderkvist@gmail.com

Usage: socket_client.py command [OPTIONS]

Commands:
get                          Lab 1, HTTP GET from tic tac toe server
post                         HTTP-post method to one of my own API's
send server port message     Send a message to a specific server and port

Examples:
python3 socket_client.py get  # Lab 1 tic tac toe
python3 socket_client.py send localhost 1337 Hello there!
'''

from socket import socket, AF_INET, SOCK_STREAM, gaierror
from sys import argv

class SocketClient:
    ''' Socket client class '''

    def __init__(self):
        ''' Create a new socket '''
        try:
            self.socket = socket(AF_INET, SOCK_STREAM) # TCP
        except Exception as ex:
            print(ex)

    def connect(self, server, port):
        ''' Connect to the specified server and port '''
        try:
            self.server = server
            # self.port = port
            self.socket.connect((server, int(port)))
        except (ConnectionRefusedError, gaierror) as ex:
            print(ex)

    def send(self, message=''):
        ''' Establish a new socket and send message '''
        try:
            self.socket.send(message.encode('utf-8'))
        except Exception as ex:
            print(ex)

    def receive(self, buffer=1024):
        ''' Receive '''
        try:
            return self.socket.recv(buffer).decode()
        except Exception as ex:
            print(ex)

    def http_get(self, uri, close_conn=True):
        ''' HTTP GET method '''
        close = 'Connection: close\r\n'
        if not close_conn:
            close = 'Connection: keep-alive\r\n'

        get_cmd = "GET {uri} HTTP/1.1\r\nHost: {host}\r\n{close} \
        User-agent:Mozilla/5.0\r\n\r\n".format(
            uri=uri, host=self.server, close=close)
        print("Sent HTTP GET:\n {}".format(get_cmd))
        self.send(get_cmd)
        return self.receive()

    def http_post(self, uri, query={}):
        ''' HTTP POST method '''
        content_type = "Content-Type: application/x-www-form-urlencoded"
        query_string = ""
        for key, value in query.items():
            query_string += "{}={}&".format(key, value)

        query_string = query_string[:-1]
        content_length = len(query_string)

        post_cmd = '''
POST {uri} HTTP/1.1
Host: {host}
User-agent: Mozilla/5.0
Connection: keep-alive
{con_type}
Content-Length: {con_len}

{query_string}

'''.format(uri=uri, host=self.server, con_type=content_type, con_len=content_length,
           query_string=query_string)
        print("Sent HTTP POST:\n {}".format(post_cmd))
        self.send(post_cmd)
        return self.receive()

    def close(self):
        ''' Close the socket '''
        self.socket.close()

def main():
    ''' Main '''

    usage = '''
Usage: socket_client.py command [OPTIONS]

Commands:
get                          Lab 1, HTTP GET from tic tac toe server
post                         HTTP-post method to one of my own API's
send server port message     Send a message to a specific server and port

Examples:
python3 socket_client.py get  # Lab 1 tic tac toe
python3 socket_client.py send localhost 1337 Hello there!
'''

    allowed_commands = ['get', 'send', 'post']

    if len(argv) < 2 or argv[1] not in allowed_commands:
        print(usage)
    else:
        sock = SocketClient()

        # HTTP GET command
        if argv[1] == 'get':
            sock.connect('www.ingonline.nu', 80)
            response = sock.http_get('/tictactoe/index.php?board=xoxoxoexx')
            print("GET response:\n{}".format(response))

        # HTTP POST command
        if argv[1] == 'post':
            sock.connect('myserver.se', 5001)
            response = sock.http_post('/api/login', {'username': 'doe', 'password': 'password'})
            print("POST response:\n{}".format(response))

        # Send anything you want
        elif argv[1] == 'send':
            try:
                argv[4]
                message = ' '.join(argv[4:])
            except IndexError:
                message = "hello there!"

            sock.connect(argv[2], argv[3])
            sock.send(message)

            response = sock.receive()
            print("From server: {}".format(response))

        sock.close()

if __name__ == "__main__":
    main()
