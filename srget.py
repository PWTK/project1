import sys
import os
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
        self.contentLength = 0
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
        self.data = data.split("\r\n\r\n")[-1]
        self.header = data.split("\r\n\r\n")[0]
        self.socket.close()
    def datasize (self):
        header_list = self.header.split("\r\n")
        for fields in header_list:
            if "Content-Length" in fields:
                cl = fields.split(":")[-1]
                self.contentLength = int(cl)

    def WriteFile(self):
        if not os.path.exists(self.path):
            os.makedirs(self.path)

        with open(os.path.join(path, self.FileName), 'wb') as f:
                f.write(self.data)




