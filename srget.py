import sys
import urllib2
from socket import socket,AF_INET,SOCK_STREAM

class Downloader():
    def __init__(self):
        self.DefaultPort = 80
        self.url = ""
        self.token = ""
        self.socket = socket(AF_INET,SOCK_STREAM)
        self.header = ""
    def connect(self):
        self.socket = socket(AF_INET,SOCK_STREAM)
        self.socket.connect((self.url,self.port))

    