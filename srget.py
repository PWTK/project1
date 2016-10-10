import sys
from socket import socket,AF_INET,SOCK_STREAM

class Downloader():
    def __init__(self):
        self.DefaultPort = 80
        self.url = ""
        self.token = ""
        self.socket = socket(AF_INET,SOCK_STREAM)
        self.header = ""
        self.FileName = ""
        self.data = ""
        self.path =  "/Users/JarHan/Downloads"
        self.numConn = 5
    def connect(self):
        self.socket = socket(AF_INET,SOCK_STREAM)
        self.socket.connect((self.url,self.port))
    def GetHeader(self):
        if "connect" == Argument:
            self.header = "GET /auth HTTP/1.1\r\n"
            self.header += "id: {}\r\n".format(self.id)
    def input_splitter(self,url):
        self.FileName = url[2]
        temp_url = url[3]
        if ":" in temp_url:
            self.DefaultPort = temp_url.split(":")[-1]
        else:
            self.url = temp_url

    def Recv(self):
        data = ""
        while True:
            buff = self.socket.recv(4068)
            if not buff:
                break
            data += buff
        self.data =data
        self.header = data.split("\r\n\r\n")[0]
    def WriteFile(self):

